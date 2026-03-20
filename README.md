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

## 🔄 Workflow & Usage
1. **Setup:** Select Team A and Team B with their respective formations.
2. **Analysis:** Generate the initial Match Analysis to see the automatically selected Starting XIs.
3. **Refinement:** Modify lineups by swapping player roles or making substitutions.
4. **Co-Creation:** Click **"Generate AI Tactical Plan"** to receive a structured game plan.
5. **Iteration:** Interact with the AI Coach via chat to ask specific questions or propose tactical shifts (e.g., "How should we adjust our high press?").

---


## 🛠️ Installation & Local Setup

Follow these steps to run **CO-FOOTBALL** on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.9** or higher installed. You can check your version by running: 
```bash
python --version
```

### 2. Get a Groq API Key

### 3. Clone & Install
Open your terminal and run:
```bash
# Clone the repository
git clone [https://github.com/Riky1411/CO-FOOTBALL.git](https://github.com/Riky1411/CO-FOOTBALL.git)

# Enter the project folder
cd CO-FOOTBALL

# Install all required libraries
pip install -r requirements.txt
```

### 4. Setting up the API Key
The application looks for an environment variable named GROQ_API_KEY

On Windows (Command Prompt): 
```cmd
set GROQ_API_KEY=your_api_key_here
```

PowerShell:
```bash
$env:GROQ_API_KEY="your_api_key_here"
```

On Mac/Linux:
```bash
export GROQ_API_KEY="your_api_key_here"
```

### 5. Run the App
Start the Streamlit interface: 
```bash
streamlit run app.py
```