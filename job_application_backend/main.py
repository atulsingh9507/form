from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from database import create_connection
from models import Application
from pathlib import Path
 
app = FastAPI()
 
# Create database connection
conn = create_connection()
 
# Routes
@app.post("/submit")
async def submit_application(
    fullName: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    address: str = Form(...),
    position: str = Form(...),
    gender: str = Form(...),
    qualification: str = Form(...),
    reference: str = Form(None)
):
    try:
        # Save resume to uploads directory
        upload_folder = Path("uploads")
        upload_folder.mkdir(exist_ok=True)
        resume_path = upload_folder / resume.filename
        with open(resume_path, "wb") as f:
            f.write(resume.file.read())
       
        # Insert data into SQLite database
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO applications (fullName, phone, email, resumePath, address, position, gender, qualification, reference)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (fullName, phone, email, str(resume_path), address, position, gender, qualification, reference))
        conn.commit()
        application_id = cursor.lastrowid
        return {"message": f"Application submitted successfully with ID: {application_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit application: {str(e)}")
 
