import os
import logging
from typing import Optional, Dict, Any
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            logger.warning("Supabase credentials not configured - using mock mode")
            self.client = None
            self.mock_mode = True
        else:
            self.client: Client = create_client(self.url, self.key)
            self.mock_mode = False
    
    def get_or_create_user(self, phone: str) -> Dict[str, Any]:
        """Get or create user by phone"""
        if self.mock_mode:
            return {"id": "mock_user", "phone": phone}
        
        response = self.client.table("users").select("*").eq("phone", phone).execute()
        
        if response.data:
            return response.data[0]
        
        response = self.client.table("users").insert({
            "phone": phone,
            "created_at": "now()"
        }).execute()
        
        return response.data[0]
    
    def save_workout(self, user_id: str, workout: Dict[str, Any]):
        """Save workout to history"""
        if self.mock_mode:
            logger.info(f"Mock: Saving workout for user {user_id}")
            return
        
        self.client.table("workouts").insert({
            "user_id": user_id,
            "workout_data": workout,
            "completed": False
        }).execute()
    
    def log_completion(self, user_id: str):
        """Log workout completion"""
        if self.mock_mode:
            logger.info(f"Mock: Logging completion for user {user_id}")
            return
        
        response = self.client.table("workouts").select("id").eq("user_id", user_id).eq("completed", False).order("created_at", desc=True).limit(1).execute()
        
        if response.data:
            self.client.table("workouts").update({"completed": True}).eq("id", response.data[0]["id"]).execute()
    
    def log_skip(self, user_id: str):
        """Log workout skip"""
        if self.mock_mode:
            logger.info(f"Mock: Logging skip for user {user_id}")
            return
        
        response = self.client.table("workouts").select("id").eq("user_id", user_id).eq("completed", False).order("created_at", desc=True).limit(1).execute()
        
        if response.data:
            self.client.table("workouts").update({"skipped": True}).eq("id", response.data[0]["id"]).execute()
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        if self.mock_mode:
            return {"total_workouts": 0, "completed": 0, "skipped": 0}
        
        workouts = self.client.table("workouts").select("*").eq("user_id", user_id).execute()
        
        return {
            "total_workouts": len(workouts.data),
            "completed": sum(1 for w in workouts.data if w.get("completed")),
            "skipped": sum(1 for w in workouts.data if w.get("skipped"))
        }
