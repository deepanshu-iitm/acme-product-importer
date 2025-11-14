from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"

@router.post("/")
def upload_csv(file: UploadFile = File(...)):
    # Only allow CSV files
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Create unique file name
    file_id = str(uuid.uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    # Save the uploaded file to disk
    with open(saved_path, "wb") as f:
        f.write(file.file.read())

    return {
        "message": "File uploaded successfully",
        "file_id": file_id,
        "path": saved_path
    }
