from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import User, File as FileModel
from database import get_db
from auth import get_current_user
import os
from datetime import datetime

router = APIRouter()

STORAGE_DIR = "generated_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/upload")
def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file_path = os.path.join(STORAGE_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    db_file = FileModel(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        created_at=datetime.utcnow()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.get("/")
def list_files(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    files = db.query(FileModel).filter(FileModel.user_id == current_user.id).all()
    return files

@router.get("/{file_id}")
def get_file(file_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.delete("/{file_id}")
def delete_file(file_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(file)
    db.commit()
    os.remove(file.file_path)
    return {"detail": "File deleted"}
