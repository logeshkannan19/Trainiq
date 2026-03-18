from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
import database as db
import openai_service as ai
import whatsapp_service as wa
import logging

# Configure logger to be detailed for production readiness
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("Trainiq.Webhooks")

app = FastAPI(
    title="Trainiq API Webhooks",
    description="Inbound router for Meta's WhatsApp Cloud API",
    version="1.1.0"
)

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Meta WhatsApp Webhook Verification"""
    hub_mode = request.query_params.get("hub.mode")
    hub_challenge = request.query_params.get("hub.challenge")
    hub_verify_token = request.query_params.get("hub.verify_token")
    
    if hub_mode == "subscribe" and hub_verify_token == "TRAINIQ_SECURE_TOKEN":
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def handle_whatsapp_message(request: Request, background_tasks: BackgroundTasks):
    """
    Receives inbound messages from users via WhatsApp.
    We offload the heavy LLM lifting to background tasks so we don't
    timeout the Meta webhook endpoint (they expect a 200 OK fast).
    """
    try:
        data = await request.json()
        logger.debug(f"Raw incoming payload: {data}")
        
        # Meta's webhook payload is deeply nested. Let's safely extract what we need.
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            # Often Meta sends status updates (delivered, read). We just ack them.
            return {"status": "ok", "message": "No actionable messages found"}
            
        msg = messages[0]
        user_phone = msg.get("from")
        msg_body = msg.get("text", {}).get("body", "")
        
        # If it's a voice note, there's a different payload structure, but we'll focus on text for the MVP.
        if not msg_body:
            logger.warning(f"Received non-text message from {user_phone}. Skipping.")
            return {"status": "ok"}
            
        logger.info(f"Received message from {user_phone}: {msg_body[:50]}...")
        
        # Validate the user. We only talk to registered Trainiq athletes.
        user = db.get_user_by_phone(user_phone)
        if not user:
            logger.warning(f"Unknown number interacted: {user_phone}")
            wa.send_whatsapp_message(
                user_phone, 
                "Welcome to Trainiq! I don't recognize this number yet. Please bind it at trainiq.app first so I can pull your fitness profile."
            )
            return {"status": "ok"}
            
        # Push the AI processing to a background task for snappy UX
        background_tasks.add_task(process_inbound_message, user, msg_body, user_phone)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Critical error handling webhook payload: {e}", exc_info=True)
        # We still return 200 so Meta doesn't disable our endpoint due to repeated 500s
        return {"status": "error"}

def process_inbound_message(user: dict, msg_body: str, user_phone: str):
    """
    The actual brain of the operation. Parses intent and routes to the correct system logic.
    """
    try:
        # 1. Detect Intent using OpenAI
        parsed_intent = ai.detect_intent(msg_body)
        intent = parsed_intent.get("intent", "general_chat")
        
        # 2. Route Logic based on intent
        bot_response = ""
        if intent == "mark_done":
            db.update_workout_status(user["id"], "completed", "perfect")
            bot_response = "Stellar job today! I've logged your workout as complete. Enjoy the rest and recover well! 🔥"
            
        elif intent == "skip":
            db.update_workout_status(user["id"], "skipped")
            bot_response = "Understood. I've marked today as a rest day. Listen to your body—we'll hit it hard tomorrow! 😴"
            
        elif intent == "change_workout":
            # The user wants something else. Let's regenerate dynamically.
            logger.info(f"User {user['full_name']} requested a workout change.")
            new_workout = ai.generate_workout(user, recent_feedback=f"Requested change: {msg_body}")
            db.create_workout(user["id"], new_workout)
            bot_response = f"Got it. I pivoted your plan. Check this out:\n\n{new_workout}"
            
        else:
            # Fallback chat
            bot_response = "Noted! Hit me with a 'done' or '1' when you finish today's session."
            
        # 3. Save to DB audit trail and reply to the user
        db.log_interaction(user["id"], "text", msg_body, intent, bot_response)
        wa.send_whatsapp_message(user_phone, bot_response)
        logger.info(f"Successfully processed and replied to {user['full_name']}.")

    except Exception as e:
        logger.error(f"Failed to process message for {user['full_name']}: {e}", exc_info=True)
