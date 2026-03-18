import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import database as db
import openai_service as ai
import whatsapp_service as wa

# Configure professional stdout logging for container orchestration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("Trainiq.Scheduler")

def daily_workout_job():
    """
    Wakes up every day at 7 AM. 
    Loops over all premium subscribers and generates a unique, tailored workout based on their specific DB profile constraints.
    """
    logger.info("Initializing Daily Workout Generation Sequence...")
    users = db.get_active_premium_users()
    
    if not users:
        logger.warning("No active premium users found. Sleeping.")
        return
        
    for user in users:
        try:
            logger.debug(f"Processing athlete: {user['full_name']}")
            workout = ai.generate_workout(user)
            db.create_workout(user["id"], workout)
            wa.send_whatsapp_message(user["phone_number"], workout)
            logger.info(f"✅ Dispatched daily workout to {user['full_name']}")
        except Exception as e:
            # We catch exceptions PER USER so one failure doesn't crash the entire morning loop
            logger.error(f"❌ Critical failure processing athlete {user['full_name']}: {e}", exc_info=True)

def daily_diet_job():
    logging.info("Triggered Daily Diet Job")
    users = db.get_active_premium_users()
    for user in users:
        try:
            # Simple AI prompt target calculation dict
            targets = {"cals": float(user.get("current_weight_kg", 80)) * 24}
            # Simplified for brevity - generate diet via gpt
            bot_response = "Here are your suggested meals for today based on your weight..."
            wa.send_whatsapp_message(user["phone_number"], bot_response)
        except Exception as e:
            logging.error(f"Failed diet job for {user['full_name']}: {e}")

def weekly_report_job():
    logging.info("Triggered Weekly Report Job")
    users = db.get_active_premium_users()
    for user in users:
        # DB logic to aggregate last 7 days goes here
        wa.send_whatsapp_message(user["phone_number"], "📊 Your Weekly Trainiq Report:\nAwesome work this week!")

def job_listener(event):
    """Fallback audit for cron-level exceptions."""
    if event.exception:
        logger.error(f"Job {event.job_id} crashed entirely: {event.exception}")
    else:
        logger.debug(f"Job {event.job_id} executed gracefully.")

if __name__ == "__main__":
    logger.info("Starting Trainiq background scheduler... 🚀")
    scheduler = BlockingScheduler()
    scheduler.add_listener(job_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
    
    # Core Routines mapped to UTC/System time. In prod, configure specific Timezones.
    # 7 AM: Morning Workout Push
    scheduler.add_job(daily_workout_job, 'cron', hour=7, minute=0, id='morning_workout_push')
    
    # 8 AM: Dietary Macros Push
    scheduler.add_job(daily_diet_job, 'cron', hour=8, minute=0, id='morning_diet_push')
    
    # Sunday 9 AM: Progress Recap
    scheduler.add_job(weekly_report_job, 'cron', day_of_week='sun', hour=9, minute=0, id='weekly_digest_push')
    
    logger.info("All chron tasks successfully registered. Waiting for trigger event...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Gracefully shutting down scheduler. Catch you later!")

