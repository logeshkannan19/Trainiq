import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
from datetime import datetime
import json

from openai_service import OpenAIService
from database import Database
from scheduler import WorkoutScheduler
from whatsapp_service import WhatsAppService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Trainiq Fit API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
openai_service = OpenAIService()
scheduler = WorkoutScheduler(db, openai_service)
whatsapp_service = WhatsAppService()

class WhatsAppMessage(BaseModel):
    from_: str
    body: str
    timestamp: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "ok", "service": "Trainiq Fit API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify WhatsApp webhook"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "trainiq_verify_token")
    
    if mode == "subscribe" and token == verify_token:
        logger.info("Webhook verified successfully")
        return int(challenge)
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_webhook(request: Request):
    """Receive WhatsApp messages"""
    try:
        body = await request.json()
        logger.info(f"Received webhook: {json.dumps(body, indent=2)}")
        
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        for message in messages:
            phone = message.get("from")
            msg_body = message.get("text", {}).get("body", "")
            
            if phone and msg_body:
                await handle_message(phone, msg_body)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}

async def handle_message(phone: str, message: str):
    """Handle incoming WhatsApp message"""
    logger.info(f"Handling message from {phone}: {message}")
    
    user = db.get_or_create_user(phone)
    intent = openai_service.detect_intent(message)
    
    logger.info(f"Detected intent: {intent}")
    
    if intent["type"] == "workout_request":
        workout = openai_service.generate_workout(intent.get("params", {}))
        response = format_workout_response(workout)
        db.save_workout(user["id"], workout)
        
    elif intent["type"] == "diet_request":
        diet = openai_service.generate_diet_plan(intent.get("params", {}))
        response = format_diet_response(diet)
        
    elif intent["type"] == "skip":
        db.log_skip(user["id"])
        response = "No worries! Rest is important. I'll send you a lighter workout tomorrow 💪"
        
    elif intent["type"] == "done":
        db.log_completion(user["id"])
        response = "Great job! 🎉 Keep up the momentum!"
        
    elif intent["type"] == "question":
        response = openai_service.answer_fitness_question(message)
        
    else:
        response = "I'm here to help with your fitness journey! Try:\n- 'Give me a workout'\n- 'What should I eat?'\n- 'I skipped yesterday'"
    
    whatsapp_service.send_message(phone, response)

def format_workout_response(workout: dict) -> str:
    """Format workout for WhatsApp"""
    exercises = workout.get("exercises", [])
    formatted = f"🏋️ *{workout.get('name', 'Workout')}*\n\n"
    
    for i, ex in enumerate(exercises, 1):
        formatted += f"{i}. {ex['name']} - {ex['sets']}x{ex['reps']}\n"
    
    formatted += f"\n⏱️ Duration: ~{workout.get('duration_minutes', 30)} mins\n"
    formatted += f"🔥 Est. Calories: {workout.get('calories', 200)}"
    
    return formatted

def format_diet_response(diet: dict) -> str:
    """Format diet plan for WhatsApp"""
    meals = diet.get("meals", [])
    formatted = f"🥗 *{diet.get('name', 'Diet Plan')}*\n\n"
    
    for meal in meals:
        formatted += f"*{meal['time']}:* {meal['food']}\n"
    
    formatted += f"\n📊 Total: {diet.get('calories', 2000)} cal"
    
    return formatted

@app.on_event("startup")
async def startup():
    """Start scheduled jobs"""
    logger.info("Starting Trainiq Fit API...")
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    """Stop scheduled jobs"""
    logger.info("Shutting down Trainiq Fit API...")
    scheduler.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000) or 8000))
