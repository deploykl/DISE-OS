import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from ddgs import DDGS  # ← CAMBIADO
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
import re

console = Console()

class AsistentePersonal:
    def __init__(self, nombre_asistente="Asistente"):
        self.nombre = nombre_asistente
        self.console = Console()
        
        # Crear directorios si no existen
        os.makedirs("asistente_data", exist_ok=True)
        
        # Inicializar modelo de lenguaje local
        console.print("🧠 Cargando modelo de lenguaje...")
        self.modelo = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Inicializar base de datos vectorial
        self.chroma_client = chromadb.PersistentClient(path="./asistente_data/vector_db")
        self.coleccion = self.chroma_client.get_or_create_collection(
            name="conocimiento",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Inicializar base de datos SQL
        self.conn = sqlite3.connect('asistente_data/memoria.db')
        self.crear_tablas()
        
        # Cargar memoria
        self.memoria = self.cargar_memoria()
        
        console.print(f"✅ ¡{self.nombre} está listo!\n")
    
    def crear_tablas(self):
        """Crea las tablas de la base de datos"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            usuario TEXT,
            asistente TEXT,
            contexto TEXT,
            embedding_id TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hechos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            hecho TEXT,
            embedding_id TEXT,
            fecha_aprendido TEXT,
            relevancia INTEGER DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferencias (
            clave TEXT PRIMARY KEY,
            valor TEXT,
            fecha_actualizacion TEXT
        )
        ''')
        
        self.conn.commit()
    
    def cargar_memoria(self):
        """Carga la memoria guardada"""
        cursor = self.conn.cursor()
        memoria = {
            "hechos": [],
            "preferencias": {},
            "ultima_conversacion": None
        }
        
        cursor.execute("SELECT categoria, hecho FROM hechos ORDER BY relevancia DESC LIMIT 100")
        memoria["hechos"] = cursor.fetchall()
        
        cursor.execute("SELECT clave, valor FROM preferencias")
        for clave, valor in cursor.fetchall():
            memoria["preferencias"][clave] = valor
        
        return memoria
    
    def aprender_hecho(self, hecho: str, categoria: str = "general"):
        """Aprende un hecho nuevo"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM hechos WHERE hecho LIKE ?", 
            (f"%{hecho[:50]}%",)
        )
        
        if cursor.fetchone():
            cursor.execute(
                "UPDATE hechos SET relevancia = relevancia + 1 WHERE hecho LIKE ?",
                (f"%{hecho[:50]}%",)
            )
        else:
            embedding = self.modelo.encode(hecho).tolist()
            embedding_id = f"hecho_{datetime.now().timestamp()}"
            
            self.coleccion.add(
                embeddings=[embedding],
                documents=[hecho],
                ids=[embedding_id],
                metadatas=[{"categoria": categoria}]
            )
            
            # CORREGIDO: guardar fecha como texto
            cursor.execute(
                "INSERT INTO hechos (categoria, hecho, embedding_id, fecha_aprendido) VALUES (?, ?, ?, ?)",
                (categoria, hecho, embedding_id, datetime.now().isoformat())
            )
        
        self.conn.commit()
        return f"✅ He aprendido: {hecho[:100]}..."
    
    def buscar_memoria(self, consulta: str, n_resultados: int = 5) -> List[str]:
        """Busca en la memoria"""
        try:
            embedding_consulta = self.modelo.encode(consulta).tolist()
            
            resultados = self.coleccion.query(
                query_embeddings=[embedding_consulta],
                n_results=n_resultados
            )
            
            if resultados['documents']:
                return resultados['documents'][0]
            return []
        except:
            return []
    
    def buscar_internet(self, consulta: str) -> str:
        """Busca en internet usando DDGS (nueva librería)"""
        try:
            console.print("🌐 Buscando en internet...")
            with DDGS() as ddgs:
                resultados = list(ddgs.text(consulta, max_results=3))
                
                if resultados:
                    respuesta = "📡 Información de internet:\n\n"
                    for i, r in enumerate(resultados, 1):
                        respuesta += f"{i}. {r['title']}\n"
                        respuesta += f"   {r['body'][:200]}...\n"
                        respuesta += f"   🔗 {r['href']}\n\n"
                    return respuesta
                return "No encontré información relevante en internet."
        except Exception as e:
            console.print(f"[yellow]⚠️ Error de internet: {e}[/yellow]")
            return "No pude conectarme a internet. Pero puedo ayudarte con lo que sé."
    
    def analizar_pregunta(self, pregunta: str) -> str:
        """Analiza el tipo de pregunta"""
        pregunta_lower = pregunta.lower()
        
        # Detectar saludos y presentaciones
        saludos = ['hola', 'hey', 'buenos días', 'buenas tardes', 'buenas noches']
        if any(s in pregunta_lower for s in saludos):
            return "saludo"
        
        # Detectar presentación (HOLA SOY...)
        if 'soy' in pregunta_lower or 'me llamo' in pregunta_lower:
            return "presentacion"
        
        # Detectar hora
        if any(p in pregunta_lower for p in ['hora', 'qué hora', 'que hora']):
            return "hora"
        
        # Detectar fecha
        if any(p in pregunta_lower for p in ['fecha', 'día', 'que día', 'qué día']):
            return "fecha"
        
        # Detectar búsqueda en internet
        if any(p in pregunta_lower for p in ['busca', 'buscar', 'internet', 'web', 'online']):
            return "internet"
        
        # Detectar guardar información
        if any(p in pregunta_lower for p in ['recuerda', 'guarda', 'aprende', 'memoriza', 'recuérdame']):
            return "aprender"
        
        return "conversacion"
    
    def responder(self, pregunta: str) -> str:
        """Procesa la pregunta"""
        tipo = self.analizar_pregunta(pregunta)
        
        # Respuestas según tipo
        if tipo == "saludo":
            nombre_usuario = self.memoria.get("preferencias", {}).get("nombre_usuario", "")
            if nombre_usuario:
                respuesta = f"¡Hola {nombre_usuario}! ¿En qué puedo ayudarte hoy?"
            else:
                respuesta = "¡Hola! ¿Cómo te llamas? Así puedo recordarte mejor."
        
        elif tipo == "presentacion":
            # Extraer nombre
            nombre = pregunta.replace('hola', '').replace('soy', '').replace('me llamo', '').strip().upper()
            # Guardar nombre como preferencia
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO preferencias (clave, valor, fecha_actualizacion) VALUES (?, ?, ?)",
                ("nombre_usuario", nombre, datetime.now().isoformat())
            )
            self.conn.commit()
            # Recargar memoria
            self.memoria = self.cargar_memoria()
            
            respuesta = f"¡Mucho gusto {nombre}! He guardado tu nombre. ¿En qué puedo ayudarte?"
        
        elif tipo == "hora":
            ahora = datetime.now()
            respuesta = f"🕐 Son las {ahora.strftime('%H:%M')} del {ahora.strftime('%d de %B de %Y')}"
        
        elif tipo == "fecha":
            ahora = datetime.now()
            respuesta = f"📅 Hoy es {ahora.strftime('%A, %d de %B de %Y')}"
        
        elif tipo == "aprender":
            hecho = pregunta.replace('recuerda', '').replace('guarda', '').replace('aprende', '').replace('memoriza', '').strip()
            self.aprender_hecho(hecho, "usuario")
            respuesta = f"✅ ¡Listo! He guardado: '{hecho}'"
        
        elif tipo == "internet":
            respuesta = self.buscar_internet(pregunta)
        
        else:
            # Buscar en memoria
            recuerdos = self.buscar_memoria(pregunta)
            
            if recuerdos:
                respuesta = "💭 Basado en lo que sé:\n\n"
                for i, recuerdo in enumerate(recuerdos, 1):
                    respuesta += f"{i}. {recuerdo}\n"
            else:
                respuesta = self.buscar_internet(pregunta)
        
        # Guardar conversación (fecha como texto)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO conversaciones (timestamp, usuario, asistente) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), pregunta, respuesta)
        )
        self.conn.commit()
        
        return respuesta
    
    def chat(self):
        """Modo chat interactivo"""
        console.print(f"""
╔══════════════════════════════════════╗
║     🤖 {self.nombre.upper()} - TU ASISTENTE     ║
║     Aprendo, recuerdo y busco       ║
║     Escribe 'salir' para terminar   ║
╚══════════════════════════════════════╝
""")
        
        while True:
            try:
                pregunta = console.input("\n[bold cyan]Tú:[/bold cyan] ")
                
                if pregunta.lower() in ['salir', 'exit', 'quit', 'adiós']:
                    nombre = self.memoria.get("preferencias", {}).get("nombre_usuario", "amigo")
                    console.print(f"\n[bold green]{self.nombre}:[/bold green] ¡Hasta luego {nombre}! He aprendido mucho 🧠")
                    break
                
                respuesta = self.responder(pregunta)
                console.print(f"\n[bold green]{self.nombre}:[/bold green] {respuesta}")
                
            except KeyboardInterrupt:
                console.print("\n\n[bold yellow]¡Hasta pronto![/bold yellow]")
                break
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {e}")

# Iniciar
if __name__ == "__main__":
    # CAMBIA ESTE NOMBRE
    asistente = AsistentePersonal("LUIS-BOT")
    asistente.chat()