from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlite3
from app.db import get_db
from app.api.auth_utils import get_current_user

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingsUpdate(BaseModel):
    notifications_enabled: bool
    theme: str
    language: str

@router.get("/")
def get_settings(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT notifications_enabled, theme, language FROM settings WHERE user_id = ?", (current_user["id"],))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return {"notifications_enabled": True, "theme": "system", "language": "en"}

@router.put("/")
def update_settings(settings: SettingsUpdate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE settings 
        SET notifications_enabled = ?, theme = ?, language = ?
        WHERE user_id = ?
    """, (settings.notifications_enabled, settings.theme, settings.language, current_user["id"]))
    db.commit()
    return {"status": "success"}
