import os
import logging
import requests

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        
        if not self.phone_number_id or not self.access_token:
            logger.warning("WhatsApp credentials not configured - messages will be logged only")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
    
    def send_message(self, to: str, message: str) -> bool:
        """Send WhatsApp message"""
        if self.mock_mode:
            logger.info(f"Mock: Sending to {to}: {message[:50]}...")
            return True
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Message sent to {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def send_workout(self, to: str, workout: dict) -> bool:
        """Send formatted workout message"""
        exercises = workout.get("exercises", [])
        message = f"🏋️ *{workout.get('name', 'Workout')}*\n\n"
        
        for i, ex in enumerate(exercises, 1):
            message += f"{i}. {ex['name']} - {ex['sets']}x{ex['reps']}\n"
        
        message += f"\n⏱️ Duration: ~{workout.get('duration_minutes', 30)} mins"
        
        return self.send_message(to, message)
    
    def send_daily_reminder(self, to: str) -> bool:
        """Send daily workout reminder"""
        message = "🌅 Good morning! Your daily workout is ready.\n\nType 'workout' to get your personalized routine for today!"
        return self.send_message(to, message)
