# Contributing to Trainiq 🏋️‍♂️

First off, thank you for considering contributing to Trainiq! It's people like you that make Trainiq such a powerful fitness AI coach. 

## 🧠 Approach to Development

We believe in **clean, robust, and highly scalable** code.
Since our backend relies heavily on n8n graphical orchestration and strict OpenAI JSON enforcement, we expect contributors to test their workflow modifications carefully before submitting PRs.

## 🛠️ How to Contribute

1. **Fork** the repository via GitHub.
2. **Clone** your fork locally.
3. **Install Dependencies** for the dashboard component:
   ```bash
   cd dashboard
   npm install
   ```
4. **Create a Branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `fix/your-fix-name`.
5. **Test Your Workflows**: If modifying JSON n8n definitions, please test them inside your local n8n instance and export them cleanly without your personal credentials attached.
6. **Commit** your changes following conventional commits architecture (e.g. `feat: add whisper parsing for french accents`).
7. **Push** and create a **Pull Request**.

## 🐛 Bug Reports

If you find a bug in the code or a hallucination in the system prompts, please open an Issue with:
- The exact raw text that caused the failure.
- Expected behavior vs Actual behavior.
- Screenshots if applicable.

Welcome to the team!
