-- Trainiq Fit: Seed Data for Testing

-- Insert a Free User
INSERT INTO public.users (id, phone_number, full_name, current_weight_kg, target_weight_kg, fitness_goal, experience_level, subscription_tier, timezone)
VALUES 
('d1f9c3b8-6b8c-44e2-a0e2-2a9f4c8b2d10', '+12345678901', 'Alice Free', 70.0, 65.0, 'cut', 'beginner', 'free', 'America/New_York');

-- Insert a Premium User
INSERT INTO public.users (id, phone_number, full_name, current_weight_kg, target_weight_kg, fitness_goal, experience_level, subscription_tier, timezone)
VALUES 
('f4b3a2c1-8d9e-11ec-b909-0242ac120002', '+19876543210', 'Bob Premium', 85.0, 95.0, 'bulk', 'intermediate', 'premium', 'Europe/London');

-- Insert a recent completed workout for Bob
INSERT INTO public.workouts (user_id, scheduled_date, workout_plan, status, feedback, calories_burned, completed_at)
VALUES 
('f4b3a2c1-8d9e-11ec-b909-0242ac120002', CURRENT_DATE - INTERVAL '1 day', 'Chest & Triceps\n- Bench Press: 4x8\n- Incline Dumbbell Press: 3x10\n- Tricep Pushdowns: 3x15\n- Overhead Extensions: 3x12', 'completed', 'perfect', 450, CURRENT_TIMESTAMP - INTERVAL '1 day');

-- Insert a pending diet plan for Alice
INSERT INTO public.diet_plans (user_id, scheduled_date, daily_calories_target, protein_g, carbs_g, fats_g, meal_suggestions)
VALUES 
('d1f9c3b8-6b8c-44e2-a0e2-2a9f4c8b2d10', CURRENT_DATE, 1800, 140, 150, 60, 'Breakfast: Oatmeal with protein powder (400 kcal)\nLunch: Grilled chicken salad (500 kcal)\nDinner: Salmon with sweet potato (700 kcal)\nSnack: Greek yogurt (200 kcal)');

-- Insert interaction logs
INSERT INTO public.interactions (user_id, message_type, content, detected_intent, bot_response)
VALUES 
('f4b3a2c1-8d9e-11ec-b909-0242ac120002', 'text', 'Done with my workout!', 'mark_done', 'Great job Bob! I have logged your workout. How did it feel? Reply with Easy, Perfect, or Hard.');
