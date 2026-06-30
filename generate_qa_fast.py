"""Fast QA generation using qwen2.5:3b model"""
import json, re, time, httpx, sys
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"
CHAPTERS_DIR = Path("lms/chapters")
OUTPUT_DIR = Path("qa_output")

CHAPTER_TITLES = {
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
    "13_apendices_indice": "Apéndices e Índice",
}

def query(prompt, system=None, timeout=120):
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.2, "num_predict": 1024}}
    if system: payload["system"] = system
    for attempt in range(3):
        try:
            r = httpx.post(OLLAMA_URL, json=payload, timeout=timeout)
            return r.json().get("response", "")
        except Exception as e:
            print(f"  Attempt {attempt+1}: {e}")
            time.sleep(3)
    return ""

def extract_json(text):
    m = re.search(r'\[[\s\S]*?\]', text)
    if m:
        try: return json.loads(m.group())
        except: pass
    m = re.search(r'\{[\s\S]*?\}', text)
    if m:
        try: return [json.loads(m.group())]
        except: pass
    return []

def generate(slug, title):
    fp = CHAPTERS_DIR / f"{slug}.txt"
    if not fp.exists(): return []
    text = fp.read_text(encoding="utf-8")
    chunks = []
    words = text.split()
    for i in range(0, len(words), 800):
        chunks.append(" ".join(words[i:i+800]))
    
    all_qa = []
    for i, chunk in enumerate(chunks):
        prompt = f"""Del capítulo "{title}" del PMBOK 7, genera 2-3 preguntas con respuestas.

Texto: {chunk[:2500]}

Responde SOLO JSON array:
[{{"concept":"...","question":"...","answer":"...","difficulty":"easy|medium|hard"}}]"""
        print(f"  Chunk {i+1}/{len(chunks)}...")
        resp = query(prompt)
        qa = extract_json(resp)
        print(f"    -> {len(qa)} QA")
        all_qa.extend(qa)
        time.sleep(0.3)
    return all_qa

OUTPUT_DIR.mkdir(exist_ok=True)
total = 0
for slug, title in CHAPTER_TITLES.items():
    out = OUTPUT_DIR / f"{slug}_qa.json"
    if out.exists():
        print(f"\n{slug}: already exists, skipping")
        total += len(json.loads(out.read_text()))
        continue
    print(f"\n=== {title} ===")
    qa = generate(slug, title)
    out.write_text(json.dumps(qa, ensure_ascii=False, indent=2))
    print(f"  Saved {len(qa)} items")
    total += len(qa)

print(f"\nTotal: {total} QA pairs")
