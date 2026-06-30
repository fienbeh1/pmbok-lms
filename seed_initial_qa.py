"""
Seed initial QA pairs directly so the site has content.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from lms.database import SessionLocal
from lms.models import Chapter, QAConcept

INITIAL_QA = [
    # Chapter 1: Introducción
    {"chapter": "01_intro_estandar", "qa": [
        {"concept": "Estándar", "question": "¿Qué es El Estándar para la Dirección de Proyectos?", "answer": "Es un conjunto de guías y prácticas reconocidas que describen los fundamentos de la dirección de proyectos, aplicables a la mayoría de los proyectos la mayor parte del tiempo.", "difficulty": "easy"},
        {"concept": "Guía PMBOK", "question": "¿Cuál es el propósito de la Guía del PMBOK®?", "answer": "Proporcionar fundamentos para la dirección de proyectos que incluyen procesos, prácticas, modelos, métodos y artefactos para gestionar proyectos de manera efectiva.", "difficulty": "easy"},
        {"concept": "Valor", "question": "¿Qué significa 'enfocarse en el valor' en dirección de proyectos?", "answer": "Significa evaluar continuamente la alineación del proyecto con los objetivos de negocio, los beneficios esperados y el valor entregado a los interesados.", "difficulty": "medium"},
    ]},
    # Chapter 2: Sistema de Valor
    {"chapter": "02_sistema_valor", "qa": [
        {"concept": "Sistema de Entrega de Valor", "question": "¿Qué es un sistema para la entrega de valor?", "answer": "Es un conjunto de actividades estratégicas, procesos y recursos que una organización utiliza para crear, mantener y entregar valor a través de proyectos, programas y portafolios.", "difficulty": "medium"},
        {"concept": "Gobernanza", "question": "¿Cuál es el rol de la gobernanza organizacional en proyectos?", "answer": "Proporciona la estructura de autoridad, responsabilidad, políticas y procedimientos que guían la toma de decisiones y el comportamiento del equipo del proyecto.", "difficulty": "medium"},
        {"concept": "Entorno del Proyecto", "question": "¿Qué factores del entorno interno afectan un proyecto?", "answer": "Factores como la cultura organizacional, la estructura, los recursos disponibles, las capacidades del equipo, la tecnología y los procesos internos.", "difficulty": "easy"},
    ]},
    # Chapter 3: Principios
    {"chapter": "03_principios", "qa": [
        {"concept": "Administrador Diligente", "question": "¿Qué significa ser un administrador diligente, respetuoso y cuidadoso?", "answer": "Significa actuar con integridad, responsabilidad y cuidado ético, gestionando los recursos del proyecto de manera responsable y considerando el impacto en los interesados y el medio ambiente.", "difficulty": "medium"},
        {"concept": "Entorno Colaborativo", "question": "¿Cómo se crea un entorno colaborativo en el equipo del proyecto?", "answer": "Fomentando la confianza, la comunicación abierta, el respeto mutuo, la diversidad de pensamiento y proporcionando las herramientas y procesos que facilitan la colaboración efectiva.", "difficulty": "medium"},
        {"concept": "Interesados", "question": "¿Por qué es importante involucrarse eficazmente con los interesados?", "answer": "Porque los interesados tienen influencia en el proyecto y sus necesidades y expectativas deben ser comprendidas y gestionadas para asegurar el éxito y la aceptación de los resultados.", "difficulty": "easy"},
        {"concept": "Valor", "question": "¿Qué significa enfocarse en el valor?", "answer": "Significa priorizar la entrega de beneficios y valor al negocio y a los interesados, evaluando continuamente si el proyecto está generando el valor esperado.", "difficulty": "easy"},
        {"concept": "Liderazgo", "question": "¿Qué comportamientos de liderazgo son importantes en dirección de proyectos?", "answer": "Demostrar integridad, visión, capacidad de motivar, comunicación efectiva, empatía, adaptabilidad, pensamiento crítico y capacidad para inspirar y guiar al equipo.", "difficulty": "medium"},
        {"concept": "Calidad", "question": "¿Cómo se incorpora la calidad en los procesos y entregables?", "answer": "Mediante la definición de estándares de calidad desde el inicio, realizando aseguramiento y control de calidad, y fomentando una cultura de mejora continua.", "difficulty": "medium"},
    ]},
]

def seed():
    db = SessionLocal()
    slug_to_id = {ch.slug: ch.id for ch in db.query(Chapter).all()}
    count = 0
    for item in INITIAL_QA:
        chapter_id = slug_to_id.get(item["chapter"])
        if not chapter_id:
            continue
        for qa_data in item["qa"]:
            existing = db.query(QAConcept).filter(
                QAConcept.chapter_id == chapter_id,
                QAConcept.question == qa_data["question"]
            ).first()
            if existing:
                continue
            db.add(QAConcept(
                chapter_id=chapter_id,
                question=qa_data["question"],
                answer=qa_data["answer"],
                concept=qa_data["concept"],
                difficulty=qa_data["difficulty"],
            ))
            count += 1
    db.commit()
    total = db.query(QAConcept).count()
    print(f"Added {count} QA pairs. Total in DB: {total}")
    db.close()

if __name__ == "__main__":
    seed()
