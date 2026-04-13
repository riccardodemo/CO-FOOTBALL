# =========================
# CORE — CO-FOOTBALL
# =========================

from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from groq import Groq

from src.config import (
    NUMERIC_COLUMNS,
    FAKE_TO_REAL,
    FORMATIONS,
    POSITION_MAPPING,
    FALLBACK_ROLES,
    TEAM_COLORS,
    GK_COLORS,
    FORMATION_POSITIONS,
    ROLE_ZONES,
    MATCHUPS,
    MISMATCH_THRESHOLD,
    LLM_MODEL,
    LLM_TEMPERATURE,
    PITCH_BG_COLOR,
    PITCH_LINE_COLOR,
    PITCH_LINE_WIDTH,
)

# =========================
# DATA LOADING
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "EAFC26-Men.csv"

df = pd.read_csv(DATA_PATH)

# -------------------------
# CLEAN & CONVERT
# -------------------------

if "Height" in df.columns:
    df["Height"] = df["Height"].astype(str).str.extract(r"(\d+)").astype(float)

if "Weight" in df.columns:
    df["Weight"] = df["Weight"].astype(str).str.extract(r"(\d+)").astype(float)

for col in NUMERIC_COLUMNS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].fillna(0)

df["Team"] = df["Team"].replace(FAKE_TO_REAL)

# =========================
# LINEUP LOGIC
# =========================

def position_penalty(role, player_position):
    if role == player_position:
        return 0
    if role in ["LCAM", "RCAM"] and player_position == "CAM":
        return 0
    if role in ["LCB", "RCB", "CB"] and player_position == "CB":
        return 1
    return 8

def build_lineup(df, team_name, formation):
    team = df[df["Team"] == team_name]
    lineup, remaining = [], team.copy()

    for role in FORMATIONS[formation]:
        possible = POSITION_MAPPING.get(role, [role])
        available = remaining[remaining["Position"].isin(possible)]

        if available.empty:
            fallback = remaining[remaining["Position"].isin(FALLBACK_ROLES.get(role, []))]
            if fallback.empty:
                lineup.append((role, "— NO PLAYER —", "-", "-"))
                continue
            available = fallback
            penalty_extra = 4
        else:
            penalty_extra = 0

        available = available.copy()
        available["Score"] = available["OVR"] - available["Position"].apply(
            lambda p: position_penalty(role, p) + penalty_extra
        )

        best = available.sort_values("Score", ascending=False).iloc[0]
        lineup.append((role, best["Name"], best["Position"], best["OVR"]))
        remaining = remaining[remaining["Name"] != best["Name"]]

    return lineup

def get_bench(df, team_name, lineup):
    used = {n for _, n, _, _ in lineup if not n.startswith("—")}
    bench = df[(df["Team"] == team_name) & (~df["Name"].isin(used))]
    return bench.sort_values("OVR", ascending=False)

# --------------------------------------------------------------------
# DRAWING FUNCTIONS (REALISTIC PITCH)
# --------------------------------------------------------------------

def draw_pitch(ax):
    ax.set_facecolor(PITCH_BG_COLOR)
    lw = PITCH_LINE_WIDTH
    lc = PITCH_LINE_COLOR

    ax.add_patch(patches.Rectangle((0, 0), 100, 100, fill=False, edgecolor=lc, lw=lw))
    ax.plot([0, 100], [50, 50], color=lc, lw=lw)

    ax.add_patch(patches.Circle((50, 50), 9.15, fill=False, edgecolor=lc, lw=lw))
    ax.scatter(50, 50, color=lc, s=18, zorder=2)

    ax.add_patch(patches.Rectangle((21.1, 0), 57.8, 16.5, fill=False, edgecolor=lc, lw=lw))
    ax.add_patch(patches.Rectangle((36.8, 0), 26.4, 5.5, fill=False, edgecolor=lc, lw=lw))
    ax.scatter(50, 11, color=lc, s=18, zorder=2)

    ax.add_patch(patches.Rectangle((21.1, 83.5), 57.8, 16.5, fill=False, edgecolor=lc, lw=lw))
    ax.add_patch(patches.Rectangle((36.8, 94.5), 26.4, 5.5, fill=False, edgecolor=lc, lw=lw))
    ax.scatter(50, 89, color=lc, s=18, zorder=2)

    ax.add_patch(patches.Arc((50, 11), 18.3, 18.3, theta1=37, theta2=143, edgecolor=lc, lw=lw))
    ax.add_patch(patches.Arc((50, 89), 18.3, 18.3, theta1=217, theta2=323, edgecolor=lc, lw=lw))

    ax.add_patch(patches.Rectangle((45, -2), 10, 2, fill=False, edgecolor=lc, lw=lw))
    ax.add_patch(patches.Rectangle((45, 100), 10, 2, fill=False, edgecolor=lc, lw=lw))

    ax.set_xlim(-3, 103)
    ax.set_ylim(-3, 103)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# --------------------------------------------------------------------
# DRAW PLAYER MARKER (SOLID OR SPLIT)
# --------------------------------------------------------------------

def draw_player_marker(ax, x, y, colors, size=850):
    radius = np.sqrt(size / np.pi) / 7

    if len(colors) == 1:
        ax.add_patch(
            patches.Circle(
                (x, y), radius,
                facecolor=colors[0], edgecolor="white", lw=2.2, zorder=3
            )
        )
    else:
        ax.add_patch(
            patches.Wedge(
                (x, y), radius, 90, 270,
                facecolor=colors[0], edgecolor="none", zorder=3
            )
        )
        ax.add_patch(
            patches.Wedge(
                (x, y), radius, -90, 90,
                facecolor=colors[1], edgecolor="none", zorder=3
            )
        )
        ax.add_patch(
            patches.Circle(
                (x, y), radius,
                facecolor="none", edgecolor="white", lw=2.2, zorder=4
            )
        )

# --------------------------------------------------------------------
# PLOT TEAM
# --------------------------------------------------------------------

def plot_team(lineup, formation, team_name, ax, side="left"):
    draw_pitch(ax)

    team_colors = TEAM_COLORS.get(team_name, ["#888888"])

    title = ax.set_title(
        f"{team_name}  {formation}",
        fontsize=20, color=team_colors[0], weight="bold", pad=18
    )
    title.set_path_effects([pe.withStroke(linewidth=4, foreground="black")])

    coords = FORMATION_POSITIONS.get(formation, {})

    for role, name, pos, _ in lineup:
        x, y = coords.get(role, (50, 50))

        if role == "GK":
            colors = GK_COLORS["left"] if side == "left" else GK_COLORS["right"]
        else:
            colors = team_colors

        draw_player_marker(ax, x, y, colors)

        parts = str(name).split()
        label = " ".join(parts[1:]) if len(parts) >= 2 else parts[0]

        ax.text(
            x, y, label,
            ha="center", va="center",
            fontsize=9, weight="bold", color="white",
            path_effects=[pe.withStroke(linewidth=2.5, foreground="black")],
            zorder=5
        )

# =========================
# MISMATCH ANALYSIS
# =========================

def analyze_mismatches(lineup_a, lineup_b, df, team1, team2):
    METRICS = {
        "Speed": lambda p: (p["Sprint Speed"] + p["Acceleration"]) / 2,
        "Aerial": lambda p: (p["Height"] + p["Jumping"]) / 2,
        "Physicality": lambda p: (p["Strength"] + p["Aggression"]) / 2,
        "Balance": lambda p: (p["Balance"] + p["Agility"]) / 2
    }

    def zone(role):
        for z, roles in ROLE_ZONES.items():
            if role in roles:
                return z
        return None

    def get_player(name):
        return df[df["Name"] == name].iloc[0]

    rows = []

    for A, B, ta, tb in [
        (lineup_a, lineup_b, team1, team2),
        (lineup_b, lineup_a, team2, team1)
    ]:
        for rA, nA, _, _ in A:
            if nA.startswith("—"):
                continue
            zA = zone(rA)
            if zA not in MATCHUPS:
                continue
            pA = get_player(nA)

            for rB, nB, _, _ in B:
                if nB.startswith("—"):
                    continue
                if zone(rB) not in MATCHUPS[zA]:
                    continue
                pB = get_player(nB)

                for m, fn in METRICS.items():
                    diff = fn(pA) - fn(pB)
                    if abs(diff) > MISMATCH_THRESHOLD:
                        rows.append({
                            "Attacking Team": ta,
                            "Defending Team": tb,
                            "Attacker": f"{nA} ({rA})",
                            "Defender": f"{nB} ({rB})",
                            "Metric": m,
                            "Difference": round(diff, 1)
                        })

    return pd.DataFrame(rows)

# =========================
# LLM SUPPORT
# =========================

def format_lineup_for_llm(lineup):
    return "\n".join(f"{r}: {n} ({p}, OVR {o})" for r, n, p, o in lineup)

def build_llm_analysis_text(mismatch_df, lineup_a, lineup_b, team1, team2, df):
    lines = [f"TEAM A: {team1}", f"TEAM B: {team2}", ""]
    if mismatch_df is not None and not mismatch_df.empty:
        for _, r in mismatch_df.head(10).iterrows():
            lines.append(f"- {r['Attacker']} vs {r['Defender']} | {r['Metric']}: {r['Difference']}")
    return "\n".join(lines)

def generate_tactical_analysis(
    team1, formation1, lineup_team1, bench_team1,
    team2, formation2, lineup_team2,
    analysis_text
):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a professional football assistant coach."},
            {"role": "user", "content": analysis_text}
        ]
    )

    return response.choices[0].message.content

# =========================
# MAIN CORE ENTRYPOINT
# =========================

def run_cofootball(team1, formation1, team2, formation2, df=df):
    lineup1 = build_lineup(df, team1, formation1)
    lineup2 = build_lineup(df, team2, formation2)

    bench1 = get_bench(df, team1, lineup1)
    bench2 = get_bench(df, team2, lineup2)

    mismatches = analyze_mismatches(lineup1, lineup2, df, team1, team2)
    analysis_text = build_llm_analysis_text(mismatches, lineup1, lineup2, team1, team2, df)

    return {
        "lineup_team1": lineup1,
        "lineup_team2": lineup2,
        "bench_team1": bench1,
        "bench_team2": bench2,
        "mismatch_df": mismatches,
        "analysis_text": analysis_text
    }

def swap_lineup_players(lineup, role_a, role_b):
    lineup = list(lineup)

    idx_a = next(i for i, (r, _, _, _) in enumerate(lineup) if r == role_a)
    idx_b = next(i for i, (r, _, _, _) in enumerate(lineup) if r == role_b)

    lineup[idx_a], lineup[idx_b] = (
        (lineup[idx_a][0], lineup[idx_b][1], lineup[idx_b][2], lineup[idx_b][3]),
        (lineup[idx_b][0], lineup[idx_a][1], lineup[idx_a][2], lineup[idx_a][3])
    )

    return lineup

def substitute_player(lineup, bench_df, role_out, player_in_name):
    lineup = list(lineup)
    bench_df = bench_df.copy()

    idx_out = next(
        i for i, (r, _, _, _) in enumerate(lineup) if r == role_out
    )

    role, player_out_name, _, _ = lineup[idx_out]

    player_in_row = bench_df.loc[
        bench_df["Name"] == player_in_name
    ].iloc[0]

    lineup[idx_out] = (
        role,
        player_in_row["Name"],
        player_in_row["Position"],
        player_in_row["OVR"]
    )

    bench_df = bench_df[bench_df["Name"] != player_in_name]

    bench_df = pd.concat(
        [bench_df, df.loc[df["Name"] == player_out_name].head(1)],
        ignore_index=True
    )

    return lineup, bench_df.sort_values("OVR", ascending=False)

def generate_chat_response(messages):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=messages
    )

    return response.choices[0].message.content

def build_llm_match_context(
    team1, formation1, lineup1, bench1,
    team2, formation2, lineup2, bench2,
    analysis_text
):
    def fmt_lineup(lineup):
        return "\n".join(
            f"- {r}: {n} ({p}, OVR {o})"
            for r, n, p, o in lineup
        )

    def fmt_bench(bench_df):
        return "\n".join(
            f"- {r['Name']} ({r['Position']}, OVR {r['OVR']})"
            for _, r in bench_df.head(10).iterrows()
        )

    return f"""
MATCH CONTEXT
=============

TEAM A
- Team: {team1}
- Formation: {formation1}

Starting XI:
{fmt_lineup(lineup1)}

Bench options (ONLY these players can be used for substitutions):
{fmt_bench(bench1)}


TEAM B
- Team: {team2}
- Formation: {formation2}

Starting XI:
{fmt_lineup(lineup2)}

Bench options:
{fmt_bench(bench2)}


KEY PHYSICAL & POSITIONAL MISMATCHES
===================================
{analysis_text}


TACTICAL TASK
==============

Prepare a tactical game plan for TEAM A.

### 1. Attacking Strategy
- Identify the **2–3 most important positive mismatches** for Team A.
- For each mismatch:
  • where it occurs on the pitch
  • why it is an advantage
  • how it should be exploited

### 2. Defensive & Rest-Defense Strategy
- Identify the **main risks** for Team A when attacking.
- Explain:
  • which zones must be protected
  • how the team should be positioned in possession
  • how to prevent counter-attacks

### 3. Team Principles
- Attacking principles (max 5 bullets)
- Defensive principles (max 5 bullets)
Each bullet must include a **short tactical reason**.

### 4. Substitutions & Adjustments
- If the starting XI is already optimal, explicitly say so.
- Otherwise, suggest **at most 2 substitutions**.
- Each substitution must:
  • use ONLY the listed bench players
  • solve a specific tactical problem
  • include timing
  • explain why it improves the plan



DATA CONSTRAINTS
================
- Do NOT invent players.
- Do NOT suggest formation changes unless strictly necessary.
- Base every recommendation on the provided data and mismatches.
"""
