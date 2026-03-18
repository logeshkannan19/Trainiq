import os
import logging
from supabase import create_client, Client
from typing import Optional, List, Dict, Any

logger = logging.getLogger("Trainiq.Database")

# It's risky to crash on boot if env vars are missing, but for the DB, it's a hard requirement.
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    logger.critical("🚨 SUPABASE_URL or SUPABASE_KEY is missing from environment variables!")
    # We fallback to dummy strings here to prevent app crash during local CI, but it will fail on query.
    url = url or "https://dummy.supabase.co"
    key = key or "dummy-key"

supabase: Client = create_client(url, key)

def get_user_by_phone(phone_number: str) -> Optional[Dict[str, Any]]:
    """Retrieve a user by their registered WhatsApp number."""
    try:
        response = supabase.table('users').select('*').eq('phone_number', phone_number).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Failed to fetch user by phone '{phone_number}': {e}")
        return None

def get_active_premium_users() -> List[Dict[str, Any]]:
    """Pull all users eligible for automated generation (Premium/Pro logic)."""
    try:
        response = supabase.table('users').select('*').eq('is_active', True).in_('subscription_tier', ['premium', 'pro']).execute()
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch active premium users: {e}")
        return []

def log_interaction(user_id: str, message_type: str, content: str, intent: str = None, bot_response: str = None):
    """Keep an audit trail of conversations. Crucial for fine-tuning our ML models later."""
    try:
        data = {
            "user_id": user_id, 
            "message_type": message_type, 
            "content": content, 
            "detected_intent": intent, 
            "bot_response": bot_response
        }
        supabase.table('interactions').insert(data).execute()
    except Exception as e:
        logger.error(f"Failed to log interaction for user {user_id}: {e}")

def create_workout(user_id: str, plan_text: str):
    """Save the newly generated workout to the user's timeline."""
    try:
        data = {"user_id": user_id, "workout_plan": plan_text, "scheduled_date": "now()"}
        supabase.table('workouts').insert(data).execute()
    except Exception as e:
        logger.error(f"Failed to create workout for user {user_id}: {e}")

def update_workout_status(user_id: str, status: str, feedback: str = None):
    """Finds the user's pending workout for today and updates it according to their WhatsApp reply."""
    try:
        data = {"status": status}
        if feedback:
            data["feedback"] = feedback
        
        # We only update 'pending' workouts to avoid overwriting historical data
        supabase.table('workouts').update(data).eq('user_id', user_id).eq('status', 'pending').execute()
    except Exception as e:
        logger.error(f"Failed to update workout status to '{status}' for user {user_id}: {e}")

def create_diet_plan(user_id: str, plan_text: str, targets: dict):
    data = {
        "user_id": user_id,
        "daily_calories_target": targets.get("cals", 2000),
        "protein_g": targets.get("protein", 150),
        "carbs_g": targets.get("carbs", 200),
        "fats_g": targets.get("fats", 65),
        "meal_suggestions": plan_text,
        "scheduled_date": "now()"
    }
    supabase.table('diet_plans').insert(data).execute()
