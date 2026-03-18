import os
import logging
import requests

logger = logging.getLogger("Trainiq.WhatsApp")

META_API_TOKEN = os.getenv("META_API_TOKEN", "dummy_token")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "dummy_id")

def send_whatsapp_message(to_phone: str, message_text: str):
    """
    Pushes a payload out to the Meta Cloud API.
    A crucial outbound pipeline; must fail gracefully without bringing down down main loop.
    """
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {META_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    
    try:
        # Note: 5s timeout limits latency cascading if Meta experiences an outage
        response = requests.post(url, json=payload, headers=headers, timeout=5.0)
        response.raise_for_status()
        logger.debug(f"Successfully dispatched message to {to_phone}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"WhatsApp API transmission failed: {e}")
        return {"error": str(e)}
