Below is the **complete README text**.
You can **copy & paste it directly** into a `README.txt` file.

```
CO-FOOTBALL — Co-Creative Tactical Football Analysis System
===========================================================

This repository contains the implementation of **CO-FOOTBALL**, a co-creative
interactive system designed to support football tactical analysis through
human–AI collaboration.

The system allows users to explore matchups, modify lineups, identify on-field
mismatches, and iteratively co-create tactical plans together with an AI coach.


----------------------------------------------------------------
1. System Walkthrough (Screenshots PDF)
----------------------------------------------------------------

To quickly understand how the system works without running the code, please
refer to the following file:

    System_Screenshots_Walkthrough.pdf

This PDF contains a step-by-step visual walkthrough of a real usage scenario,
including:

- Initial application layout
- Team and formation selection
- Dynamic formation visualization
- Lineup editing (swaps and substitutions)
- Physical and positional mismatch detection
- AI-generated tactical game plan
- Interactive dialogue with the AI coach
- Iterative refinement of tactics through user feedback

The PDF is intended to give an immediate and concrete example of how the
co-creative system behaves in practice.


----------------------------------------------------------------
2. Setting the Groq API Key
----------------------------------------------------------------

The AI coach is powered by a Large Language Model accessed via **Groq API**.
To run the application, you must set a valid Groq API key as an environment
variable.

Steps:

1. Create a Groq account and obtain an API key from:
   https://console.groq.com/

2. Set the environment variable **GROQ_API_KEY**.

On macOS / Linux (terminal):
------------------------------------------------
export GROQ_API_KEY="your_api_key_here"
------------------------------------------------

On Windows (PowerShell):
------------------------------------------------
setx GROQ_API_KEY "your_api_key_here"
------------------------------------------------

After setting the key, restart the terminal so the variable is available
to Python.

⚠️ Important:
- Do NOT hard-code the API key inside the source files.
- The application will raise an error if the key is not set.


----------------------------------------------------------------
3. System Requirements
----------------------------------------------------------------

Software requirements:

- Python 3.9 or higher
- pip (Python package manager)

Required Python libraries:

- streamlit
- pandas
- numpy
- matplotlib
- groq

You can install the dependencies with:

------------------------------------------------
pip install streamlit pandas numpy matplotlib groq
------------------------------------------------


----------------------------------------------------------------
4. How to Run the Application
----------------------------------------------------------------

1. Make sure the following files are in the same directory:
   - app.py
   - core.py
   - EAFC26-Men.csv
   - System_Screenshots_Walkthrough.pdf

2. Open a terminal in that directory.

3. Run the Streamlit application:
------------------------------------------------
streamlit run app.py
------------------------------------------------

4. The application will open automatically in your web browser.


----------------------------------------------------------------
5. How to Use the App
----------------------------------------------------------------

Basic workflow:

1. Select **Team A** and **Team B** from the sidebar.
2. Choose a tactical formation for each team.
3. Click **Generate Match Analysis** to create the initial lineups.
4. Inspect the automatically generated Starting XIs and benches.
5. Modify lineups by:
   - Swapping player roles
   - Making substitutions from the bench
6. Observe how the pitch visualization and mismatch analysis update.
7. Click **Generate AI Tactical Plan** to receive a data-driven tactical plan.
8. Interact with the AI coach through the chat:
   - Ask questions
   - Propose tactical ideas
   - Suggest substitutions or pressing styles
9. Continue iterating until a satisfactory and realistic tactical solution
   is reached.

The system is explicitly designed for **co-creation**:
the human user guides the reasoning, while the AI adapts and responds based
on data, constraints, and tactical logic.


----------------------------------------------------------------
6. Notes
----------------------------------------------------------------

- All tactical suggestions are grounded in the provided data and current lineups.
- The AI is constrained to use only available players and bench options.
- The system prioritizes realism and explainability over generic advice.

----------------------------------------------------------------
End of README
----------------------------------------------------------------
```
