"""
Generate QA pairs from PMBOK chapters using local ollama model (llama3.1:8b)
"""
import json
import re
import time
import httpx
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"
CHAPTERS_DIR = Path("chapters")
OUTPUT_DIR = Path("qa_output")

CHAPTER_TITLES = {
    "01_intro_estandar": "Introducción al Estándar",
    "02_sistema_valor": "Sistema para la Entrega de Valor",
    "03_principios": "12 Principios de la Dirección de Proyectos",
    "04_part2_intro": "Introducción a la Guía PMBOK",
    "05_dominio_ciclo_vida": "Dominio: Enfoque de Desarrollo y Ciclo de Vida",
    "06_dominio_planificacion": "Dominio: Planificación",
    "07_dominio_trabajo": "Dominio: Trabajo del Proyecto",
    "08_dominio_entrega": "Dominio: Entrega",
    "09_dominio_medicion": "Dominio: Medición",
    "10_dominio_incertidumbre": "Dominio: Incertidumbre",
    "11_adaptacion": "Adaptación",
    "12_modelos_metodos": "Modelos, Métodos y Artefactos",
}

SYSTEM_PROMPT = """Eres un experto en dirección de proyectos PMBOK. 
Genera preguntas de opción múltiple y sus respuestas basadas en el texto proporcionado.
Cada QA debe seguir este formato JSON exacto:
{"concept": "nombre del concepto", "question": "pregunta clara", "answer": "respuesta detallada", "difficulty": "easy|medium|hard"}

Genera SOLO arrays JSON válidos, sin texto adicional."""


def query_ollama(prompt: str, system: str = None) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 2048},
    }
    if system:
        payload["system"] = system

    for attempt in range(3):
        try:
            resp = httpx.post(OLLAMA_URL, json=payload, timeout=300)
            resp.raise_for_status()
            return resp.json().get("response", "")
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(5)
    return ""


def extract_json(text: str) -> list:
    # Try to find JSON array in the response
    json_match = re.search(r'\[[\s\S]*\]', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    # Try single object
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return [json.loads(json_match.group())]
        except json.JSONDecodeError:
            pass
    return []


def chunk_text(text: str, max_chars: int = 3000) -> list:
    words = text.split()
    chunks = []
    current = []
    current_len = 0
    for w in words:
        if current_len + len(w) > max_chars and current:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
        current.append(w)
        current_len += len(w) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def generate_qa_for_chapter(slug: str, title: str):
    filepath = CHAPTERS_DIR / f"{slug}.txt"
    if not filepath.exists():
        print(f"  File not found: {filepath}")
        return []

    text = filepath.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    all_qa = []

    print(f"  Processing {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        prompt = f"""Basado en el siguiente texto del capítulo "{title}" del PMBOK 7ma edición, genera de 2 a 4 preguntas de opción múltiple con respuestas.

TEXTO:
{chunk}

Responde SOLO con un array JSON válido. Ejemplo:
[{{"concept": "Ciclo de Vida", "question": "¿Qué es un ciclo de vida del proyecto?", "answer": "Serie de fases que atraviesa un proyecto desde su inicio hasta su conclusión", "difficulty": "easy"}}]"""
        
        print(f"  Chunk {i+1}/{len(chunks)}...")
        response = query_ollama(prompt, SYSTEM_PROMPT)
        qa_items = extract_json(response)
        print(f"    Generated {len(qa_items)} QA items")
        all_qa.extend(qa_items)
        time.sleep(0.5)

    return all_qa


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_qa = []

    for slug, title in CHAPTER_TITLES.items():
        print(f"\n=== {title} ({slug}) ===")
        qa = generate_qa_for_chapter(slug, title)
        
        # Save per-chapter
        output_file = OUTPUT_DIR / f"{slug}_qa.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(qa, f, ensure_ascii=False, indent=2)
        print(f"  Saved {len(qa)} items to {output_file}")
        all_qa.extend(qa)

    # Save all combined
    with open(OUTPUT_DIR / "all_qa.json", "w", encoding="utf-8") as f:
        json.dump(all_qa, f, ensure_ascii=False, indent=2)
    print(f"\nTotal QA pairs generated: {len(all_qa)}")


if __name__ == "__main__":
    main()
