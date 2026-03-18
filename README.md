# Trainiq Fit – AI Fitness Coach 🏋️‍♂️

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> [!NOTE]
> **Demo:** [trainiq-fit-landing.vercel.app](https://trainiq-fit-landing.vercel.app)

Trainiq Fit is a production-ready MVP for a WhatsApp-based AI Personal Trainer. It leverages a modern Python architecture (FastAPI, APScheduler, Streamlit), OpenAI for intelligent generation and intent detection, and PostgreSQL (Supabase) for scalable tracking.

## 🌟 Core Features

| Feature | Description |
|---------|-------------|
| 🤖 **Automated Morning Workouts** | Daily AI-generated routines delivered to WhatsApp at 7 AM |
| 💬 **Natural Language Intent** | Understands "Done", "Skip", "Change to legs" |
| 🔄 **Dynamic Adjustments** | Adapts if user skips too much or finds routines too hard |
| 🥗 **Dietary Recommendations** | AI nutritional coach tailored to calories and macros |
| 🎤 **Voice Support** | Send voice notes directly to Trainiq |

## 🏗️ Architecture Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **API** | FastAPI | High-throughput webhook routing |
| **Scheduler** | APScheduler | Daily workout generation |
| **AI** | OpenAI GPT-4 + Whisper | Intent detection, workout generation |
| **Dashboard** | Streamlit | Admin monitoring panel |
| **Database** | Supabase PostgreSQL | User data, workout history |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Supabase account
- OpenAI API key
- WhatsApp Business account
- Streamlit Cloud (for admin panel)

### Installation

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/Trainiq_Fit.git
cd Trainiq_Fit

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Configure environment variables
# See docs/SETUP.md for details

# Start the API server
uvicorn src.main:app --reload

# Start admin dashboard (separate terminal)
cd admin-panel && streamlit run app.py
```

## 🗂️ Directory Structure

```
Trainiq_Fit/
├── src/                    # Python backend
│   ├── main.py           # FastAPI application
│   ├── database.py       # Supabase integration
│   ├── openai_service.py # AI service layer
│   ├── scheduler.py      # APScheduler jobs
│   └── whatsapp_service.py
├── admin-panel/           # Streamlit dashboard
│   └── app.py
├── database/              # SQL schemas
├── prompts/               # OpenAI system prompts
├── docs/                  # Documentation
└── requirements.txt
```

## 📱 WhatsApp Integration

Trainiq connects to WhatsApp Cloud API for seamless user communication.

**Webhook Setup:**
- Callback URL: `https://your-domain.com/webhook`
- Verify Token: Configured in environment

## 🔧 Configuration

Required environment variables:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `WHATSAPP_VERIFY_TOKEN` | Webhook verification |
| `WHATSAPP_ACCESS_TOKEN` | Meta access token |

See [`docs/SETUP.md`](docs/SETUP.md) for detailed setup instructions.

## 📚 Documentation

- [`docs/SETUP.md`](docs/SETUP.md) - Step-by-step deployment guide
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - System architecture deep dive

## 🤝 Contributing

Contributions welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting PRs.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
