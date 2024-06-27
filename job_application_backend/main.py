# main.py

from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from database import engine, SessionLocal
from models import Base, Application
from schemas import ApplicationResponse
from database import get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/Application_Form")
async def submit_application(
    fullName: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    upload_file: UploadFile = File(...),
    photo: UploadFile = File(None),
    address: str = Form(...),
    position: str = Form(...),
    gender: str = Form(...),
    qualification: str = Form(...),
    reference: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Save resume file
        upload_folder = Path("uploads")
        upload_folder.mkdir(parents=True, exist_ok=True)
        resume_path = upload_folder / upload_file.filename
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)
        
        # Save photo file if provided
        photo_path = None
        if photo:
            photo_path = upload_folder / photo.filename
            with open(photo_path, "wb") as f:
                shutil.copyfileobj(photo.file, f)
        
        # Create Application instance
        application = Application(
            fullName=fullName,
            phone=phone,
            email=email,
            resumePath=str(resume_path),
            photoPath=str(photo_path) if photo_path else None,
            address=address,
            position=position,
            gender=gender,
            qualification=qualification,
            reference=reference
        )
        
        # Add to database session
        db.add(application)
        db.commit()
        db.refresh(application)
        
        return {"message": "Application submitted successfully", "application_id": application.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit application: {str(e)}")

@app.get("/get_resume_by_path")
async def get_resume_by_path(resume_path: str = Query(..., description="Path to the resume file")):
    try:
        path = Path(resume_path)
        if not path.is_file():
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve resume: {str(e)}")

@app.get("/get_photo_by_path")
async def get_photo_by_path(photo_path: str = Query(..., description="Path to the photo file")):
    try:
        path = Path(photo_path)
        if not path.is_file():
            raise HTTPException(status_code=404, detail="Photo not found")
        
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve photo: {str(e)}")

@app.get("/get_application_details/{application_id}", response_model=ApplicationResponse)
async def get_application_details(application_id: int, db: Session = Depends(get_db)):
    try:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return application
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve application details: {str(e)}")
