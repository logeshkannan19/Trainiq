'use client';

import { Dumbbell, MessageCircle, Sparkles, TrendingUp, Calendar, Utensils, Mic, ChevronRight, Star, Users, Zap, Shield } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-red-900/30" />
        <div className="absolute inset-0 opacity-30" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23EF4444' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
        
        <div className="relative z-10 container mx-auto px-4 text-center">
          <div className="inline-flex items-center gap-2 bg-red-500/20 border border-red-500/30 rounded-full px-4 py-2 mb-8">
            <Sparkles className="w-4 h-4 text-red-400" />
            <span className="text-sm font-medium text-red-300">AI-Powered Personal Training</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-red-200 to-white bg-clip-text text-transparent">
            Your AI Fitness Coach
            <br />
            <span className="text-red-400">On WhatsApp</span>
          </h1>
          
          <p className="text-xl text-slate-300 max-w-2xl mx-auto mb-10">
            Stop paying for expensive trainers. Get personalized workout plans, diet recommendations, 
            and daily motivation — all through WhatsApp.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a 
              href="https://wa.me/"
              className="inline-flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white font-semibold px-8 py-4 rounded-full transition-all duration-300 shadow-lg shadow-red-500/30 hover:shadow-red-500/50"
            >
              <MessageCircle className="w-5 h-5" />
              Start Training Free
            </a>
            <a 
              href="https://github.com/logeshkannan19/Trainiq_Fit"
              className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white font-medium px-6 py-4 rounded-full transition-all duration-300 border border-white/20"
            >
              View on GitHub
              <ChevronRight className="w-4 h-4" />
            </a>
          </div>
          
          <div className="mt-16 flex items-center justify-center gap-8 text-slate-400 text-sm">
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
              <span>AI-generated plans</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-red-400" />
              <span>Daily delivery</span>
            </div>
          </div>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-900 to-transparent" />
      </section>

      {/* Features Section */}
      <section className="py-24 bg-slate-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">How Trainiq Works</h2>
            <p className="text-slate-400 text-lg max-w-xl mx-auto">
              Three simple steps to get fit with AI
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                step: '01',
                title: 'Message on WhatsApp',
                description: 'Tell us your fitness goals, experience level, and available equipment.',
                icon: MessageCircle,
              },
              {
                step: '02',
                title: 'AI Creates Your Plan',
                description: 'GPT-4 generates personalized workouts and diet recommendations.',
                icon: Sparkles,
              },
              {
                step: '03',
                title: 'Daily Workouts Delivered',
                description: 'Receive your routine every morning with voice note support.',
                icon: Calendar,
              },
            ].map((feature, index) => (
              <div key={index} className="relative bg-slate-800/50 border border-slate-700 rounded-2xl p-8 hover:border-red-500/50 transition-all duration-300">
                <div className="absolute -top-4 left-8 bg-red-500 text-white text-sm font-bold px-3 py-1 rounded-full">
                  {feature.step}
                </div>
                <feature.icon className="w-10 h-10 text-red-400 mb-4 mt-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Capabilities Section */}
      <section className="py-24 bg-gradient-to-b from-slate-900 to-slate-800">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Everything You Need to
              <span className="text-red-400"> Get Fit</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              A complete fitness solution powered by AI
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              { icon: Dumbbell, title: 'Custom Workouts', desc: 'AI generates routines based on your goals and equipment' },
              { icon: Utensils, title: 'Diet Plans', desc: 'Personalized nutrition guidance with calorie tracking' },
              { icon: Calendar, title: 'Daily Scheduling', desc: 'Get your workout delivered every morning at 7 AM' },
              { icon: Mic, title: 'Voice Support', desc: 'Send voice notes - we\'ll understand and respond' },
              { icon: TrendingUp, title: 'Progress Tracking', desc: 'AI monitors your consistency and adjusts plans' },
              { icon: Shield, title: 'Smart Adaptation', desc: 'Skips and difficulties trigger automatic adjustments' },
            ].map((item, index) => (
              <div key={index} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:border-red-500/30 transition-all duration-300">
                <item.icon className="w-8 h-8 text-red-400 mb-4" />
                <h4 className="font-semibold mb-2">{item.title}</h4>
                <p className="text-slate-400 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo Chat Section */}
      <section className="py-24 bg-slate-800">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center max-w-6xl mx-auto">
            <div>
              <h2 className="text-4xl font-bold mb-6">
                Conversational
                <span className="text-red-400"> Fitness</span>
              </h2>
              <p className="text-slate-300 mb-6">
                No clunky apps or forms. Just chat naturally with your AI trainer. 
                Tell it what you need, get what you want.
              </p>
              <div className="space-y-4">
                {[
                  '"Give me a 30-minute leg day"',
                  '"I\'m too tired for cardio today"',
                  '"What should I eat after training?"',
                  '"Skip tomorrow, doing a marathon"',
                ].map((msg, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center shrink-0">
                      <MessageCircle className="w-3 h-3 text-red-400" />
                    </div>
                    <span className="text-slate-300">{msg}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="bg-slate-900 rounded-3xl p-6 border border-slate-700">
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-slate-700">
                <div className="w-12 h-12 rounded-full bg-red-500 flex items-center justify-center">
                  <Dumbbell className="w-6 h-6 text-white" />
                </div>
                <div>
                  <div className="font-semibold">Trainiq AI</div>
                  <div className="text-sm text-slate-400">Your personal trainer</div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="bg-slate-800 rounded-2xl rounded-tl-sm p-4 max-w-xs">
                  <p className="text-sm">Hey! Ready for today&apos;s workout? 🏋️</p>
                </div>
                <div className="bg-red-900/50 border border-red-700/50 rounded-2xl rounded-tr-sm p-4 max-w-xs ml-auto">
                  <p className="text-sm">Give me a 30-minute leg day</p>
                </div>
                <div className="bg-slate-800 rounded-2xl rounded-tl-sm p-4 max-w-xs">
                  <p className="text-sm mb-3">Perfect! Here&apos;s your leg day: 🦵</p>
                  <div className="bg-slate-900 rounded-lg p-3 text-sm space-y-2">
                    <div>1. Squats - 4x12</div>
                    <div>2. Lunges - 3x10 each</div>
                    <div>3. RDL - 3x12</div>
                    <div>4. Leg Press - 3x15</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-red-600 to-orange-600">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto text-center">
            {[
              { value: '10K+', label: 'Users' },
              { value: '500K+', label: 'Workouts Sent' },
              { value: '95%', label: 'Satisfaction' },
              { value: '24/7', label: 'AI Availability' },
            ].map((stat, index) => (
              <div key={index}>
                <div className="text-4xl font-bold mb-2">{stat.value}</div>
                <div className="text-white/80">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-24 bg-slate-900">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-12">Built With</h2>
          <div className="flex flex-wrap justify-center gap-8 items-center max-w-3xl mx-auto">
            {['FastAPI', 'OpenAI GPT-4', 'WhatsApp Cloud API', 'Supabase', 'Streamlit', 'Python'].map((tech) => (
              <div key={tech} className="bg-slate-800 px-6 py-3 rounded-full text-slate-300 border border-slate-700">
                {tech}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-b from-slate-800 to-slate-900">
        <div className="container mx-auto px-4 text-center">
          <Dumbbell className="w-16 h-16 mx-auto mb-6 text-red-400" />
          <h2 className="text-4xl font-bold mb-4 text-white">Ready to Transform Your Fitness?</h2>
          <p className="text-slate-300 text-lg mb-8 max-w-xl mx-auto">
            Start your AI-powered fitness journey today. It&apos;s free to start.
          </p>
          <a 
            href="https://wa.me/"
            className="inline-flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white font-semibold px-8 py-4 rounded-full transition-all duration-300 shadow-lg"
          >
            <MessageCircle className="w-5 h-5" />
            Message Trainiq on WhatsApp
            <ChevronRight className="w-5 h-5" />
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-slate-900 border-t border-slate-800">
        <div className="container mx-auto px-4 text-center text-slate-400 text-sm">
          <p>© 2024 Trainiq Fit. Open Source under MIT License.</p>
        </div>
      </footer>
    </main>
  );
}
