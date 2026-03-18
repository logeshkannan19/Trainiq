/**
 * Trainiq Fit: Core Database Schema (Supabase/PostgreSQL)
 * 
 * Defines the relational models for the Trainiq AI pipeline:
 * - Users: Stores profile constraints (weight, goals, experience tier).
 * - Workouts: Daily generated programs triggered via n8n cron node.
 * - Diet Plans: Macro-specific generated payload via ChatGPT.
 * - Interactions: AI intent router audit logs.
 */

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    current_weight_kg DECIMAL(5,2),
    target_weight_kg DECIMAL(5,2),
    fitness_goal VARCHAR(20) CHECK (fitness_goal IN ('cut', 'bulk', 'maintain')),
    experience_level VARCHAR(20) CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
    subscription_tier VARCHAR(20) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'premium', 'pro')),
    preferred_workout_time TIME DEFAULT '07:00:00',
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Workouts Table
CREATE TABLE public.workouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    scheduled_date DATE NOT NULL,
    workout_plan TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'skipped')),
    feedback VARCHAR(20) CHECK (feedback IN ('easy', 'perfect', 'hard')),
    calories_burned INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Diet Plans Table
CREATE TABLE public.diet_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    scheduled_date DATE NOT NULL,
    daily_calories_target INTEGER NOT NULL,
    protein_g INTEGER NOT NULL,
    carbs_g INTEGER NOT NULL,
    fats_g INTEGER NOT NULL,
    meal_suggestions TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Interactions Log (For AI context and intent training)
CREATE TABLE public.interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    message_type VARCHAR(20) CHECK (message_type IN ('text', 'audio', 'image')),
    content TEXT NOT NULL,
    detected_intent VARCHAR(50),
    bot_response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Create indexes for performance
CREATE INDEX idx_users_phone ON public.users(phone_number);
CREATE INDEX idx_workouts_user_date ON public.workouts(user_id, scheduled_date);
CREATE INDEX idx_interactions_user ON public.interactions(user_id);
