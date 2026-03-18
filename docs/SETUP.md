# Trainiq Setup Guide

To deploy this pure Python project from scratch, follow these instructions:

## Part 1: Database Setup (Supabase)
1. Go to the Supabase SQL Editor and paste `database/schema.sql`.
2. Grab your `SUPABASE_URL` and `SUPABASE_KEY`.

## Part 2: Environment Variables
Create a `.env` file in the root with:
```env
SUPABASE_URL=...
SUPABASE_KEY=...
OPENAI_API_KEY=...
META_API_TOKEN=...
PHONE_NUMBER_ID=...
```

## Part 3: Running the Backend
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI Webhook Server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
4. In a separate terminal, start the Background Scheduler:
   ```bash
   python src/scheduler.py
   ```

## Part 4: Running the Streamlit Dashboard
1. In a split terminal, run:
   ```bash
   streamlit run admin-panel/app.py
   ```
2. Navigate to `http://localhost:8501`.
