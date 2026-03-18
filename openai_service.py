import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            logger.warning("OpenAI API key not configured - using mock responses")
            self.client = None
            self.mock_mode = True
        else:
            self.client = OpenAI(api_key=api_key)
            self.mock_mode = False
    
    def detect_intent(self, message: str) -> Dict[str, Any]:
        """Detect user intent from message"""
        if self.mock_mode:
            return self._mock_intent_detection(message)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a fitness intent detector. Analyze the user message and return JSON:
                {"type": "workout_request|skip|done|diet_request|question|greeting", "params": {specific params}}
                
                Types:
                - workout_request: user wants a workout (include duration, muscle_group if specified)
                - skip: user wants to skip
                - done: user completed workout
                - diet_request: user wants diet/nutrition info
                - question: user has a question
                - greeting: user is saying hello"""},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _mock_intent_detection(self, message: str) -> Dict[str, Any]:
        """Mock intent detection for testing"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ["workout", "exercise", "train", "gym"]):
            return {"type": "workout_request", "params": {"duration": 30}}
        elif any(word in msg_lower for word in ["skip", "can't", "tired", "rest"]):
            return {"type": "skip", "params": {}}
        elif any(word in msg_lower for word in ["done", "finished", "completed"]):
            return {"type": "done", "params": {}}
        elif any(word in msg_lower for word in ["eat", "diet", "food", "nutrition", "calories"]):
            return {"type": "diet_request", "params": {}}
        elif any(word in msg_lower for word in ["hi", "hello", "hey", "help"]):
            return {"type": "greeting", "params": {}}
        else:
            return {"type": "question", "params": {}}
    
    def generate_workout(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workout plan"""
        if self.mock_mode:
            return self._mock_workout(params)
        
        duration = params.get("duration", 30)
        muscle_group = params.get("muscle_group", "full body")
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Generate a workout plan in JSON format:
                {"name": "Workout Name", "exercises": [{"name": "Exercise", "sets": 3, "reps": 10, "rest": "60s"}], "duration_minutes": 30, "calories": 200}
                Include 4-6 exercises suitable for the requested workout."""},
                {"role": "user", "content": f"Generate a {duration} minute {muscle_group} workout"}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _mock_workout(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock workout for testing"""
        return {
            "name": "Full Body Blast",
            "exercises": [
                {"name": "Push-ups", "sets": 3, "reps": 12, "rest": "60s"},
                {"name": "Squats", "sets": 3, "reps": 15, "rest": "60s"},
                {"name": "Lunges", "sets": 3, "reps": 10, "rest": "45s"},
                {"name": "Plank", "sets": 3, "reps": 30, "rest": "30s"},
                {"name": "Dumbbell Rows", "sets": 3, "reps": 12, "rest": "60s"},
            ],
            "duration_minutes": params.get("duration", 30),
            "calories": 250
        }
    
    def generate_diet_plan(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diet plan"""
        if self.mock_mode:
            return self._mock_diet_plan()
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Generate a diet plan in JSON format:
                {"name": "Plan Name", "meals": [{"time": "Breakfast", "food": "Oatmeal with berries"}], "calories": 2000}
                Include 4-5 meals."""},
                {"role": "user", "content": "Generate a healthy diet plan"}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _mock_diet_plan(self) -> Dict[str, Any]:
        """Mock diet plan for testing"""
        return {
            "name": "Daily Nutrition Plan",
            "meals": [
                {"time": "Breakfast", "food": "Oatmeal with berries and honey"},
                {"time": "Lunch", "food": "Grilled chicken with quinoa and vegetables"},
                {"time": "Snack", "food": "Greek yogurt with almonds"},
                {"time": "Dinner", "food": "Salmon with sweet potato and broccoli"},
            ],
            "calories": 2100
        }
    
    def answer_fitness_question(self, question: str) -> str:
        """Answer fitness questions"""
        if self.mock_mode:
            return "I'm a fitness AI assistant. Ask me about workouts, diet, or training tips! 💪"
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful fitness coach. Give concise, encouraging answers."},
                {"role": "user", "content": question}
            ]
        )
        
        return response.choices[0].message.content
