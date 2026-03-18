# CO-FOOTBALL ⚽🤖
### Co-Creative AI System for Football Tactical Analysis

CO-FOOTBALL is an interactive system that enables users to explore football tactics through **data-driven analysis** and **human–AI collaboration**.

The system combines:
- Player-level data analysis
- Tactical mismatch detection
- Interactive visualizations
- A conversational AI assistant

to support realistic and explainable tactical decision-making.

---

## 📸 Demo / Preview

To quickly understand how the system works, check the visual walkthrough:

👉 **[Click here to view the full System Walkthrough (PDF)](./System_Screenshots_Walkthrough.pdf)**

The PDF includes:
- Team and formation selection
- Dynamic pitch visualization
- Lineup editing (substitutions & swaps)
- Mismatch detection
- AI-generated tactical plans
- Interactive dialogue with the AI coach

---

## 🚀 Project Overview

Modern football tactics are complex and highly dependent on player attributes and matchups.

CO-FOOTBALL helps users:
- Analyze **player mismatches** using data
- Experiment with **formations and lineups**
- Receive **AI-generated tactical suggestions**
- Iteratively refine strategies through **natural language interaction**

Unlike standard recommendation systems, CO-FOOTBALL follows a **mixed-initiative approach**, where:
- The user drives the decision-making
- The AI supports reasoning and explanation

---

## ⚙️ Features

- ⚽ **Mismatch Analysis**  
  Detects player-level and positional advantages using aggregated metrics (speed, physicality, aerial ability, etc.)

- 📊 **Data-Driven Modeling**  
  Uses structured player attributes to support tactical reasoning

- 🧠 **AI Tactical Assistant**  
  LLM-based assistant that generates and explains tactical plans

- 🎨 **Interactive Visualization**  
  Real-time formation rendering and lineup updates

- 🔄 **Co-Creative Interaction**  
  Iterative human-AI collaboration through conversation

---

## 🧰 Tech Stack

- **Python**
- **Streamlit** (frontend)
- **Pandas / NumPy** (data processing)
- **Matplotlib** (visualization)
- **Groq API (LLM)** (AI assistant)

---

## 📊 Data

Player data is sourced from the EA Sports FC dataset (Kaggle), which provides structured attributes such as:

- Speed
- Physicality
- Aerial ability
- Positional roles

This enables quantitative and interpretable tactical analysis.

---

## 🖥️ Installation

```bash
git clone <your-repo-link>
cd co-football
pip install -r requirements.txt
