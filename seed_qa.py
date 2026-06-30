"""
Seed QA pairs into the database from generated JSON files.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lms.database import SessionLocal
from lms.models import Chapter, QAConcept


def seed():
    db = SessionLocal()
    qa_dir = Path("qa_output")
    
    # Map chapter slugs
    slug_map = {}
    for ch in db.query(Chapter).all():
        slug_map[ch.slug] = ch.id
    
    for qa_file in sorted(qa_dir.glob("*_qa.json")):
        if qa_file.name == "all_qa.json":
            continue
        slug = qa_file.stem.replace("_qa", "")
        chapter_id = slug_map.get(slug)
        if not chapter_id:
            print(f"  No chapter found for slug: {slug}")
            continue
        
        with open(qa_file, "r", encoding="utf-8") as f:
            items = json.load(f)
        
        count = 0
        for item in items:
            # Check if already exists
            existing = db.query(QAConcept).filter(
                QAConcept.chapter_id == chapter_id,
                QAConcept.question == item.get("question", ""),
            ).first()
            if existing:
                continue
            
            qa = QAConcept(
                chapter_id=chapter_id,
                question=item.get("question", ""),
                answer=item.get("answer", ""),
                concept=item.get("concept", "General"),
                difficulty=item.get("difficulty", "medium"),
            )
            db.add(qa)
            count += 1
        
        db.commit()
        print(f"  {slug}: added {count} QA pairs")
    
    total = db.query(QAConcept).count()
    print(f"\nTotal QA in database: {total}")
    db.close()


if __name__ == "__main__":
    seed()
