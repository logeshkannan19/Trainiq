import os
import json
import logging
from openai import OpenAI, OpenAIError

logger = logging.getLogger("Trainiq.AI")

# Default to a dummy key if not present during local setup
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY is missing! Calling OpenAI will fail.")
client = OpenAI(api_key=api_key or "dummy-key")

def load_prompt(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "..", "prompts", filename)
    with open(path, "r") as f:
        return f.read()

def detect_intent(message: str) -> dict:
    """
    Passes the raw message through our specialized Intent Pipeline.
    Strictly forces GPT-4 into a JSON output format for perfect routing.
    """
    try:
        prompt_template = load_prompt("intent-detector.md")
        system_prompt = prompt_template.replace("{user_message}", message).replace("{message_type}", "text")
        
        response = client.chat.completions.create(
            model="gpt-4o",  # gpt-4o gives us excellent balance of speed and reasoning
            messages=[{"role": "system", "content": system_prompt}],
            response_format={"type": "json_object"},
            temperature=0.1  # Low temp because classification needs to be deterministic
        )
        
        return json.loads(response.choices[0].message.content)
    except OpenAIError as e:
        logger.error(f"OpenAI Intent Detection failed: {e}")
        # Graceful fallback to prevent total system panic
        return {"intent": "general_chat", "fallback": True}
    except json.JSONDecodeError as e:
        logger.error(f"GPT returned malformed JSON: {e}")
        return {"intent": "general_chat", "fallback": True}

def generate_workout(user: dict, recent_feedback: str = "none") -> str:
    """
    The holy grail of Trainiq. Builds a personalized, physiologically sound workout routine.
    Takes into account the user's specific goals and their most recent feedback constraints.
    """
    try:
        prompt_template = load_prompt("workout-generator.md")
        system_prompt = prompt_template.replace("{user_name}", user.get("full_name", "Athlete")) \
                                       .replace("{fitness_goal}", user.get("fitness_goal", "maintain")) \
                                       .replace("{experience_level}", user.get("experience_level", "intermediate")) \
                                       .replace("{recent_feedback}", recent_feedback)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7  # A bit of creativity for varied workouts
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Failed to generate workout: {e}")
        return "Hey! Trainiq's brain is taking a quick breather. Let's stick to 3x10 Pushups and bodyweight squats today. 💪"

def process_voice_note(transcript: str) -> dict:
    prompt_template = load_prompt("voice-assistant.md")
    system_prompt = prompt_template.replace("{whisper_transcript}", transcript)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
