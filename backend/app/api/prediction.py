from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Dict, Any, List
import random
import sqlite3
import json
from datetime import datetime
from app.db import get_db
from app.api.auth_utils import get_current_user

router = APIRouter(prefix="/api/prediction", tags=["prediction"])

@router.post("/analyze")
async def analyze_fingerprint(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Experimental ML Inference endpoint.
    Takes an image upload, creates a mock prediction, and saves it to the DB.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Mock analysis delay
    import asyncio
    await asyncio.sleep(1.5)
    
    classes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    predicted_idx = random.randint(0, len(classes) - 1)
    prediction = classes[predicted_idx]
    
    base_confidence = 0.85 + (random.random() * 0.14)
    remaining = 1.0 - base_confidence
    probabilities: Dict[str, float] = {}
    
    for i, c in enumerate(classes):
        if i == predicted_idx:
            probabilities[c] = base_confidence
        else:
            prob = random.random() * remaining
            probabilities[c] = prob
            remaining -= prob
            
    other_idx = 1 if predicted_idx == 0 else 0
    probabilities[classes[other_idx]] += remaining
    quality_score = 0.85 + (random.random() * 0.15)
    
    # Save to DB
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO predictions (user_id, prediction, confidence, probabilities, quality_score)
        VALUES (?, ?, ?, ?, ?)
    """, (current_user["id"], prediction, base_confidence, json.dumps(probabilities), quality_score))
    db.commit()
    
    return {
        "id": cursor.lastrowid,
        "prediction": prediction,
        "confidence": base_confidence,
        "probabilities": probabilities,
        "quality_score": quality_score,
        "model_version": "bloodid-efficientnet-mock-v1",
        "explanation": {},
        "created_at": datetime.utcnow().isoformat()
    }

@router.get("/history")
async def get_history(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Returns prediction history for the current user"""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, prediction, confidence, probabilities, quality_score, created_at 
        FROM predictions 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """, (current_user["id"],))
    
    rows = cursor.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": str(row["id"]),
            "prediction": row["prediction"],
            "confidence": row["confidence"],
            "probabilities": json.loads(row["probabilities"]),
            "quality_score": row["quality_score"],
            "created_at": row["created_at"]
        })
    return history

