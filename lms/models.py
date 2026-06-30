from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from .database import Base


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True)
    title = Column(String(255))
    content = Column(Text)
    slug = Column(String(100), unique=True)


class QAConcept(Base):
    __tablename__ = "qa_concepts"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    question = Column(Text)
    answer = Column(Text)
    concept = Column(String(255))
    difficulty = Column(String(50), default="medium")


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100))
    question_id = Column(Integer, ForeignKey("qa_concepts.id"))
    correct = Column(Integer, default=0)
    score = Column(Float, default=0.0)
