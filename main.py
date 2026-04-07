from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import date

DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    role = Column(String)
    status = Column(String)
    date_applied = Column(Date)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/applications")
def add_application(app_data: dict, db: Session = Depends(get_db)):
    new_app = Application(
        company=app_data["company"],
        role=app_data["role"],
        status=app_data["status"],
        date_applied=date.today()
    )

    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return new_app


@app.get("/applications")
def get_all_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()


@app.get("/applications/{status}")
def get_by_status(status: str, db: Session = Depends(get_db)):
    return db.query(Application).filter(Application.status == status).all()

