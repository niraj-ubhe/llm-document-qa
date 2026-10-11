from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Document
from app.schemas import DocumentCreate, DocumentResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    with SessionLocal() as session:
        yield session


@app.get("/")
def read_root():
    return {"message": "LLM Document Q&A API"}


@app.get("/health")
def read_health():
    return {"status": "ok"}


@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(
    document_data: DocumentCreate, db: Session = Depends(get_db)
):
    document = Document(**document_data.model_dump())
    db.add(document)

    try:
        db.commit()
        db.refresh(document)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=503, detail="Could not save document metadata."
        ) from error

    return document


@app.get("/documents", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    try:
        return db.scalars(select(Document).order_by(Document.id)).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503, detail="Could not retrieve document metadata."
        ) from error
