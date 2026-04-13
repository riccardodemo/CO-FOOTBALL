# ⚽ CO-FOOTBALL: Co-Creative Tactical Analysis System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LLM](https://img.shields.io/badge/AI-Groq%20/%20LLaMA%203-orange.svg)](https://groq.com/)

**CO-FOOTBALL** is a **functional prototype** of an AI-powered interactive system designed to support football fans and tactical analysts in exploring match strategies through **Human-AI Collaboration**. 

The system leverages **EAFC 26 player data** as a rich proxy for real-world attributes to identify tactical mismatches, using a Large Language Model (LLM) as a "Co-Creative Coach" to help users build, refine, and iterate on a game plan.

---

## 🎓 Academic Context & Research
This project was developed for the **Computational Creativity** course during my Erasmus program at **Leiden University** (Netherlands). 

Unlike standard dashboards, CO-FOOTBALL is grounded in a "Mixed-Initiative" design philosophy, where the AI acts as a collaborator rather than a simple automation tool.

👉 **[Read the Full System Description Paper (PDF)](./docs/CO_FOOTBALL_paper.pdf)**

**Research Focus:**
- **Mismatch Logic:** Quantitative calculation of tactical advantages using player-level attributes.
- **Co-Creativity:** Enhancing human decision-making through AI-generated explanations.
- **User Agency:** Maintaining the human "in the loop" for final strategic choices.

---

## 📸 System Walkthrough
To see the system in action (UI layout, pitch visualization, and AI chat), please refer to the visual guide:

👉 **[Click here to view the Full Screenshots Walkthrough (PDF)](./docs/System_Screenshots_Walkthrough.pdf)**

---

## 🌟 Key Features
- **Dynamic Mismatch Engine:** A custom algorithm that analyzes player attributes (Speed, Height, Strength, etc.) to identify physical and positional advantages/disadvantages.
- **Interactive Lineup Management:** A Streamlit-based UI where users can select teams, swap player roles, and make substitutions with real-time updates.
- **Mixed-Initiative AI Coach:** Integrated with **LLaMA-3 (via Groq API)**. The AI coach is constrained to use only listed bench players and provides data-driven tactical reasoning.
- **Explainable AI (XAI):** The system doesn't just suggest a move; it explains *why* based on the underlying player statistics.

---

## 🛠️ Tech Stack & Data
- **Language:** Python 3.9+
- **Data Science:** Pandas, NumPy (Mismatch logic & data cleaning)
- **Visualization:** Matplotlib (Custom pitch rendering)
- **Generative AI:** Groq Cloud API (LLaMA-3 model)
- **Web App:** Streamlit
- **Dataset:** EA Sports FC 26 Player Database (Sourced from Kaggle)

---

## 📂 Project Structure

```text
CO-FOOTBALL/
├── app.py                  # Streamlit UI (entry point)
├── src/
│   ├── __init__.py
│   ├── config.py           # All constants, formations, team colors, LLM settings
│   └── core.py             # Lineup logic, mismatch engine, pitch drawing, LLM calls
├── data/
│   └── EAFC26-Men.csv      # EA FC 26 player dataset
├── docs/
│   ├── CO_FOOTBALL_paper.pdf
│   └── System_Screenshots_Walkthrough.pdf
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Workflow & Usage
1. **Setup:** Select Team A and Team B with their respective formations.
2. **Analysis:** Generate the initial Match Analysis to see the automatically selected Starting XIs.
3. **Refinement:** Modify lineups by swapping player roles or making substitutions.
4. **Co-Creation:** Click **"Generate AI Tactical Plan"** to receive a structured game plan.
5. **Iteration:** Interact with the AI Coach via chat to ask specific questions or propose tactical shifts (e.g., "How should we adjust our high press?").

---


## 🛠️ Installation & Local Setup

Follow these steps to run **CO-FOOTBALL** on your local machine.

### 1. Prerequisites

- **Python 3.9+** — check with `python --version`
- A free **Groq API Key** — sign up at [console.groq.com](https://console.groq.com/)

### 2. Clone & Install

```bash
# Clone the repository
git clone https://github.com/Riky1411/CO-FOOTBALL.git
cd CO-FOOTBALL

# (Recommended) Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set the API Key

The application needs the environment variable `GROQ_API_KEY`.

**Option A — `.env` file (recommended):**
Create a `.env` file in the project root (it is already in `.gitignore`):

```text
GROQ_API_KEY=your_api_key_here
```

Then install the helper package and it will be loaded automatically:

```bash
pip install python-dotenv
```

**Option B — Export directly in your terminal:**

```bash
# Windows (Command Prompt)
set GROQ_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY="your_api_key_here"

# Mac / Linux
export GROQ_API_KEY="your_api_key_here"
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.
