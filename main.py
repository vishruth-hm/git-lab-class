from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------- DATABASE ----------------

DATABASE_URL = "sqlite:///./placement.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ---------------- TABLES ----------------

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    department = Column(String)
    cgpa = Column(Float)
    graduation_year = Column(Integer)
    skills = Column(String)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    location = Column(String)
    industry = Column(String)
    website = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    job_title = Column(String)
    package = Column(Float)
    eligibility = Column(String)
    deadline = Column(String)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    date = Column(String)
    status = Column(String)


Base.metadata.create_all(bind=engine)


# ---------------- FASTAPI ----------------

app = FastAPI(title="Placement Management Portal")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ---------------- PYDANTIC MODELS ----------------

class StudentData(BaseModel):
    name: str
    email: str
    department: str
    cgpa: float
    graduation_year: int
    skills: str


class CompanyData(BaseModel):
    company_name: str
    location: str
    industry: str
    website: str


class JobData(BaseModel):
    company_id: int
    job_title: str
    package: float
    eligibility: str
    deadline: str


class ApplicationData(BaseModel):
    student_id: int
    job_id: int
    date: str
    status: str


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Placement Management Portal API is running"
    }


# ---------------- STUDENTS ----------------

@app.post("/students")
def add_student(data: StudentData):

    db = SessionLocal()

    student = Student(
        name=data.name,
        email=data.email,
        department=data.department,
        cgpa=data.cgpa,
        graduation_year=data.graduation_year,
        skills=data.skills
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    db.close()

    return student


@app.get("/students")
def get_students():

    db = SessionLocal()

    students = db.query(Student).all()

    result = []

    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "department": s.department,
            "cgpa": s.cgpa,
            "graduation_year": s.graduation_year,
            "skills": s.skills
        })

    db.close()

    return result


@app.get("/students/{student_id}")
def get_student(student_id: int):

    db = SessionLocal()

    student = db.query(Student).filter(Student.id == student_id).first()

    db.close()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ---------------- COMPANIES ----------------

@app.post("/companies")
def add_company(data: CompanyData):

    db = SessionLocal()

    company = Company(
        company_name=data.company_name,
        location=data.location,
        industry=data.industry,
        website=data.website
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    db.close()

    return company


@app.get("/companies")
def get_companies():

    db = SessionLocal()

    companies = db.query(Company).all()

    result = []

    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "location": c.location,
            "industry": c.industry,
            "website": c.website
        })

    db.close()

    return result


@app.get("/companies/{company_id}")
def get_company(company_id: int):

    db = SessionLocal()

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    db.close()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# ---------------- JOBS ----------------

@app.post("/jobs")
def add_job(data: JobData):

    db = SessionLocal()

    company = db.query(Company).filter(
        Company.id == data.company_id
    ).first()

    if not company:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    job = Job(
        company_id=data.company_id,
        job_title=data.job_title,
        package=data.package,
        eligibility=data.eligibility,
        deadline=data.deadline
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    db.close()

    return job


@app.get("/jobs")
def get_jobs():

    db = SessionLocal()

    jobs = db.query(Job).all()

    result = []

    for job in jobs:

        company = db.query(Company).filter(
            Company.id == job.company_id
        ).first()

        result.append({
            "id": job.id,
            "company_id": job.company_id,
            "company_name": company.company_name if company else "Unknown",
            "job_title": job.job_title,
            "package": job.package,
            "eligibility": job.eligibility,
            "deadline": job.deadline
        })

    db.close()

    return result


# ---------------- APPLICATIONS ----------------

@app.post("/applications")
def apply_job(data: ApplicationData):

    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    job = db.query(Job).filter(
        Job.id == data.job_id
    ).first()

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if not job:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    application = Application(
        student_id=data.student_id,
        job_id=data.job_id,
        date=data.date,
        status=data.status
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    db.close()

    return application


@app.get("/applications")
def get_applications():

    db = SessionLocal()

    applications = db.query(Application).all()

    result = []

    for a in applications:

        student = db.query(Student).filter(
            Student.id == a.student_id
        ).first()

        job = db.query(Job).filter(
            Job.id == a.job_id
        ).first()

        result.append({
            "id": a.id,
            "student_name": student.name if student else "Unknown",
            "job_title": job.job_title if job else "Unknown",
            "date": a.date,
            "status": a.status
        })

    db.close()

    return result


# ---------------- DASHBOARD ----------------

@app.get("/dashboard")
def dashboard():

    db = SessionLocal()

    students = db.query(Student).count()
    companies = db.query(Company).count()
    jobs = db.query(Job).count()
    applications = db.query(Application).count()

    db.close()

    return {
        "students": students,
        "companies": companies,
        "jobs": jobs,
        "applications": applications
    }