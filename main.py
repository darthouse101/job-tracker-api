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

# adds a new job application to the database 
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

# returns all job applications
@app.get("/applications")
def get_all_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()

# returns job applications filtered by status (e.g Applied, Interview )
@app.get("/applications/{status}")
def get_by_status(status: str, db: Session = Depends(get_db)):
    return db.query(Application).filter(Application.status == status).all()

# returns total applications, interviews, and interview success rate
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Application).count()
    interviews = db.query(Application).filter(Application.status == "Interview").count()

    return {
        "total_applications": total,
        "interview_count": interviews,
        "success_rate": interviews / total if total > 0 else 0
    }