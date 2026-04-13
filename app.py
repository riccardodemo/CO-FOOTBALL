# =========================
# APP — CO-FOOTBALL (Streamlit)
# =========================

import streamlit as st
import matplotlib.pyplot as plt

from src.config import FORMATION_LIST, SYSTEM_PROMPT
from src.core import (
    df,
    generate_chat_response,
    run_cofootball,
    plot_team,
    generate_tactical_analysis,
    swap_lineup_players,
    substitute_player,
    analyze_mismatches,
    build_llm_analysis_text,
    build_llm_match_context
)

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="CO-FOOTBALL", layout="wide")
st.title("⚽ CO-FOOTBALL — Tactical Match Analysis")


if "llm_messages" not in st.session_state:
    st.session_state["llm_messages"] = []

# -------------------------
# HELPERS
# -------------------------
def signature(team1, formation1, team2, formation2):
    return (team1, formation1, team2, formation2)

def init_match_state(team1, formation1, team2, formation2):
    base = run_cofootball(team1, formation1, team2, formation2)

    st.session_state["lineup_team1"] = base["lineup_team1"]
    st.session_state["bench_team1"] = base["bench_team1"]
    st.session_state["lineup_team2"] = base["lineup_team2"]
    st.session_state["bench_team2"] = base["bench_team2"]

    st.session_state["out"] = {
        "mismatch_df": base["mismatch_df"],
        "analysis_text": base["analysis_text"]
    }

    st.session_state["match_signature"] = signature(team1, formation1, team2, formation2)
    st.session_state["lineups_dirty"] = False

def recalc_outputs_only(team1, team2):
    mismatch_df = analyze_mismatches(
        st.session_state["lineup_team1"],
        st.session_state["lineup_team2"],
        df,
        team1,
        team2
    )

    analysis_text = build_llm_analysis_text(
        mismatch_df,
        st.session_state["lineup_team1"],
        st.session_state["lineup_team2"],
        team1,
        team2,
        df
    )

    st.session_state["out"] = {
        "mismatch_df": mismatch_df,
        "analysis_text": analysis_text
    }

# -------------------------
# CALLBACKS (key idea)
# These run BEFORE the script body is rendered in the rerun,
# so the pitch updates immediately on the same click.
# -------------------------
def _swap_callback(prefix: str):
    team_key = "team1" if prefix == "A" else "team2"

    lineup_key = "lineup_team1" if prefix == "A" else "lineup_team2"

    role_a = st.session_state[f"{prefix}_swap_a"]
    role_b = st.session_state[f"{prefix}_swap_b"]

    st.session_state[lineup_key] = swap_lineup_players(st.session_state[lineup_key], role_a, role_b)
    st.session_state["lineups_dirty"] = True

def _sub_callback(prefix: str):
    lineup_key = "lineup_team1" if prefix == "A" else "lineup_team2"
    bench_key = "bench_team1" if prefix == "A" else "bench_team2"

    role_out = st.session_state[f"{prefix}_out"]
    player_in = st.session_state[f"{prefix}_in"]

    new_lineup, new_bench = substitute_player(
        st.session_state[lineup_key],
        st.session_state[bench_key],
        role_out,
        player_in
    )

    st.session_state[lineup_key] = new_lineup
    st.session_state[bench_key] = new_bench
    st.session_state["lineups_dirty"] = True

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("Match setup")

    teams = sorted(df["Team"].unique())

    team1 = st.selectbox("Team A", teams, key="team1")
    formation1 = st.selectbox("Formation A", FORMATION_LIST, key="formation1")

    team2 = st.selectbox("Team B", teams, index=1, key="team2")
    formation2 = st.selectbox("Formation B", FORMATION_LIST, key="formation2")

    generate_btn = st.button("Generate Match Analysis")
    reset_btn = st.button("Reset / Regenerate auto XI")

# -------------------------
# MATCH INIT / CHANGE
# -------------------------
current_sig = signature(team1, formation1, team2, formation2)


if "match_signature" not in st.session_state:
    init_match_state(team1, formation1, team2, formation2)

if st.session_state["match_signature"] != current_sig or reset_btn:
    init_match_state(team1, formation1, team2, formation2)

# -------------------------
# RECALC (single point)
# - runs when user clicks Generate OR after any edit (dirty flag)
# - safe to do it here because callbacks have already updated state
# -------------------------
if generate_btn or st.session_state.get("lineups_dirty", False):
    recalc_outputs_only(team1, team2)
    st.session_state["lineups_dirty"] = False

# -------------------------
# PITCH
# -------------------------
st.subheader("🧩 Starting XIs")

fig, axes = plt.subplots(1, 2, figsize=(16, 9))

plot_team(
    st.session_state["lineup_team1"],
    formation1,
    team1,
    axes[0],
    side="left"
)

plot_team(
    st.session_state["lineup_team2"],
    formation2,
    team2,
    axes[1],
    side="right"
)

st.pyplot(fig)

# -------------------------
# BENCHES
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🪑 Bench — {team1}")
    st.dataframe(
        st.session_state["bench_team1"][["Name", "Position", "OVR"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader(f"🪑 Bench — {team2}")
    st.dataframe(
        st.session_state["bench_team2"][["Name", "Position", "OVR"]],
        use_container_width=True,
        hide_index=True
    )

# -------------------------
# EDIT LINEUPS
# -------------------------
st.subheader("✏️ Edit Lineups")

team_edit = st.radio(
    "Select team to edit",
    ["Team A", "Team B"],
    horizontal=True
)

if team_edit == "Team A":
    prefix = "A"
    lineup = st.session_state["lineup_team1"]
    bench = st.session_state["bench_team1"]
else:
    prefix = "B"
    lineup = st.session_state["lineup_team2"]
    bench = st.session_state["bench_team2"]

roles = [r for r, _, _, _ in lineup]

# 🔄 Swap
st.markdown("### 🔄 Swap positions")
c1, c2, c3 = st.columns([3, 3, 2])
with c1:
    st.selectbox("Role A", roles, key=f"{prefix}_swap_a")
with c2:
    st.selectbox("Role B", roles, index=1 if len(roles) > 1 else 0, key=f"{prefix}_swap_b")
with c3:
    st.button("Swap", key=f"{prefix}_swap", on_click=_swap_callback, args=(prefix,))

# 🔁 Substitution
st.markdown("### 🔁 Substitution")
c1, c2, c3 = st.columns([3, 3, 2])
with c1:
    st.selectbox("OUT", roles, key=f"{prefix}_out")
with c2:
    st.selectbox("IN", bench["Name"].tolist(), key=f"{prefix}_in")
with c3:
    st.button("Substitute", key=f"{prefix}_sub", on_click=_sub_callback, args=(prefix,))

# -------------------------
# MISMATCHES
# -------------------------
st.subheader("📊 Physical & Positional Mismatches")

if st.session_state["out"]["mismatch_df"].empty:
    st.info("No significant mismatches detected.")
else:
    st.dataframe(st.session_state["out"]["mismatch_df"], use_container_width=True)

# -------------------------
# AI TACTICS
# -------------------------

st.subheader("🧠 AI Tactical Game Plan")

# Generate initial tactical analysis
if st.button("Generate AI Tactical Plan"):
    match_context = build_llm_match_context(
        team1, formation1,
        st.session_state["lineup_team1"],
        st.session_state["bench_team1"],
        team2, formation2,
        st.session_state["lineup_team2"],
        st.session_state["bench_team2"],
        st.session_state["out"]["analysis_text"]
    )

    st.session_state["llm_messages"] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": match_context
        }
    ]

    ai_text = generate_chat_response(st.session_state["llm_messages"])
    st.session_state["llm_messages"].append(
        {"role": "assistant", "content": ai_text}
    )

# -------------------------
# CHAT RENDER (AI + user follow-ups ONLY)
# -------------------------



st.markdown("### 💬 Talk with the AI Coach")

if "llm_messages" in st.session_state and len(st.session_state["llm_messages"]) > 0:

    for i, msg in enumerate(st.session_state["llm_messages"]):
        # skip system message
        if msg["role"] == "system":
            continue

        # skip initial match context (first user message)
        if msg["role"] == "user" and i == 1:
            continue

        if msg["role"] == "assistant":
            st.markdown(f"🧠 **Coach:**\n\n{msg['content']}")
        elif msg["role"] == "user":
            st.markdown(f"🧑‍💼 **You:** {msg['content']}")

# -------------------------
# CHAT INPUT (ENTER + SEND BUTTON)
# -------------------------
if "llm_messages" in st.session_state and len(st.session_state["llm_messages"]) > 0:

    # init input state
    if "chat_input" not in st.session_state:
        st.session_state["chat_input"] = ""

    def send_message():
        text = st.session_state["chat_input"].strip()
        if not text:
            return

        # 1️⃣ append user message
        st.session_state["llm_messages"].append(
            {"role": "user", "content": text}
        )

        # 2️⃣ clear input BEFORE LLM call
        st.session_state["chat_input"] = ""

        # 3️⃣ call LLM
        with st.spinner("AI coach is thinking..."):
            ai_reply = generate_chat_response(st.session_state["llm_messages"])

        # 4️⃣ append AI reply
        st.session_state["llm_messages"].append(
            {"role": "assistant", "content": ai_reply}
        )

    # ENTER triggers this
    st.text_input(
        "Your message",
        placeholder="e.g. What if I press higher in the first 20 minutes?",
        key="chat_input",
        on_change=send_message
    )
