# =========================
# CONFIG — CO-FOOTBALL
# Single source of truth for all hardcoded data
# =========================

# -------------------------
# DATA COLUMNS
# -------------------------

NUMERIC_COLUMNS = [
    "OVR", "PAC", "SHO", "PAS", "DRI", "DEF", "PHY",
    "Acceleration", "Sprint Speed", "Positioning", "Finishing", "Shot Power",
    "Long Shots", "Volleys", "Penalties", "Vision", "Crossing", "Free Kick Accuracy",
    "Short Passing", "Long Passing", "Curve", "Dribbling", "Agility", "Balance",
    "Reactions", "Ball Control", "Composure", "Interceptions", "Heading Accuracy",
    "Def Awareness", "Standing Tackle", "Sliding Tackle", "Jumping",
    "Stamina", "Strength", "Aggression", "Age"
]

# -------------------------
# TEAM NAME ALIASES (fake -> real)
# -------------------------

FAKE_TO_REAL = {
    "Lombardia FC": "Inter Milan",
    "Milano FC": "AC Milan",
    "Milan FC": "AC Milan",
    "Bergamo Calcio": "Atalanta BC",
    "Latium": "SS Lazio"
}

# -------------------------
# FORMATIONS (role slots)
# -------------------------

FORMATIONS = {
    "4-3-3":   ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CDM", "RCM", "LW", "ST", "RW"],
    "4-4-2":   ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "RCM", "RM", "LST", "RST"],
    "3-5-2":   ["GK", "LCB", "CB", "RCB", "LWB", "LCM", "CDM", "RCM", "RWB", "LST", "RST"],
    "4-2-3-1": ["GK", "LB", "LCB", "RCB", "RB", "LCDM", "RCDM", "CAM", "LW", "RW", "ST"],
    "3-4-3":   ["GK", "LCB", "CB", "RCB", "LWB", "LCM", "RCM", "RWB", "LW", "ST", "RW"],
    "3-4-2-1": ["GK", "LCB", "CB", "RCB", "LWB", "LCM", "RCM", "RWB", "LCAM", "RCAM", "ST"]
}

FORMATION_LIST = list(FORMATIONS.keys())

# -------------------------
# POSITION MAPPING (role -> preferred positions)
# -------------------------

POSITION_MAPPING = {
    "GK":   ["GK"],
    "LB":   ["LB", "LWB"],
    "RB":   ["RB", "RWB"],
    "LCB":  ["CB", "LB"],
    "RCB":  ["CB", "RB"],
    "CB":   ["CB"],
    "LWB":  ["LWB", "LB", "LM"],
    "RWB":  ["RWB", "RB", "RM"],
    "LCDM": ["CDM", "CM"],
    "RCDM": ["CDM", "CM"],
    "LCM":  ["CM", "CAM", "LM"],
    "RCM":  ["CM", "CAM", "RM"],
    "CM":   ["CM", "CDM", "CAM"],
    "CAM":  ["CAM", "CM"],
    "LCAM": ["CAM", "CM", "LM"],
    "RCAM": ["CAM", "CM", "RM"],
    "LW":   ["LW", "LM"],
    "RW":   ["RW", "RM"],
    "ST":   ["ST", "CF"],
    "LST":  ["ST", "CF"],
    "RST":  ["ST", "CF"]
}

# -------------------------
# FALLBACK ROLES (when no ideal match)
# -------------------------

FALLBACK_ROLES = {
    "LW":  ["RW", "ST"],
    "RW":  ["LW", "ST"],
    "ST":  ["CF"],
    "LST": ["ST", "CF"],
    "RST": ["ST", "CF"],
    "CAM": ["CM", "ST", "LW", "RW"],
    "LCM": ["CM", "CDM", "CAM"],
    "RCM": ["CM", "CDM", "CAM"],
    "CM":  ["LCM", "RCM", "CDM"],
    "CDM": ["CM", "CB"],
    "LWB": ["LB", "LM"],
    "RWB": ["RB", "RM"],
    "LB":  ["LWB", "CB"],
    "RB":  ["RWB", "CB"],
    "LCB": ["CB"],
    "RCB": ["CB"],
    "CB":  ["LCB", "RCB"]
}

# -------------------------
# TEAM COLORS
# -------------------------

TEAM_COLORS = {

    # =========================
    # PREMIER LEAGUE (FC 26)
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
    # SERIE A ENILIVE (FC 26)
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
    # LALIGA EA SPORTS (FC 26)
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
    # LIGUE 1 McDONALD'S (FC 26)
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
    # BUNDESLIGA (FC 26)
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
    # LIGA PORTUGAL (FC 26)
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
    # EREDIVISIE (FC 26)
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
    "left":  ["#E6FF00"],   # YELLOW
    "right": ["#7B1FA2"]    # PURPLE
}

# -------------------------
# FORMATION PITCH POSITIONS (x, y in 0-100 range)
# -------------------------

FORMATION_POSITIONS = {
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
        "LWB": (15, 50), "LCM": (35, 50), "CDM": (50, 45), "RCM": (65, 50), "RWB": (85, 50),
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

# -------------------------
# MISMATCH ANALYSIS CONFIG
# -------------------------

ROLE_ZONES = {
    "LEFT_WING":      ["LW", "LM", "LWB"],
    "RIGHT_WING":     ["RW", "RM", "RWB"],
    "CENTER_FORWARD": ["ST", "LST", "RST"],
    "ATTACKING_MID":  ["CAM", "LCAM", "RCAM"],
    "CENTRAL_MID":    ["CM", "LCM", "RCM", "CDM", "LCDM", "RCDM"],
    "CENTER_BACK":    ["CB", "LCB", "RCB"],
    "LEFT_DEF":       ["LB", "LCB"],
    "RIGHT_DEF":      ["RB", "RCB"]
}

MATCHUPS = {
    "LEFT_WING":      ["RIGHT_DEF"],
    "RIGHT_WING":     ["LEFT_DEF"],
    "CENTER_FORWARD": ["CENTER_BACK"],
    "ATTACKING_MID":  ["CENTRAL_MID"]
}

MISMATCH_THRESHOLD = 4

# -------------------------
# LLM CONFIG
# -------------------------

LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.45

SYSTEM_PROMPT = """
You are an elite football tactical analyst assisting a professional coaching staff.

BEHAVIOUR
- Think step by step from data to tactics.
- Base every conclusion strictly on the provided lineups and mismatches.
- Prefer structured bullet points over long paragraphs.
- Be concise, concrete, and realistic.

DECISION PRIORITY
1. Exploit clear physical or positional mismatches.
2. Protect structural weaknesses when attacking.
3. Maintain rest-defense and counter-pressing security.
4. Suggest substitutions ONLY if they solve a specific tactical problem.

CONSTRAINTS
- Do NOT invent players.
- Use ONLY the listed bench players.
- Do NOT repeat starting lineups unless asked.
- Do NOT change formation unless strictly necessary.
- If information is missing, say so explicitly.

OUTPUT STYLE
- Clear section headers.
- Bullet points with short tactical reasoning.
- No generic football clichés.
"""

# -------------------------
# PITCH DRAWING
# -------------------------

PITCH_BG_COLOR = "#2e7d32"
PITCH_LINE_COLOR = "white"
PITCH_LINE_WIDTH = 2
