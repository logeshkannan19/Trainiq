# Trainiq Fit Backend

FastAPI backend for Trainiq Fit - AI-powered fitness coach on WhatsApp.

## 🚀 Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Click the button above
2. Connect GitHub and select this repo
3. Add environment variables from `.env.example`
4. Deploy!

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your credentials

# Run server
uvicorn main:app --reload
```

## 📱 WhatsApp Setup

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create WhatsApp Business app
3. Get your Phone Number ID and Access Token
4. Set webhook URL: `https://your-domain.com/webhook`
5. Set verify token in environment variables

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon key |
| `OPENAI_API_KEY` | OpenAI API key |
| `WHATSAPP_VERIFY_TOKEN` | Webhook verification token |
| `WHATSAPP_ACCESS_TOKEN` | Meta access token |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp phone ID |
| `PORT` | Server port (default: 8000) |

## 🌐 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /webhook` - WhatsApp webhook verification
- `POST /webhook` - Receive WhatsApp messages

## 🤖 Features

- AI-powered intent detection
- Personalized workout generation
- Diet plan recommendations
- Daily workout reminders (7 AM)
- Weekly progress reports
- Natural language understanding
