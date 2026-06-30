import os
import random
import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader

from .database import engine, Base, get_db, SessionLocal
from .models import Chapter, QAConcept, QuizResult

CHAPTER_FILES = [
    "01_intro_estandar", "02_sistema_valor", "03_principios",
    "04_part2_intro", "05_dominio_ciclo_vida", "06_dominio_planificacion",
    "07_dominio_trabajo", "08_dominio_entrega", "09_dominio_medicion",
    "10_dominio_incertidumbre", "11_adaptacion", "12_modelos_metodos",
    "13_apendices_indice",
]

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
    "13_apendices_indice": "Apéndices e Índice",
}

BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / "chapters"
TEMPLATES_DIR = BASE_DIR / "templates"

jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
jinja_env.globals["CHAPTER_TITLES"] = CHAPTER_TITLES


def render(template_name: str, **kwargs):
    t = jinja_env.get_template(template_name)
    return HTMLResponse(t.render(**kwargs))


@__import__('contextlib').asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_chapters()
    yield


app = FastAPI(title="PMBOK LMS", lifespan=lifespan)

static_dir = str(BASE_DIR / "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


def seed_chapters():
    db = SessionLocal()
    try:
        if db.query(Chapter).count() == 0:
            for i, slug in enumerate(CHAPTER_FILES, 1):
                title = CHAPTER_TITLES.get(slug, slug)
                filepath = CHAPTERS_DIR / f"{slug}.txt"
                content = filepath.read_text(encoding="utf-8") if filepath.exists() else ""
                db.add(Chapter(number=i, title=title, content=content, slug=slug))
            db.commit()
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    chapters = db.query(Chapter).order_by(Chapter.number).all()
    total_qa = db.query(QAConcept).count()
    return render("home.html", request=request, chapters=chapters, total_qa=total_qa)


@app.get("/chapter/{slug}", response_class=HTMLResponse)
async def chapter_view(request: Request, slug: str, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()
    if not chapter:
        return HTMLResponse("Capítulo no encontrado", status_code=404)
    qas = db.query(QAConcept).filter(QAConcept.chapter_id == chapter.id).all()
    return render("chapter.html", request=request, chapter=chapter, qas=qas)


@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request, db: Session = Depends(get_db)):
    chapters = db.query(Chapter).order_by(Chapter.number).all()
    return render("quiz.html", request=request, chapters=chapters)


@app.get("/study", response_class=HTMLResponse)
async def study_page(request: Request, db: Session = Depends(get_db)):
    concepts = db.query(QAConcept).order_by(QAConcept.concept).all()
    chapters_map = {c.id: c.title for c in db.query(Chapter).all()}
    return render("study.html", request=request, concepts=concepts, chapters=chapters_map)


@app.get("/notes", response_class=HTMLResponse)
async def notes_page(request: Request):
    return render("notes.html", request=request)


@app.get("/flipcards", response_class=HTMLResponse)
async def flipcards_page(request: Request, db: Session = Depends(get_db)):
    chapters = db.query(Chapter).order_by(Chapter.number).all()
    return render("flipcards.html", request=request, chapters=chapters)


@app.get("/api/quiz/questions")
async def quiz_questions(
    chapter_id: int = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db),
):
    q = db.query(QAConcept)
    if chapter_id:
        q = q.filter(QAConcept.chapter_id == chapter_id)
    questions = q.order_by(QAConcept.id).all()
    if not questions:
        return []
    selected = random.sample(questions, min(limit, len(questions)))
    return [
        {"id": q.id, "question": q.question, "concept": q.concept,
         "chapter_id": q.chapter_id, "difficulty": q.difficulty}
        for q in selected
    ]


@app.get("/api/quiz/answer/{question_id}")
async def quiz_answer(question_id: int, db: Session = Depends(get_db)):
    qa = db.query(QAConcept).filter(QAConcept.id == question_id).first()
    if not qa:
        return {"error": "not found"}
    return {"id": qa.id, "question": qa.question, "answer": qa.answer,
            "concept": qa.concept, "difficulty": qa.difficulty}


@app.get("/api/flipcards")
async def api_flipcards(chapter_id: int = Query(None), limit: int = Query(20), db: Session = Depends(get_db)):
    q = db.query(QAConcept)
    if chapter_id:
        q = q.filter(QAConcept.chapter_id == chapter_id)
    cards = q.order_by(QAConcept.id).all()
    selected = random.sample(cards, min(limit, len(cards))) if cards else []
    return [
        {"id": c.id, "front": c.question, "back": c.answer,
         "concept": c.concept, "difficulty": c.difficulty}
        for c in selected
    ]


@app.get("/api/search")
async def search(q: str = Query(""), db: Session = Depends(get_db)):
    if not q:
        return []
    results = db.query(QAConcept).filter(
        QAConcept.question.ilike(f"%{q}%") |
        QAConcept.answer.ilike(f"%{q}%") |
        QAConcept.concept.ilike(f"%{q}%")
    ).limit(20).all()
    return [{"id": r.id, "question": r.question[:100], "concept": r.concept} for r in results]


@app.post("/api/notes/save")
async def save_note(request: Request):
    data = await request.json()
    notes_dir = BASE_DIR / "user_notes"
    notes_dir.mkdir(exist_ok=True)
    note_file = notes_dir / f"{data.get('chapter_slug', 'general')}.json"
    import json
    existing = json.loads(note_file.read_text()) if note_file.exists() else []
    existing.append({"id": str(uuid.uuid4()), "text": data.get("text", ""), "created": __import__('datetime').datetime.now().isoformat()})
    note_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    return {"status": "ok"}


@app.get("/api/notes/{chapter_slug}")
async def get_notes(chapter_slug: str):
    import json
    notes_dir = BASE_DIR / "user_notes"
    note_file = notes_dir / f"{chapter_slug}.json"
    if note_file.exists():
        return json.loads(note_file.read_text())
    return []
