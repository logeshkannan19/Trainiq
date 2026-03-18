# Trainiq Product Roadmap 🚀

This document outlines the strategic future of Trainiq. We are continuously building towards making Trainiq the most intelligent, autonomous fitness coach on WhatsApp.

## Phase 1: MVP Layer (Current)
- [x] Full n8n orchestration for core routines (Daily Workouts)
- [x] GPT-4 based intent detection (Skip, Reschedule, Done, General Chat)
- [x] Weekly PostgreSQL analytical aggregation
- [x] Whisper API voice note parsing
- [x] Premium Next.js admin instrumentation dashboard

## Phase 2: Scale & Memory (Q3 2026)
- [ ] **Vector Database Memory**: Move beyond exact relational queries to highly conversational memories using Pinecone. Trainiq will remember "You said your knee hurt 3 weeks ago" organically.
- [ ] **Multilingual Support**: Fully localize workouts and NLP routing for Spanish, Arabic, and Hindi.
- [ ] **Form Checking Vision**: Allow users to send video clips of their workouts, automatically routed to GPT-4o Vision for real-time form correction cues.

## Phase 3: Wearable Integration (Q4 2026)
- [ ] **Apple Health / Oura Sync**: Webhook integration to pull active caloric burn directly into the DB.
- [ ] **Biometric Rest Recommendations**: If HRV drops too low (via Oura), Trainiq preemptively texts the user to switch their heavy lifting day to an active recovery day.
- [ ] **Stripe Monetization & Tier Gating**: Fully automated billing webhooks dictating `free` vs `pro` prompt limits.
