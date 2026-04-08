import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# Part (b) – Database setup
# ─────────────────────────────────────────────
DB_NAME = "microscope.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    NOT NULL,
            specimen        TEXT    NOT NULL,
            microscope_size REAL    NOT NULL,
            magnification   REAL    NOT NULL,
            actual_size     REAL    NOT NULL,
            unit            TEXT    NOT NULL,
            timestamp       TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_record(username, specimen, microscope_size, magnification, actual_size, unit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO records (username, specimen, microscope_size, magnification, actual_size, unit, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, specimen, microscope_size, magnification, actual_size, unit,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_records(username=None):
    conn = sqlite3.connect(DB_NAME)
    if username:
        df = pd.read_sql_query(
            "SELECT * FROM records WHERE username = ? ORDER BY timestamp DESC",
            conn, params=(username,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM records ORDER BY timestamp DESC", conn
        )
    conn.close()
    return df

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# Part (a) – Core calculation
# ─────────────────────────────────────────────
def calculate_actual_size(microscope_size: float, magnification: float) -> float:
    """Actual (real) size = Microscope (image) size / Magnification"""
    if magnification == 0:
        raise ValueError("Magnification cannot be zero.")
    return microscope_size / magnification

# ─────────────────────────────────────────────
# SVG Assets – Biology illustrations
# ─────────────────────────────────────────────

MICROSCOPE_SVG = """
<svg viewBox="0 0 160 260" xmlns="http://www.w3.org/2000/svg" width="140" height="220">
  <ellipse cx="80" cy="245" rx="52" ry="10" fill="#1a3a2a" opacity="0.6"/>
  <rect x="42" y="228" width="76" height="18" rx="6" fill="#2d6a4f"/>
  <rect x="70" y="100" width="20" height="130" rx="5" fill="#40916c"/>
  <rect x="48" y="98" width="64" height="14" rx="5" fill="#52b788"/>
  <rect x="38" y="155" width="84" height="10" rx="3" fill="#74c69d"/>
  <rect x="44" y="148" width="8" height="18" rx="2" fill="#95d5b2"/>
  <rect x="108" y="148" width="8" height="18" rx="2" fill="#95d5b2"/>
  <ellipse cx="40" cy="170" rx="12" ry="7" fill="#52b788"/>
  <ellipse cx="40" cy="170" rx="9" ry="5" fill="#40916c"/>
  <ellipse cx="120" cy="170" rx="9" ry="5" fill="#52b788"/>
  <rect x="68" y="42" width="24" height="58" rx="5" fill="#2d6a4f"/>
  <rect x="64" y="22" width="32" height="24" rx="6" fill="#1b4332"/>
  <ellipse cx="80" cy="22" rx="14" ry="6" fill="#081c15"/>
  <ellipse cx="80" cy="22" rx="9" ry="4" fill="#52b788" opacity="0.5"/>
  <ellipse cx="80" cy="100" rx="18" ry="7" fill="#1b4332"/>
  <rect x="77" y="100" width="6" height="28" rx="3" fill="#081c15"/>
  <rect x="63" y="108" width="5" height="22" rx="2.5" fill="#1b4332"/>
  <rect x="92" y="108" width="5" height="18" rx="2.5" fill="#1b4332"/>
  <ellipse cx="80" cy="228" rx="10" ry="4" fill="#d8f3dc" opacity="0.7"/>
  <polygon points="75,160 85,160 83,228 77,228" fill="#d8f3dc" opacity="0.12"/>
  <ellipse cx="74" cy="20" rx="3" ry="2" fill="white" opacity="0.4"/>
</svg>
"""

CELL_PLANT_SVG = """
<svg viewBox="0 0 100 80" xmlns="http://www.w3.org/2000/svg" width="90" height="72">
  <rect x="5" y="5" width="90" height="70" rx="4" fill="none" stroke="#52b788" stroke-width="2.5"/>
  <line x1="52" y1="5" x2="52" y2="75" stroke="#52b788" stroke-width="1.5" opacity="0.5"/>
  <line x1="5" y1="38" x2="95" y2="38" stroke="#52b788" stroke-width="1.5" opacity="0.5"/>
  <ellipse cx="28" cy="22" rx="12" ry="9" fill="none" stroke="#95d5b2" stroke-width="1.5"/>
  <ellipse cx="28" cy="22" rx="5" ry="4" fill="#40916c" opacity="0.7"/>
  <ellipse cx="44" cy="14" rx="5" ry="3" fill="#2d6a4f" opacity="0.9"/>
  <ellipse cx="14" cy="30" rx="4" ry="2.5" fill="#2d6a4f" opacity="0.9"/>
  <ellipse cx="74" cy="20" rx="11" ry="8" fill="none" stroke="#95d5b2" stroke-width="1.5"/>
  <ellipse cx="74" cy="20" rx="4.5" ry="3.5" fill="#40916c" opacity="0.7"/>
  <ellipse cx="88" cy="30" rx="4" ry="2.5" fill="#2d6a4f" opacity="0.9"/>
  <ellipse cx="26" cy="58" rx="11" ry="8" fill="none" stroke="#95d5b2" stroke-width="1.5"/>
  <ellipse cx="26" cy="58" rx="4.5" ry="3.5" fill="#40916c" opacity="0.7"/>
  <ellipse cx="74" cy="58" rx="12" ry="9" fill="none" stroke="#95d5b2" stroke-width="1.5"/>
  <ellipse cx="74" cy="58" rx="5" ry="4" fill="#40916c" opacity="0.7"/>
  <ellipse cx="62" cy="66" rx="4" ry="2.5" fill="#2d6a4f" opacity="0.9"/>
  <ellipse cx="86" cy="48" rx="4" ry="2.5" fill="#2d6a4f" opacity="0.9"/>
</svg>
"""

BACTERIA_SVG = """
<svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg" width="110" height="72">
  <rect x="8" y="30" width="28" height="12" rx="6" fill="#52b788" opacity="0.85"/>
  <ellipse cx="22" cy="36" rx="4" ry="3" fill="#1b4332" opacity="0.6"/>
  <path d="M8,34 Q0,28 4,22 Q8,16 4,10" fill="none" stroke="#74c69d" stroke-width="1.2"/>
  <path d="M8,38 Q2,42 6,48" fill="none" stroke="#74c69d" stroke-width="1.2"/>
  <circle cx="62" cy="20" r="9" fill="#40916c" opacity="0.85"/>
  <ellipse cx="60" cy="18" rx="3" ry="2.5" fill="#1b4332" opacity="0.6"/>
  <circle cx="78" cy="18" r="9" fill="#40916c" opacity="0.85"/>
  <ellipse cx="76" cy="16" rx="3" ry="2.5" fill="#1b4332" opacity="0.6"/>
  <circle cx="70" cy="32" r="9" fill="#40916c" opacity="0.85"/>
  <ellipse cx="68" cy="30" rx="3" ry="2.5" fill="#1b4332" opacity="0.6"/>
  <path d="M90,55 Q95,48 100,55 Q105,62 110,55 Q115,48 118,52"
        fill="none" stroke="#52b788" stroke-width="4" stroke-linecap="round"/>
  <circle cx="90" cy="55" r="3" fill="#40916c"/>
  <circle cx="118" cy="52" r="2" fill="#40916c"/>
  <rect x="15" y="58" width="22" height="10" rx="5" fill="#74c69d" opacity="0.75"/>
  <ellipse cx="26" cy="63" rx="3.5" ry="2.5" fill="#1b4332" opacity="0.5"/>
  <text x="4"  y="76" font-size="7" fill="#95d5b2" font-family="monospace">Bacillus</text>
  <text x="58" y="76" font-size="7" fill="#95d5b2" font-family="monospace">Cocci</text>
  <text x="90" y="76" font-size="7" fill="#95d5b2" font-family="monospace">Spiral</text>
</svg>
"""

AMOEBA_SVG = """
<svg viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" width="90" height="80">
  <path d="M50,10 Q70,5 80,20 Q92,30 88,48 Q90,65 75,72 Q60,82 45,75 Q28,78 18,65 Q8,52 12,36 Q14,20 28,14 Q38,8 50,10Z"
        fill="#40916c" opacity="0.5" stroke="#52b788" stroke-width="1.5"/>
  <path d="M80,20 Q95,12 90,6"   fill="none" stroke="#40916c" stroke-width="5" stroke-linecap="round" opacity="0.6"/>
  <path d="M88,48 Q100,44 102,52" fill="none" stroke="#40916c" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
  <path d="M18,65 Q8,72 10,80"   fill="none" stroke="#40916c" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
  <path d="M28,14 Q20,4 14,8"    fill="none" stroke="#40916c" stroke-width="3.5" stroke-linecap="round" opacity="0.6"/>
  <ellipse cx="50" cy="42" rx="16" ry="12" fill="none" stroke="#95d5b2" stroke-width="1.8"/>
  <ellipse cx="50" cy="42" rx="7"  ry="5"  fill="#1b4332" opacity="0.8"/>
  <circle cx="34" cy="32" r="5"  fill="none" stroke="#74c69d" stroke-width="1.2"/>
  <circle cx="66" cy="58" r="6"  fill="none" stroke="#74c69d" stroke-width="1.2"/>
  <circle cx="38" cy="60" r="4"  fill="none" stroke="#74c69d" stroke-width="1"/>
  <circle cx="65" cy="30" r="4"  fill="#d8f3dc" opacity="0.5" stroke="#95d5b2" stroke-width="1"/>
  <text x="30" y="88" font-size="8" fill="#95d5b2" font-family="monospace">Amoeba</text>
</svg>
"""

CHEEK_CELL_SVG = """
<svg viewBox="0 0 100 80" xmlns="http://www.w3.org/2000/svg" width="90" height="72">
  <path d="M50,8 Q68,6 78,18 Q88,32 84,50 Q80,66 62,72 Q44,78 30,68 Q16,58 14,42 Q10,24 24,14 Q36,6 50,8Z"
        fill="#2d6a4f" opacity="0.4" stroke="#52b788" stroke-width="1.5"/>
  <path d="M50,8 Q54,12 52,16"   fill="none" stroke="#74c69d" stroke-width="0.8" opacity="0.6"/>
  <path d="M78,18 Q76,24 80,28"  fill="none" stroke="#74c69d" stroke-width="0.8" opacity="0.6"/>
  <path d="M14,42 Q18,44 16,50"  fill="none" stroke="#74c69d" stroke-width="0.8" opacity="0.6"/>
  <ellipse cx="50" cy="40" rx="18" ry="15" fill="#1b4332" opacity="0.7" stroke="#95d5b2" stroke-width="1.5"/>
  <ellipse cx="48" cy="38" rx="6"  ry="5"  fill="#40916c" opacity="0.9"/>
  <circle cx="30" cy="28" r="2"   fill="#52b788" opacity="0.5"/>
  <circle cx="72" cy="32" r="1.5" fill="#52b788" opacity="0.5"/>
  <circle cx="68" cy="58" r="2"   fill="#52b788" opacity="0.5"/>
  <circle cx="28" cy="56" r="1.5" fill="#52b788" opacity="0.5"/>
  <circle cx="40" cy="22" r="1"   fill="#52b788" opacity="0.5"/>
  <text x="22" y="78" font-size="7.5" fill="#95d5b2" font-family="monospace">Cheek Cell</text>
</svg>
"""

ONION_CELL_SVG = """
<svg viewBox="0 0 110 80" xmlns="http://www.w3.org/2000/svg" width="100" height="72">
  <rect x="5"  y="8"  width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="21" cy="22" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="21" cy="22" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <rect x="39" y="8"  width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="55" cy="22" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="55" cy="22" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <rect x="73" y="8"  width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="89" cy="22" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="89" cy="22" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <rect x="5"  y="38" width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="21" cy="52" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="21" cy="52" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <rect x="39" y="38" width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="55" cy="52" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="55" cy="52" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <rect x="73" y="38" width="32" height="28" rx="2" fill="#2d6a4f" opacity="0.35" stroke="#52b788" stroke-width="1.8"/>
  <ellipse cx="89" cy="52" rx="8" ry="6" fill="none" stroke="#95d5b2" stroke-width="1.2"/>
  <ellipse cx="89" cy="52" rx="3" ry="2.5" fill="#40916c" opacity="0.8"/>
  <text x="22" y="76" font-size="7.5" fill="#95d5b2" font-family="monospace">Onion Cells</text>
</svg>
"""


def eyepiece_result_svg(actual, unit_short, specimen, microscope_size, magnification):
    """Circular eyepiece-style result display."""
    return f"""
<div style="display:flex; justify-content:center; margin: 1.2rem 0;">
<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" width="300" height="300">
  <circle cx="150" cy="150" r="145" fill="#0a1f14" stroke="#40916c" stroke-width="6"/>
  <circle cx="150" cy="150" r="130" fill="#061209"/>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%"   stop-color="#52b788" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="#061209" stop-opacity="0"/>
  </radialGradient>
  <circle cx="150" cy="150" r="130" fill="url(#glow)"/>
  <line x1="20"  y1="150" x2="280" y2="150" stroke="#40916c" stroke-width="0.8" opacity="0.6"/>
  <line x1="150" y1="20"  x2="150" y2="280" stroke="#40916c" stroke-width="0.8" opacity="0.6"/>
  <circle cx="150" cy="150" r="50"  fill="none" stroke="#2d6a4f" stroke-width="0.7" opacity="0.7"/>
  <circle cx="150" cy="150" r="90"  fill="none" stroke="#2d6a4f" stroke-width="0.7" opacity="0.5"/>
  <circle cx="150" cy="150" r="118" fill="none" stroke="#2d6a4f" stroke-width="0.7" opacity="0.3"/>
  <line x1="60"  y1="147" x2="60"  y2="153" stroke="#52b788" stroke-width="1.2"/>
  <line x1="90"  y1="147" x2="90"  y2="153" stroke="#52b788" stroke-width="1.2"/>
  <line x1="120" y1="146" x2="120" y2="154" stroke="#52b788" stroke-width="1.5"/>
  <line x1="180" y1="146" x2="180" y2="154" stroke="#52b788" stroke-width="1.5"/>
  <line x1="210" y1="147" x2="210" y2="153" stroke="#52b788" stroke-width="1.2"/>
  <line x1="240" y1="147" x2="240" y2="153" stroke="#52b788" stroke-width="1.2"/>
  <circle cx="150" cy="150" r="3" fill="#95d5b2"/>
  <text x="150" y="130" text-anchor="middle" font-size="13" fill="#74c69d"
        font-family="monospace" opacity="0.9">{specimen}</text>
  <text x="150" y="163" text-anchor="middle" font-size="30" fill="#d8f3dc"
        font-family="monospace" font-weight="bold">{actual:.5f}</text>
  <text x="150" y="184" text-anchor="middle" font-size="16" fill="#95d5b2"
        font-family="monospace">{unit_short}</text>
  <text x="150" y="210" text-anchor="middle" font-size="9.5" fill="#52b788"
        font-family="monospace">img: {microscope_size} {unit_short}  |  x{int(magnification)}</text>
  <ellipse cx="100" cy="80" rx="18" ry="10" fill="white" opacity="0.04" transform="rotate(-30 100 80)"/>
  <circle cx="150" cy="150" r="145" fill="none" stroke="#74c69d" stroke-width="1.5" opacity="0.3"/>
</svg>
</div>
"""


# ─────────────────────────────────────────────
# Part (c/d) – Web-based GUI via Streamlit
# ─────────────────────────────────────────────
def main():
    init_db()

    st.set_page_config(
        page_title="BioScope | Microscope Size Calculator",
        page_icon="🔬",
        layout="wide"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Nunito:wght@300;400;600&display=swap');

    html, body, [class*="css"], .stApp {
        background-color: #061209 !important;
        color: #d8f3dc !important;
        font-family: 'Nunito', sans-serif !important;
    }
    h1,h2,h3,h4 { font-family:'Rajdhani',sans-serif !important; color:#95d5b2 !important; letter-spacing:1px; }

    .stTabs [data-baseweb="tab-list"] { background:#0a1f14 !important; border-radius:8px; padding:4px; }
    .stTabs [data-baseweb="tab"]      { color:#74c69d !important; font-family:'Share Tech Mono',monospace !important; }
    .stTabs [aria-selected="true"]    { background:#1b4332 !important; border-radius:6px !important; color:#d8f3dc !important; }

    .stTextInput input, .stNumberInput input {
        background:#0d2218 !important; color:#d8f3dc !important;
        border:1px solid #2d6a4f !important; border-radius:6px !important;
        font-family:'Share Tech Mono',monospace !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color:#74c69d !important; font-weight:600;
    }
    div[data-baseweb="select"] > div {
        background:#0d2218 !important; border-color:#2d6a4f !important; color:#d8f3dc !important;
    }

    .stButton > button {
        background:linear-gradient(135deg,#1b4332,#2d6a4f) !important;
        color:#d8f3dc !important; border:1.5px solid #52b788 !important;
        border-radius:8px !important; font-family:'Rajdhani',sans-serif !important;
        font-size:1rem !important; font-weight:700 !important; letter-spacing:1.5px !important;
    }
    .stButton > button:hover {
        background:linear-gradient(135deg,#2d6a4f,#40916c) !important;
        border-color:#95d5b2 !important; transform:translateY(-2px) !important;
        box-shadow:0 4px 18px rgba(82,183,136,0.3) !important;
    }

    [data-testid="stSidebar"]         { background:#0a1f14 !important; border-right:1px solid #1b4332; }
    [data-testid="stMetric"]          { background:#0d2218 !important; border:1px solid #2d6a4f !important; border-radius:8px !important; padding:0.6rem 1rem !important; }
    [data-testid="stMetricValue"]     { color:#95d5b2 !important; font-family:'Share Tech Mono',monospace !important; }
    [data-testid="stMetricLabel"]     { color:#74c69d !important; }
    .stDataFrame                      { border:1px solid #2d6a4f !important; border-radius:8px; }
    hr                                { border-color:#1b4332 !important; }
    .stCaption                        { color:#52b788 !important; font-family:'Share Tech Mono',monospace !important; }
    .streamlit-expanderHeader         { background:#0d2218 !important; color:#74c69d !important; border:1px solid #2d6a4f !important; border-radius:6px !important; font-family:'Share Tech Mono',monospace !important; }
    .stCheckbox label                 { color:#74c69d !important; }
    .stDownloadButton > button        { background:#0d2218 !important; border:1px solid #40916c !important; color:#95d5b2 !important; font-family:'Share Tech Mono',monospace !important; }

    .formula-card {
        background:#0d2218; border:1px solid #2d6a4f; border-left:5px solid #52b788;
        border-radius:8px; padding:1rem 1.4rem;
        font-family:'Share Tech Mono',monospace; font-size:1rem; color:#95d5b2; margin-bottom:1.2rem;
    }
    .formula-card span { color:#d8f3dc; font-size:1.1rem; }
    .bio-card {
        background:#0d2218; border:1px solid #2d6a4f; border-radius:10px;
        padding:0.8rem 1rem; margin:0.5rem 0; font-size:0.82rem; color:#74c69d; line-height:1.6;
    }
    .bio-card strong { color:#95d5b2; }
    .specimen-label { font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:#52b788; margin-bottom:0.3rem; }
    .page-header {
        background:linear-gradient(135deg,#0d2218 0%,#1b4332 100%);
        border:1px solid #2d6a4f; border-radius:14px; padding:1.5rem 2rem; margin-bottom:1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="display:flex;justify-content:center;margin-bottom:0.5rem;">{MICROSCOPE_SVG}</div>
        <div style="text-align:center;font-family:'Rajdhani',sans-serif;font-size:1.3rem;
                    color:#95d5b2;letter-spacing:2px;margin-bottom:1rem;">BIOSCOPE LAB</div>
        """, unsafe_allow_html=True)
        st.divider()

        st.markdown("### 👤 User Login")
        username = st.text_input("Username", placeholder="e.g. temmy123", label_visibility="collapsed")
        if not username.strip():
            st.markdown('<p style="color:#52b788;font-family:monospace;font-size:0.8rem;">⚠ Enter username to continue</p>',
                        unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🔭 Specimen Gallery")
        st.markdown(f"""
        <div style="margin:0.3rem 0 0.2rem 0;">
            <div class="specimen-label">🌿 Plant cells</div>
            {ONION_CELL_SVG}
        </div>
        <div style="margin:0.6rem 0 0.2rem 0;">
            <div class="specimen-label">🧫 Human cell</div>
            {CHEEK_CELL_SVG}
        </div>
        <div style="margin:0.6rem 0 0.2rem 0;">
            <div class="specimen-label">🦠 Bacteria types</div>
            {BACTERIA_SVG}
        </div>
        <div style="margin:0.6rem 0 0.2rem 0;">
            <div class="specimen-label">🔵 Protozoa</div>
            {AMOEBA_SVG}
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("""
        <div class="bio-card">
        <strong>📐 Formula</strong><br>
        Actual Size = Image Size ÷ Magnification<br><br>
        <strong>Common Magnifications:</strong><br>
        • 4× obj &nbsp;→ ×40 total<br>
        • 10× obj → ×100 total<br>
        • 40× obj → ×400 total<br>
        • 100× obj → ×1000 total
        </div>
        """, unsafe_allow_html=True)

    # ── Stop if no username ──────────────────────
    if not username.strip():
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;">
            <div style="font-size:5rem;">🔬</div>
            <h2 style="color:#52b788;font-family:Rajdhani,sans-serif;letter-spacing:2px;">
                WELCOME TO BIOSCOPE LAB
            </h2>
            <p style="color:#40916c;font-family:monospace;">
                Enter your username in the sidebar to begin your specimen analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Page Header ───────────────────────────────
    st.markdown(f"""
    <div class="page-header" style="display:flex;align-items:center;gap:1.5rem;">
        <div style="font-size:3.5rem;line-height:1;">🔬</div>
        <div>
            <h1 style="margin:0 0 0.2rem 0;font-size:2.4rem!important;color:#d8f3dc!important;">BioScope Lab</h1>
            <p style="margin:0;color:#74c69d;font-family:'Share Tech Mono',monospace;font-size:0.85rem;">
                CSC 442 — Bioinformatics &nbsp;|&nbsp; Specimen Size Calculator &nbsp;|&nbsp;
                Analyst: <strong style="color:#d8f3dc;">{username}</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-card">
        🧬 &nbsp; <span>Actual Size</span> &nbsp;=&nbsp;
        <span>Microscope (Image) Size</span> &nbsp;÷&nbsp; <span>Magnification</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────
    tab1, tab2 = st.tabs(["🧫  CALCULATE SPECIMEN SIZE", "🗂  MY SPECIMEN RECORDS"])

    # ─── Tab 1: Calculator ────────────────────────
    with tab1:
        left_col, right_col = st.columns([1.1, 1], gap="large")

        with left_col:
            st.markdown("#### 🧪 Specimen Details")
            specimen = st.text_input(
                "Specimen Name",
                placeholder="e.g. Onion Epidermal Cell, E. coli, Amoeba proteus"
            )

            st.markdown('<p class="specimen-label">⚡ Quick fill common specimens:</p>', unsafe_allow_html=True)
            qc1, qc2, qc3, qc4 = st.columns(4)
            with qc1:
                if st.button("🌿 Onion"):
                    st.session_state["_spec"] = "Onion Cell"
            with qc2:
                if st.button("🧫 Cheek"):
                    st.session_state["_spec"] = "Cheek Cell"
            with qc3:
                if st.button("🦠 E.coli"):
                    st.session_state["_spec"] = "E. coli"
            with qc4:
                if st.button("🔵 Amoeba"):
                    st.session_state["_spec"] = "Amoeba"

            if "_spec" in st.session_state and not specimen:
                specimen = st.session_state["_spec"]
                st.caption(f"Using: {specimen}")

            st.markdown("---")
            st.markdown("#### 🔭 Microscope Settings")

            mc1, mc2 = st.columns(2)
            with mc1:
                microscope_size = st.number_input(
                    "Image Size (under microscope)",
                    min_value=0.0001, value=2.0, step=0.1, format="%.4f",
                    help="Measured size of specimen through the eyepiece"
                )
            with mc2:
                unit = st.selectbox(
                    "Unit",
                    ["µm (micrometres)", "mm (millimetres)", "nm (nanometres)", "cm (centimetres)"]
                )
            unit_short = unit.split(" ")[0]

            magnification = st.number_input(
                "Total Magnification (×)",
                min_value=1.0, value=400.0, step=10.0,
                help="Eyepiece × Objective lens"
            )

            st.markdown('<p class="specimen-label">🔢 Magnification helper (eyepiece × objective):</p>',
                        unsafe_allow_html=True)
            hc1, hc2 = st.columns(2)
            with hc1:
                eyepiece  = st.selectbox("Eyepiece", [5, 10, 15, 20], index=1)
            with hc2:
                objective = st.selectbox("Objective", [4, 10, 40, 100], index=2)
            st.markdown(
                f'<p style="color:#52b788;font-family:monospace;font-size:0.85rem;">→ Total = ×{eyepiece * objective}</p>',
                unsafe_allow_html=True
            )

            calc_btn = st.button("🔬 ANALYSE SPECIMEN", use_container_width=True)

        with right_col:
            st.markdown("#### 🔍 Eyepiece View")

            if calc_btn:
                active_specimen = specimen.strip() or st.session_state.get("_spec", "")
                if not active_specimen:
                    st.error("⚠️ Please enter or select a specimen name first.")
                else:
                    actual = calculate_actual_size(microscope_size, magnification)
                    st.markdown(
                        eyepiece_result_svg(actual, unit_short, active_specimen, microscope_size, magnification),
                        unsafe_allow_html=True
                    )
                    save_record(username.strip(), active_specimen, microscope_size, magnification, actual, unit_short)
                    st.success("✅ Specimen record saved to database!")

                    with st.expander("📋 Full Analysis Breakdown"):
                        st.markdown(f"""
| Parameter | Value |
|-----------|-------|
| 🧫 Specimen | {active_specimen} |
| 📏 Image size | {microscope_size} {unit_short} |
| 🔭 Magnification | ×{magnification:,.0f} |
| ✅ **Actual size** | **{actual:.6f} {unit_short}** |
| 👤 Analyst | {username} |
| 🕐 Time | {datetime.now().strftime('%Y-%m-%d %H:%M')} |
                        """)

                    st.markdown("""
                    <div class="bio-card">
                    <strong>🧬 Did you know?</strong><br>
                    A typical human cheek cell is ~60 µm wide, an onion epidermal cell ~250 µm,
                    <em>E. coli</em> bacteria ~2 µm long, and a human red blood cell ~7–8 µm in diameter.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Idle eyepiece
                st.markdown("""
                <div style="display:flex;justify-content:center;margin-top:0.5rem;">
                <svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" width="290" height="290">
                  <circle cx="150" cy="150" r="145" fill="#0a1f14" stroke="#1b4332" stroke-width="5"/>
                  <circle cx="150" cy="150" r="130" fill="#061209"/>
                  <line x1="20"  y1="150" x2="280" y2="150" stroke="#1b4332" stroke-width="0.8"/>
                  <line x1="150" y1="20"  x2="150" y2="280" stroke="#1b4332" stroke-width="0.8"/>
                  <circle cx="150" cy="150" r="50"  fill="none" stroke="#0d2218" stroke-width="1"/>
                  <circle cx="150" cy="150" r="90"  fill="none" stroke="#0d2218" stroke-width="1"/>
                  <circle cx="150" cy="150" r="118" fill="none" stroke="#0d2218" stroke-width="1"/>
                  <circle cx="150" cy="150" r="3" fill="#1b4332"/>
                  <text x="150" y="145" text-anchor="middle" font-size="11" fill="#2d6a4f"
                        font-family="monospace">Awaiting specimen...</text>
                  <text x="150" y="163" text-anchor="middle" font-size="9"  fill="#1b4332"
                        font-family="monospace">Fill in details and click ANALYSE</text>
                </svg>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown('<p class="specimen-label" style="text-align:center;">🔬 Common specimens under the microscope</p>',
                            unsafe_allow_html=True)
                ic1, ic2 = st.columns(2)
                with ic1:
                    st.markdown(f'<div style="display:flex;justify-content:center;">{CELL_PLANT_SVG}</div>',
                                unsafe_allow_html=True)
                    st.markdown('<p style="text-align:center;font-family:monospace;font-size:0.7rem;color:#52b788;">Plant Cell (×400)</p>',
                                unsafe_allow_html=True)
                with ic2:
                    st.markdown(f'<div style="display:flex;justify-content:center;">{AMOEBA_SVG}</div>',
                                unsafe_allow_html=True)
                    st.markdown('<p style="text-align:center;font-family:monospace;font-size:0.7rem;color:#52b788;">Amoeba (×100)</p>',
                                unsafe_allow_html=True)

    # ─── Tab 2: Records ───────────────────────────
    with tab2:
        st.markdown(f"#### 🗂️ Specimen Records — **{username}**")
        show_all = st.checkbox("🔓 Show all users (admin view)")
        df = fetch_records(None if show_all else username.strip())

        if df.empty:
            st.markdown("""
            <div style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;">🧫</div>
                <p style="color:#2d6a4f;font-family:monospace;">
                    No specimens analysed yet.<br>Head to the CALCULATE tab to begin.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            display_df = df.rename(columns={
                "id": "ID", "username": "Analyst", "specimen": "Specimen",
                "microscope_size": "Image Size", "magnification": "Magnification (×)",
                "actual_size": "Actual Size", "unit": "Unit", "timestamp": "Timestamp"
            })
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.markdown("#### 📊 Lab Statistics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("🧫 Total Analyses",   len(df))
            m2.metric("📏 Avg Actual Size",   f"{df['actual_size'].mean():.5f}")
            m3.metric("📋 Unique Specimens",  df['specimen'].nunique())
            m4.metric("👥 Analysts",          df['username'].nunique())

            st.markdown("---")
            col_del, col_dl = st.columns(2)
            with col_del:
                st.markdown("#### 🗑️ Remove Record")
                del_id = st.selectbox("Select Record ID", df["id"].tolist())
                if st.button("Delete Record", type="secondary"):
                    delete_record(del_id)
                    st.success(f"Record #{del_id} removed.")
                    st.rerun()
            with col_dl:
                st.markdown("#### ⬇️ Export Data")
                st.markdown("<br>", unsafe_allow_html=True)
                csv = display_df.to_csv(index=False)
                st.download_button(
                    "⬇️ Download as CSV",
                    data=csv,
                    file_name=f"bioscope_{username}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    st.divider()
    st.caption("🔬 BioScope Lab  ·  CSC 442 Bioinformatics  ·  Assignment Q5 (a–e)  ·  Built with Python + Streamlit")


if __name__ == "__main__":
    main()