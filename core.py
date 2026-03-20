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

# =========================
# DATA LOADING
# =========================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "EAFC26-Men.csv"

df = pd.read_csv(DATA_PATH)

# -------------------------
# CLEAN & CONVERT
# -------------------------

numeric_columns = [
    "OVR","PAC","SHO","PAS","DRI","DEF","PHY",
    "Acceleration","Sprint Speed","Positioning","Finishing","Shot Power",
    "Long Shots","Volleys","Penalties","Vision","Crossing","Free Kick Accuracy",
    "Short Passing","Long Passing","Curve","Dribbling","Agility","Balance",
    "Reactions","Ball Control","Composure","Interceptions","Heading Accuracy",
    "Def Awareness","Standing Tackle","Sliding Tackle","Jumping",
    "Stamina","Strength","Aggression","Age"
]

if "Height" in df.columns:
    df["Height"] = df["Height"].astype(str).str.extract(r"(\d+)").astype(float)

if "Weight" in df.columns:
    df["Weight"] = df["Weight"].astype(str).str.extract(r"(\d+)").astype(float)

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_columns] = df[numeric_columns].fillna(0)

fake_to_real = {
    "Lombardia FC": "Inter Milan",
    "Milano FC": "AC Milan",
    "Milan FC": "AC Milan",
    "Bergamo Calcio": "Atalanta BC",
    "Latium": "SS Lazio"
}
df["Team"] = df["Team"].replace(fake_to_real)

# =========================
# FORMATIONS & MAPPINGS
# =========================

formations = {
    "4-3-3": ["GK","LB","LCB","RCB","RB","LCM","CDM","RCM","LW","ST","RW"],
    "4-4-2": ["GK","LB","LCB","RCB","RB","LM","LCM","RCM","RM","LST","RST"],
    "3-5-2": ["GK","LCB","CB","RCB","LWB","LCM","CDM","RCM","RWB","LST","RST"],
    "4-2-3-1": ["GK","LB","LCB","RCB","RB","LCDM","RCDM","CAM","LW","RW","ST"],
    "3-4-3": ["GK","LCB","CB","RCB","LWB","LCM","RCM","RWB","LW","ST","RW"],
    "3-4-2-1": ["GK","LCB","CB","RCB","LWB","LCM","RCM","RWB","LCAM","RCAM","ST"]
}

position_mapping = {
    "GK": ["GK"],
    "LB": ["LB","LWB"], "RB": ["RB","RWB"],
    "LCB": ["CB","LB"], "RCB": ["CB","RB"], "CB": ["CB"],
    "LWB": ["LWB","LB","LM"], "RWB": ["RWB","RB","RM"],
    "LCDM": ["CDM","CM"], "RCDM": ["CDM","CM"],
    "LCM": ["CM","CAM","LM"], "RCM": ["CM","CAM","RM"],
    "CM": ["CM","CDM","CAM"],
    "CAM": ["CAM","CM"],
    "LCAM": ["CAM","CM","LM"], "RCAM": ["CAM","CM","RM"],
    "LW": ["LW","LM"], "RW": ["RW","RM"],
    "ST": ["ST","CF"], "LST": ["ST","CF"], "RST": ["ST","CF"]
}

fallback_roles = {
    "LW": ["RW","ST"], "RW": ["LW","ST"],
    "ST": ["CF"], "LST": ["ST","CF"], "RST": ["ST","CF"],
    "CAM": ["CM","ST","LW","RW"],
    "LCM": ["CM","CDM","CAM"], "RCM": ["CM","CDM","CAM"],
    "CM": ["LCM","RCM","CDM"],
    "CDM": ["CM","CB"],
    "LWB": ["LB","LM"], "RWB": ["RB","RM"],
    "LB": ["LWB","CB"], "RB": ["RWB","CB"],
    "LCB": ["CB"], "RCB": ["CB"], "CB": ["LCB","RCB"]
}

# =========================
# LINEUP LOGIC
# =========================

def position_penalty(role, player_position):
    if role == player_position:
        return 0
    if role in ["LCAM","RCAM"] and player_position == "CAM":
        return 0
    if role in ["LCB","RCB","CB"] and player_position == "CB":
        return 1
    return 8

def build_lineup(df, team_name, formation):
    team = df[df["Team"] == team_name]
    lineup, remaining = [], team.copy()

    for role in formations[formation]:
        possible = position_mapping.get(role, [role])
        available = remaining[remaining["Position"].isin(possible)]

        if available.empty:
            fallback = remaining[remaining["Position"].isin(fallback_roles.get(role, []))]
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

TEAM_COLORS = {

    # =========================
    # 🇬🇧 PREMIER LEAGUE (FC 26)
    # =========================
    "AFC Bournemouth": ["#DA291C", "#000000"],
    "Arsenal": ["#EF0107", "#ffffff"],
    "Aston Villa": ["#7A003C", "#94BEE5"],
    "Brentford": ["#E30613", "#ffffff"],
    "Brighton": ["#0057B8", "#ffffff"],
    "Burnley": ["#6C1D45", "#99D6EA"],
    "Chelsea": ["#034694"],
    "Crystal Palace": ["#1B458F", "#C4122E"],
    "Everton": ["#003399"],
    "Fulham": ["#000000", "#ffffff"],
    "Leeds United": ["#ffffff", "#1D428A"],
    "Liverpool": ["#C8102E"],
    "Man Utd": ["#DA291C", "#000000"],
    "Manchester City": ["#6CABDD"],
    "Newcastle Utd": ["#000000", "#ffffff"],
    "Nott'm Forest": ["#DD0000", "#ffffff"],
    "Spurs": ["#132257", "#ffffff"],
    "Sunderland": ["#E30613", "#ffffff"],
    "West Ham": ["#7A263A", "#1BB1E7"],
    "Wolves": ["#FDB913", "#000000"],

    # =========================
    # 🇮🇹 SERIE A ENILIVE (FC 26)
    # =========================
    "AC Milan": ["#FB090B", "#000000"],
    "AS Roma": ["#8E1F2F", "#F7A600"],
    "Atalanta BC": ["#0057B8", "#000000"],
    "Bologna": ["#1F2A44", "#8B1C2D"],
    "Cagliari": ["#7A0026", "#003A8F"],
    "Como": ["#005DAA", "#ffffff"],
    "Cremonese": ["#E30613", "#CFAE70"],
    "Fiorentina": ["#5B2C83"],
    "Genoa": ["#A50021", "#002F6C"],
    "Hellas Verona": ["#002F6C", "#FEEB00"],
    "Inter Milan": ["#00529F", "#000000"],
    "Juventus": ["#000000", "#ffffff"],
    "Lecce": ["#E30613", "#FEEB00"],
    "Parma": ["#003A8F", "#FEEB00"],
    "Pisa": ["#000000", "#003A8F"],
    "SS Lazio": ["#A7C6ED"],
    "SSC Napoli": ["#12A0D7"],
    "Sassuolo": ["#007A33", "#000000"],
    "Torino": ["#7A263A"],
    "Udinese": ["#000000", "#ffffff"],

    # =========================
    # 🇪🇸 LALIGA EA SPORTS (FC 26)
    # =========================
    "Athletic Club": ["#EE2523", "#ffffff"],
    "Atlético de Madrid": ["#CB3524", "#ffffff"],
    "CA Osasuna": ["#C8102E", "#002F6C"],
    "Celta": ["#7EC8E3", "#ffffff"],
    "D. Alavés": ["#003A8F", "#ffffff"],
    "Elche CF": ["#007A33", "#ffffff"],
    "FC Barcelona": ["#A50044", "#004D98"],
    "Getafe CF": ["#0057B8", "#ffffff"],
    "Girona FC": ["#D71920", "#ffffff"],
    "Levante UD": ["#9B1C2D", "#003A8F"],
    "R. Oviedo": ["#003A8F", "#ffffff"],
    "RCD Espanyol": ["#0057B8", "#ffffff"],
    "RCD Mallorca": ["#E30613", "#000000"],
    "Rayo Vallecano": ["#E30613", "#ffffff"],
    "Real Betis": ["#007A33", "#ffffff"],
    "Real Madrid": ["#ffffff"],
    "Real Sociedad": ["#00529F", "#ffffff"],
    "Sevilla FC": ["#D71920", "#ffffff"],
    "Valencia CF": ["#000000", "#ffffff"],
    "Villarreal CF": ["#FEEB00", "#004B87"],

    # =========================
    # 🇫🇷 LIGUE 1 McDONALD'S (FC 26)
    # =========================
    "AJ Auxerre": ["#0055A4", "#ffffff"],
    "AS Monaco": ["#E31B23", "#ffffff"],
    "Angers SCO": ["#000000", "#ffffff"],
    "FC Lorient": ["#FF8C00", "#000000"],
    "FC Metz": ["#7A0026", "#ffffff"],
    "FC Nantes": ["#FFD100", "#007A33"],
    "Havre AC": ["#7EC8E3", "#002F6C"],
    "LOSC Lille": ["#E1001A", "#0A2240"],
    "OGC Nice": ["#E30613", "#000000"],
    "OL": ["#DA291C", "#0055A4"],
    "OM": ["#00AEEF", "#ffffff"],
    "Paris FC": ["#003A8F", "#ffffff"],
    "Paris SG": ["#004170", "#DA291C"],
    "RC Lens": ["#FFD100", "#E30613"],
    "Stade Brestois 29": ["#E30613", "#ffffff"],
    "Stade Rennais FC": ["#E30613", "#000000"],
    "Strasbourg": ["#0055A4", "#ffffff"],
    "Toulouse FC": ["#5B2C83", "#ffffff"],

    # =========================
    # 🇩🇪 BUNDESLIGA (FC 26)
    # =========================
    "1. FC Köln": ["#E30613", "#ffffff"],
    "1. FSV Mainz 05": ["#C8102E", "#ffffff"],
    "Borussia Dortmund": ["#FDE100", "#000000"],
    "FC Augsburg": ["#C8102E", "#007A33"],
    "FC Bayern München": ["#DC052D", "#ffffff"],
    "FC St. Pauli": ["#4E342E", "#ffffff"],
    "Frankfurt": ["#000000", "#E1001A"],
    "Hamburger SV": ["#0055A4", "#ffffff"],
    "Heidenheim": ["#E30613", "#002F6C"],
    "Leverkusen": ["#E32219", "#000000"],
    "M'gladbach": ["#000000", "#ffffff"],
    "RB Leipzig": ["#DD0741", "#ffffff"],
    "SC Freiburg": ["#000000", "#E30613"],
    "SV Werder Bremen": ["#007A33", "#ffffff"],
    "TSG Hoffenheim": ["#0055A4", "#ffffff"],
    "Union Berlin": ["#E30613", "#ffffff"],
    "VfB Stuttgart": ["#E30613", "#ffffff"],
    "VfL Wolfsburg": ["#65B32E", "#ffffff"],
    # =========================
    # 🇵🇹 LIGA PORTUGAL (FC 26)
    # =========================
    "SL Benfica": ["#E10600"],
    "FC Porto": ["#0033A0", "#ffffff"],
    "Sporting CP": ["#006633", "#ffffff"],
    "SC Braga": ["#E30613", "#ffffff"],
    "Vitória SC": ["#000000", "#ffffff"],
    "Boavista": ["#000000", "#ffffff"],
    "Famalicão": ["#0033A0", "#ffffff"],
    "Gil Vicente": ["#E30613", "#003A8F"],
    "Casa Pia": ["#000000"],
    "Estoril Praia": ["#FEEB00", "#003A8F"],
    "Portimonense": ["#000000", "#ffffff"],
    "Rio Ave": ["#007A33", "#ffffff"],
    "Moreirense": ["#007A33", "#ffffff"],
    "Arouca": ["#FFD100", "#003A8F"],
    "Farense": ["#000000", "#ffffff"],
    "Vizela": ["#0057B8", "#FEEB00"],
    "Chaves": ["#E30613", "#003A8F"],
    "AVS": ["#000000", "#ffffff"],
    # =========================
    # 🇳🇱 EREDIVISIE (FC 26)
    # =========================
    "Ajax": ["#C8102E", "#ffffff"],
    "PSV": ["#E30613", "#ffffff"],
    "Feyenoord": ["#C8102E", "#000000"],
    "AZ Alkmaar": ["#C8102E"],
    "FC Twente": ["#E30613", "#ffffff"],
    "Utrecht": ["#E30613", "#ffffff"],
    "Heerenveen": ["#0057B8", "#ffffff"],
    "Vitesse": ["#FEEB00", "#000000"],
    "NEC": ["#E30613", "#000000"],
    "Sparta Rotterdam": ["#E30613", "#ffffff"],
    "Heracles": ["#000000", "#ffffff"],
    "Go Ahead Eagles": ["#E30613", "#FEEB00"],
    "PEC Zwolle": ["#0057B8", "#ffffff"],
    "RKC Waalwijk": ["#FEEB00", "#0057B8"],
    "Fortuna Sittard": ["#007A33", "#FEEB00"],
    "Almere City": ["#E30613"],
    "FC Volendam": ["#F36F21"],
    "Excelsior": ["#000000", "#E30613"]
}

GK_COLORS = {
    "left": ["#E6FF00"],   # YELLLOW
    "right": ["#7B1FA2"]   # PURPLE
}



# --------------------------------------------------------------------
# FORMATIONS and the exact positional layout on the pitch (x,y in 0–100 range)
# --------------------------------------------------------------------
formation_positions = {
    "4-3-3": {
        "GK":  (50,  8),
        "LB":  (15, 25), "LCB": (35, 25), "RCB": (65, 25), "RB":  (85, 25),
        "LCM": (35, 50), "CDM": (50, 45), "RCM": (65, 50),
        "LW":  (15, 70), "ST":  (50, 85), "RW":  (85, 70)
    },
    "4-4-2": {
        "GK":  (50,  8),
        "LB":  (15, 25), "LCB": (35, 25), "RCB": (65, 25), "RB":  (85, 25),
        "LM":  (15, 55), "LCM": (35, 55), "RCM": (65, 55), "RM":  (85, 55),
        "LST": (40, 80), "RST": (60, 80)
    },
    "3-5-2": {
        "GK":  (50,  8),
        "LCB": (30, 25), "CB":  (50, 25), "RCB": (70, 25),
        "LWB": (15, 50), "LCM": (35, 50), "CDM":  (50, 45), "RCM": (65, 50), "RWB": (85, 50),
        "LST": (42, 80), "RST": (58, 80)
    },
    "4-2-3-1": {
        "GK":   (50,  8),
        "LB":   (15, 25), "LCB": (35, 25), "RCB": (65, 25), "RB":   (85, 25),
        "LCDM": (40, 45), "RCDM": (60, 45),
        "CAM":  (50, 65), "LW":   (20, 70), "RW":   (80, 70),
        "ST":   (50, 85)
    },
    "3-4-3": {
        "GK":  (50,  8),
        "LCB": (30, 25), "CB":  (50, 25), "RCB": (70, 25),
        "LWB": (15, 50), "LCM": (40, 50), "RCM": (60, 50), "RWB": (85, 50),
        "LW":  (20, 75), "ST":  (50, 85), "RW":  (80, 75)
    },
    "3-4-2-1": {
        "GK":  (50,  8),
        "LCB": (30, 25), "CB":  (50, 25), "RCB": (70, 25),
        "LWB": (15, 50), "LCM": (40, 50), "RCM": (60, 50), "RWB": (85, 50),
        "LCAM": (35, 70), "RCAM": (65, 70),
        "ST":  (50, 85)
    }
}


# --------------------------------------------------------------------
# DRAWING FUNCTIONS (REALISTIC PITCH)
# --------------------------------------------------------------------

def draw_pitch(ax):
    ax.set_facecolor("#2e7d32")
    line_color = "white"
    lw = 2

    ax.add_patch(patches.Rectangle((0, 0), 100, 100, fill=False, edgecolor=line_color, lw=lw))
    ax.plot([0, 100], [50, 50], color=line_color, lw=lw)

    ax.add_patch(patches.Circle((50, 50), 9.15, fill=False, edgecolor=line_color, lw=lw))
    ax.scatter(50, 50, color=line_color, s=18, zorder=2)

    ax.add_patch(patches.Rectangle((21.1, 0), 57.8, 16.5, fill=False, edgecolor=line_color, lw=lw))
    ax.add_patch(patches.Rectangle((36.8, 0), 26.4, 5.5, fill=False, edgecolor=line_color, lw=lw))
    ax.scatter(50, 11, color=line_color, s=18, zorder=2)

    ax.add_patch(patches.Rectangle((21.1, 83.5), 57.8, 16.5, fill=False, edgecolor=line_color, lw=lw))
    ax.add_patch(patches.Rectangle((36.8, 94.5), 26.4, 5.5, fill=False, edgecolor=line_color, lw=lw))
    ax.scatter(50, 89, color=line_color, s=18, zorder=2)

    ax.add_patch(patches.Arc((50, 11), 18.3, 18.3, theta1=37, theta2=143, edgecolor=line_color, lw=lw))
    ax.add_patch(patches.Arc((50, 89), 18.3, 18.3, theta1=217, theta2=323, edgecolor=line_color, lw=lw))

    ax.add_patch(patches.Rectangle((45, -2), 10, 2, fill=False, edgecolor=line_color, lw=lw))
    ax.add_patch(patches.Rectangle((45, 100), 10, 2, fill=False, edgecolor=line_color, lw=lw))

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

import numpy as np
import matplotlib.patches as patches


def draw_player_marker(ax, x, y, colors, size=850):
    """
    Draws a player marker with:
    - identical size for 1 or 2 colors
    - NO white line between colors
    - white outline only on the outside
    """

    radius = np.sqrt(size / np.pi) / 7

    if len(colors) == 1:
        # Single color: circle with outline
        ax.add_patch(
            patches.Circle(
                (x, y),
                radius,
                facecolor=colors[0],
                edgecolor="white",
                lw=2.2,
                zorder=3
            )
        )
    else:
        # Two colors: fill only (NO edges)
        ax.add_patch(
            patches.Wedge(
                (x, y), radius, 90, 270,
                facecolor=colors[0],
                edgecolor="none",
                zorder=3
            )
        )
        ax.add_patch(
            patches.Wedge(
                (x, y), radius, -90, 90,
                facecolor=colors[1],
                edgecolor="none",
                zorder=3
            )
        )

        # Single outer outline
        ax.add_patch(
            patches.Circle(
                (x, y),
                radius,
                facecolor="none",
                edgecolor="white",
                lw=2.2,
                zorder=4
            )
        )

# --------------------------------------------------------------------
# PLOT TEAM
# --------------------------------------------------------------------

def plot_team(lineup, formation, team_name, ax, side="left"):
    
    draw_pitch(ax)

    team_colors = TEAM_COLORS.get(team_name, ["#888888"])

    title = ax.set_title(f"{team_name}  {formation}", fontsize=20, color=team_colors[0], weight="bold", pad=18)
    title.set_path_effects([pe.withStroke(linewidth=4, foreground="black")])

    coords = formation_positions.get(formation, {})

    for role, name, pos, _ in lineup:
        x, y = coords.get(role, (50, 50))
    
        # 🎯 PORTIERE: colore speciale
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
    ROLE_ZONES = {
        "LEFT_WING": ["LW","LM","LWB"],
        "RIGHT_WING": ["RW","RM","RWB"],
        "CENTER_FORWARD": ["ST","LST","RST"],
        "ATTACKING_MID": ["CAM","LCAM","RCAM"],
        "CENTRAL_MID": ["CM","LCM","RCM","CDM","LCDM","RCDM"],
        "CENTER_BACK": ["CB","LCB","RCB"],
        "LEFT_DEF": ["LB","LCB"],
        "RIGHT_DEF": ["RB","RCB"]
    }

    MATCHUPS = {
        "LEFT_WING": ["RIGHT_DEF"],
        "RIGHT_WING": ["LEFT_DEF"],
        "CENTER_FORWARD": ["CENTER_BACK"],
        "ATTACKING_MID": ["CENTRAL_MID"]
    }

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
                    if abs(diff) > 4:
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
    return "\n".join(f"{r}: {n} ({p}, OVR {o})" for r,n,p,o in lineup)

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
        model="llama-3.3-70b-versatile",
        temperature=0.45,
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
    """
    Swaps two players inside the starting XI by role
    """
    lineup = list(lineup)

    idx_a = next(i for i, (r,_,_,_) in enumerate(lineup) if r == role_a)
    idx_b = next(i for i, (r,_,_,_) in enumerate(lineup) if r == role_b)

    lineup[idx_a], lineup[idx_b] = (
        (lineup[idx_a][0], lineup[idx_b][1], lineup[idx_b][2], lineup[idx_b][3]),
        (lineup[idx_b][0], lineup[idx_a][1], lineup[idx_a][2], lineup[idx_a][3])
    )

    return lineup

def substitute_player(lineup, bench_df, role_out, player_in_name):
    """
    Safe substitution:
    - replaces OUT with IN in the lineup
    - removes IN from bench
    - adds exactly ONE OUT back to bench
    - preserves lineup integrity
    """
    lineup = list(lineup)
    bench_df = bench_df.copy()

    # find exact OUT by role
    idx_out = next(
        i for i, (r, _, _, _) in enumerate(lineup) if r == role_out
    )

    role, player_out_name, _, _ = lineup[idx_out]

    # find IN (must be unique)
    player_in_row = bench_df.loc[
        bench_df["Name"] == player_in_name
    ].iloc[0]

    # replace in lineup
    lineup[idx_out] = (
        role,
        player_in_row["Name"],
        player_in_row["Position"],
        player_in_row["OVR"]
    )

    # remove IN from bench
    bench_df = bench_df[bench_df["Name"] != player_in_name]

    # add ONE row for OUT back to bench (CRUCIAL)
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
        model="llama-3.3-70b-versatile",
        temperature=0.45,
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
