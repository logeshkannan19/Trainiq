# Trainiq Architecture Guide

## System Overview
Trainiq is orchestrated via a pure **Python stack**, backed by PostgreSQL (Supabase) for durable state and metrics, and powered by OpenAI for cognitive tasks (generation, NLP routing). The delivery channel is WhatsApp via the official Meta Cloud API.

### 1. Webhook Intent Routing (FastAPI)
Whenever a user messages WhatsApp, the Meta Webhook pushes the event to our FastAPI endpoint (`src/main.py`).
1. The message string is sent to the `openai_service` with an Intent Detection prompt.
2. OpenAI replies with strict JSON denoting intent (e.g., `mark_done`, `skip`).
3. The FASTAPI server routes execution based on the intent.
4. Database state (`database.py`) is updated, and a follow-up action fires back to Meta.

### 2. Multi-Modal Interactions
We support Voice Notes natively:
- **Audio**: Extracted from WhatsApp, sent to `OpenAI Whisper` for transcription, then the text flows into the Intent Router.

### 3. Background Jobs (APScheduler)
Instead of n8n, we use `src/scheduler.py` via `APScheduler`:
- 7 AM: Iterates all premium users to generate personalized daily workouts.
- 8 AM: Generates personalized dietary macros.

### 4. Admin Dashboard (Streamlit)
The `/admin-panel/app.py` script serves a fast, data-rich analytical dashboard.
