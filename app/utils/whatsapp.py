import requests
from app.config import Config
from loguru import logger

def send_whatsapp_message(phone_number, message):
    url = Config.WHATSAPP_API_URL
    api_key = Config.WHATSAPP_API_KEY
    payload = {
        'phone_number': phone_number,
        'message': message
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"WhatsApp message sent to {phone_number}")
    except requests.RequestException as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
