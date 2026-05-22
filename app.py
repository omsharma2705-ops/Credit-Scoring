import streamlit as st
import pandas as pd
import pickle
import numpy as np
import math

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CreditLens · AI Risk Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Instrument+Sans:wght@300;400;500;600&display=swap');

/* ─── VARIABLES ─── */
:root {
  --bg:          #040812;
  --bg2:         #080f1f;
  --surface:     rgba(255,255,255,0.04);
  --surface-h:   rgba(255,255,255,0.07);
  --border:      rgba(255,255,255,0.08);
  --border-h:    rgba(255,255,255,0.18);
  --gold:        #f5c842;
  --gold2:       #ffaa00;
  --cyan:        #00e5ff;
  --violet:      #7c3aed;
  --rose:        #f43f5e;
  --green:       #10b981;
  --text:        #f1f5f9;
  --muted:       #64748b;
  --muted2:      #94a3b8;
  --radius:      20px;
  --radius-sm:   12px;
}

/* ─── GLOBAL ─── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, [class*="css"] {
  font-family: 'Instrument Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* animated mesh background */
.stApp::before {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 80% 60% at 10% 10%,  rgba(124,58,237,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 80%,  rgba(0,229,255,0.08)  0%, transparent 60%),
    radial-gradient(ellipse 50% 50% at 50% 50%,  rgba(245,200,66,0.04) 0%, transparent 70%);
  animation: meshMove 18s ease-in-out infinite alternate;
}
@keyframes meshMove {
  0%   { opacity: 1; transform: scale(1)   rotate(0deg); }
  50%  { opacity: 0.8; transform: scale(1.05) rotate(1deg); }
  100% { opacity: 1; transform: scale(1)   rotate(0deg); }
}

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"] { display: none !important; }

/* ─── SIDEBAR COLLAPSE ─── */
[data-testid="stSidebar"] { display: none !important; }

/* ─── BLOCK CONTAINER ─── */
.block-container {
  max-width: 1100px !important;
  padding: 40px 32px !important;
  position: relative; z-index: 1;
}

/* ══════════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════════ */
.hero {
  text-align: center;
  padding: 48px 0 40px;
  position: relative;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(245,200,66,0.1);
  border: 1px solid rgba(245,200,66,0.25);
  border-radius: 100px;
  padding: 6px 18px;
  font-size: 0.72rem; font-weight: 600;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--gold); margin-bottom: 24px;
}
.hero-badge .dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--gold);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(1.4); }
}
.hero h1 {
  font-family: 'Syne', sans-serif !important;
  font-size: clamp(2.2rem, 5vw, 3.6rem) !important;
  font-weight: 800 !important;
  line-height: 1.05 !important;
  letter-spacing: -0.03em !important;
  color: var(--text) !important;
  margin-bottom: 16px !important;
}
.hero h1 span {
  background: linear-gradient(135deg, var(--gold), var(--cyan));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p {
  font-size: 1rem; color: var(--muted2); max-width: 520px;
  margin: 0 auto; line-height: 1.7;
}

/* ══════════════════════════════════════════════
   STEPPER
══════════════════════════════════════════════ */
.stepper {
  display: flex; align-items: center; justify-content: center;
  gap: 0; margin: 36px 0 40px;
}
.step-item { display: flex; align-items: center; gap: 0; }
.step-circle {
  width: 42px; height: 42px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem;
  transition: all 0.3s ease; flex-shrink: 0;
}
.step-circle.active {
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  color: #000; box-shadow: 0 0 24px rgba(245,200,66,0.45);
}
.step-circle.done {
  background: linear-gradient(135deg, var(--green), #34d399);
  color: #000;
}
.step-circle.idle {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--muted);
}
.step-label {
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em;
  text-transform: uppercase; margin-left: 10px;
  color: var(--muted2);
}
.step-label.active { color: var(--gold); }
.step-label.done   { color: var(--green); }
.step-connector {
  width: 60px; height: 1px;
  background: linear-gradient(90deg, var(--border), var(--border-h), var(--border));
  margin: 0 8px;
}

/* ══════════════════════════════════════════════
   GLASS CARD
══════════════════════════════════════════════ */
.glass-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  padding: 32px;
  margin-bottom: 20px;
  transition: border-color 0.3s;
}
.glass-card:hover { border-color: var(--border-h); }

.card-header {
  display: flex; align-items: center; gap: 14px; margin-bottom: 28px;
}
.card-icon {
  width: 44px; height: 44px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.card-icon.gold   { background: rgba(245,200,66,0.12); border: 1px solid rgba(245,200,66,0.2); }
.card-icon.cyan   { background: rgba(0,229,255,0.1);   border: 1px solid rgba(0,229,255,0.2);  }
.card-icon.violet { background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.2); }
.card-icon.rose   { background: rgba(244,63,94,0.12);  border: 1px solid rgba(244,63,94,0.2);  }
.card-icon.green  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.2); }

.card-header-text h3 {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.05rem !important; font-weight: 700 !important;
  color: var(--text) !important; margin: 0 !important;
}
.card-header-text p {
  font-size: 0.78rem; color: var(--muted); margin: 3px 0 0 !important;
}

/* ══════════════════════════════════════════════
   FIELD LABELS (override streamlit)
══════════════════════════════════════════════ */
label, .stSelectbox label, .stNumberInput label,
.stSlider label, [data-testid="stWidgetLabel"] {
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.78rem !important; font-weight: 600 !important;
  letter-spacing: 0.05em !important; text-transform: uppercase !important;
  color: var(--muted2) !important; margin-bottom: 6px !important;
}

/* ─── Inputs ─── */
input[type="number"],
.stNumberInput input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 1rem !important; font-weight: 600 !important;
  padding: 12px 16px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type="number"]:focus,
.stNumberInput input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(245,200,66,0.12) !important;
  outline: none !important;
}

/* ─── Selectbox ─── */
div[data-baseweb="select"] > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-weight: 500 !important;
  transition: border-color 0.2s !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--border-h) !important; }
div[data-baseweb="popover"] { background: #111827 !important; }
li[role="option"]:hover { background: rgba(245,200,66,0.1) !important; }

/* ─── Slider ─── */
.stSlider > div > div > div {
  background: linear-gradient(90deg, var(--gold), var(--gold2)) !important;
}
.stSlider [data-testid="stThumbValue"] { display: none; }

/* ══════════════════════════════════════════════
   PAYMENT STATUS CHIP GRID
══════════════════════════════════════════════ */
.pay-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
  margin-top: 4px;
}
.pay-item { display: flex; flex-direction: column; gap: 6px; }
.pay-month {
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--muted);
}

/* ══════════════════════════════════════════════
   AMOUNT GRID (bill / payment)
══════════════════════════════════════════════ */
.amount-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
}

/* ══════════════════════════════════════════════
   NAV BUTTONS
══════════════════════════════════════════════ */
.stButton > button {
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important; letter-spacing: 0.03em !important;
  border-radius: var(--radius-sm) !important;
  border: none !important;
  padding: 14px 32px !important; font-size: 0.92rem !important;
  width: 100% !important; transition: all 0.25s ease !important;
}
/* primary */
button[kind="primary"], .stButton > button {
  background: linear-gradient(135deg, var(--gold), var(--gold2)) !important;
  color: #000 !important; box-shadow: 0 4px 20px rgba(245,200,66,0.25) !important;
}
button[kind="primary"]:hover, .stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(245,200,66,0.38) !important;
}
/* secondary */
button[kind="secondary"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}

/* ══════════════════════════════════════════════
   RESULT SCREEN
══════════════════════════════════════════════ */
.result-wrap { text-align: center; padding: 8px 0 24px; }

.score-ring-wrap {
  position: relative; display: inline-block; margin-bottom: 24px;
}

.verdict-tag {
  display: inline-flex; align-items: center; gap: 8px;
  border-radius: 100px; padding: 8px 24px;
  font-family: 'Syne', sans-serif; font-weight: 700;
  font-size: 0.85rem; letter-spacing: 0.06em; text-transform: uppercase;
  margin-bottom: 12px;
}
.verdict-tag.safe   { background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); color: var(--green); }
.verdict-tag.danger { background: rgba(244,63,94,0.15);  border: 1px solid rgba(244,63,94,0.3);  color: var(--rose);  }
.verdict-tag.warn   { background: rgba(245,200,66,0.15); border: 1px solid rgba(245,200,66,0.3); color: var(--gold);  }

.verdict-desc { font-size: 0.9rem; color: var(--muted2); max-width: 480px; margin: 0 auto 32px; line-height: 1.7; }

/* ─── Factor pills ─── */
.factors-row { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 36px; }
.factor-pill {
  display: flex; align-items: center; gap: 8px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 100px; padding: 8px 16px;
  font-size: 0.8rem; font-weight: 500;
}
.factor-pill .pill-dot { width: 8px; height: 8px; border-radius: 50%; }

/* ─── Stat grid ─── */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 28px; }
.stat-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-sm); padding: 18px 16px; text-align: center;
}
.stat-card .sv { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; }
.stat-card .sl { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; margin-top: 4px; }

/* ─── Confidence bar ─── */
.conf-bar-wrap { margin-bottom: 28px; }
.conf-bar-label { display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--muted); margin-bottom: 8px; }
.conf-bar-bg { height: 8px; background: rgba(255,255,255,0.06); border-radius: 8px; overflow: hidden; }
.conf-bar-fill {
  height: 100%; border-radius: 8px;
  transition: width 1s cubic-bezier(.4,0,.2,1);
}

/* ─── Reset button ─── */
.reset-btn { margin-top: 8px; }

/* ══════════════════════════════════════════════
   MISC
══════════════════════════════════════════════ */
.divider { height: 1px; background: var(--border); margin: 24px 0; }
.tip-box {
  display: flex; align-items: flex-start; gap: 12px;
  background: rgba(0,229,255,0.05); border: 1px solid rgba(0,229,255,0.15);
  border-radius: var(--radius-sm); padding: 14px 18px; margin-top: 16px;
  font-size: 0.8rem; color: var(--muted2); line-height: 1.6;
}
.tip-box .tip-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }

/* ─── Progress (streamlit native, hide) ─── */
.stProgress { display: none !important; }

/* ─── Column gap fix ─── */
[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "step" not in st.session_state:
    st.session_state.step = 1
if "result" not in st.session_state:
    st.session_state.result = None

# ── Field defaults
DEFAULTS = dict(
    LIMIT_BAL=100000, SEX="Male", EDUCATION="University", MARRIAGE="Single", AGE=28,
    PAY_0=0, PAY_1=0, PAY_2=0, PAY_3=0, PAY_4=0, PAY_5=0, PAY_6=0,
    BILL_AMT1=15000, BILL_AMT2=14000, BILL_AMT3=13500,
    BILL_AMT4=12000, BILL_AMT5=11000, BILL_AMT6=10000,
    PAY_AMT1=5000, PAY_AMT2=4500, PAY_AMT3=4000,
    PAY_AMT4=3500, PAY_AMT5=3000, PAY_AMT6=2500,
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  LOAD MODEL
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    m = pickle.load(open('credit_model.pkl','rb'))
    s = pickle.load(open('scaler.pkl','rb'))
    return m, s

try:
    model, scaler = load_model()
    model_ok = True
except:
    model_ok = False

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def arc_path(cx, cy, r, start_deg, end_deg):
    s = (math.radians(start_deg))
    e = (math.radians(end_deg))
    x1, y1 = cx + r*math.cos(s), cy + r*math.sin(s)
    x2, y2 = cx + r*math.cos(e), cy + r*math.sin(e)
    large = 1 if (end_deg - start_deg) % 360 > 180 else 0
    return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}"

def render_gauge(risk_pct):
    cx, cy, r = 130, 115, 88
    bg_arc   = arc_path(cx, cy, r, -215, 35)
    sweep    = (risk_pct / 100) * 250
    fill_arc = arc_path(cx, cy, r, -215, -215 + sweep)
    nx = cx + r * math.cos(math.radians(-215 + sweep))
    ny = cy + r * math.sin(math.radians(-215 + sweep))

    if risk_pct < 30:
        color, glow = "#10b981", "#10b98155"
    elif risk_pct < 65:
        color, glow = "#f5c842", "#f5c84255"
    else:
        color, glow = "#f43f5e", "#f43f5e55"

    return f"""
<svg viewBox="0 0 260 160" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:300px;display:block;margin:0 auto;">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="{color}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{color}"/>
    </linearGradient>
  </defs>
  <!-- bg track -->
  <path d="{bg_arc}" fill="none" stroke="rgba(255,255,255,0.07)"
        stroke-width="12" stroke-linecap="round"/>
  <!-- colored arc -->
  <path d="{fill_arc}" fill="none" stroke="url(#arcGrad)"
        stroke-width="12" stroke-linecap="round" filter="url(#glow)"/>
  <!-- needle tip -->
  <circle cx="{nx:.2f}" cy="{ny:.2f}" r="7"
          fill="{color}" filter="url(#glow)"/>
  <circle cx="{nx:.2f}" cy="{ny:.2f}" r="3" fill="#fff"/>
  <!-- center number -->
  <text x="{cx}" y="{cy+6}" text-anchor="middle" fill="white"
        font-family="Syne,sans-serif" font-size="30" font-weight="800">{risk_pct:.1f}%</text>
  <text x="{cx}" y="{cy+24}" text-anchor="middle" fill="rgba(255,255,255,0.4)"
        font-family="Instrument Sans,sans-serif" font-size="9.5" letter-spacing="2">DEFAULT PROBABILITY</text>
  <!-- tick labels -->
  <text x="30" y="148" fill="rgba(255,255,255,0.3)" font-size="8.5" font-family="Syne,sans-serif">0%</text>
  <text x="215" y="148" fill="rgba(255,255,255,0.3)" font-size="8.5" font-family="Syne,sans-serif">100%</text>
</svg>"""

def stepper_html(step):
    steps = [("01","Profile"),("02","Billing"),("03","Result")]
    items = ""
    for i,(num,label) in enumerate(steps, 1):
        if   i < step:  cc, lc = "done",   "done"
        elif i == step: cc, lc = "active",  "active"
        else:           cc, lc = "idle",    ""
        icon = "✓" if i < step else num
        conn = '<div class="step-connector"></div>' if i < 3 else ""
        items += f"""
        <div class="step-item">
          <div class="step-circle {cc}">{icon}</div>
          <div class="step-label {lc}">{label}</div>
        </div>{conn}"""
    return f'<div class="stepper">{items}</div>'

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge"><div class="dot"></div>AI-Powered · Real-Time Analysis</div>
  <h1>Credit<span>Lens</span></h1>
  <p>Instant credit default risk scoring powered by machine learning — beautifully simple, deeply accurate.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STEPPER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(stepper_html(st.session_state.step), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — CUSTOMER PROFILE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 1:

    # ── Card: Identity
    st.markdown("""
    <div class="glass-card">
      <div class="card-header">
        <div class="card-icon gold">👤</div>
        <div class="card-header-text">
          <h3>Personal Details</h3>
          <p>Basic demographic information about the customer</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.SEX = st.selectbox(
                "Gender", ["Male", "Female"],
                index=0 if st.session_state.SEX == "Male" else 1)
        with c2:
            st.session_state.AGE = st.slider("Age", 18, 80, st.session_state.AGE)
        with c3:
            edu_opts = ["Graduate School","University","High School","Others"]
            st.session_state.EDUCATION = st.selectbox(
                "Education Level", edu_opts,
                index=edu_opts.index(st.session_state.EDUCATION))

        c4, c5, c6 = st.columns(3)
        with c4:
            mar_opts = ["Married","Single","Others"]
            st.session_state.MARRIAGE = st.selectbox(
                "Marital Status", mar_opts,
                index=mar_opts.index(st.session_state.MARRIAGE))
        with c5:
            st.session_state.LIMIT_BAL = st.number_input(
                "Credit Limit (NT$)", min_value=0,
                value=st.session_state.LIMIT_BAL, step=10000)
        with c6:
            st.write("")  # spacer

    # ── Card: Payment Status
    st.markdown("""
    <div class="glass-card" style="margin-top:20px;">
      <div class="card-header">
        <div class="card-icon cyan">📅</div>
        <div class="card-header-text">
          <h3>Payment Status History</h3>
          <p>Monthly repayment behavior — last 7 months (−2=no use, −1=paid full, 0=revolving, 1–8=months late)</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    months = [
        ("PAY_0","September ← Most Recent"),
        ("PAY_1","August"),
        ("PAY_2","July"),
        ("PAY_3","June"),
        ("PAY_4","May"),
        ("PAY_5","April"),
        ("PAY_6","March"),
    ]
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3, c1, c2, c3, c1]
    for (key, label), col in zip(months, cols):
        with col:
            st.session_state[key] = st.slider(
                label, -2, 8, st.session_state[key], key=f"sl_{key}")

    st.markdown("""
    <div class="tip-box">
      <div class="tip-icon">💡</div>
      <div><strong>Tip:</strong> Payment status is the strongest predictor of default risk.
      Values ≥ 2 (i.e., 2+ months late) significantly raise the risk score.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2, 2, 2])
    with btn_col:
        if st.button("Continue to Billing →", key="next1"):
            st.session_state.step = 2
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — BILLING & PAYMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:

    # Bill amounts
    st.markdown("""
    <div class="glass-card">
      <div class="card-header">
        <div class="card-icon violet">🧾</div>
        <div class="card-header-text">
          <h3>Monthly Bill Amounts (NT$)</h3>
          <p>Statement balance charged each month — most recent first</p>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    bill_keys = [
        ("BILL_AMT1","September"),("BILL_AMT2","August"),("BILL_AMT3","July"),
        ("BILL_AMT4","June"),("BILL_AMT5","May"),("BILL_AMT6","April"),
    ]
    c1, c2, c3 = st.columns(3)
    cols = [c1,c2,c3,c1,c2,c3]
    for (key,label), col in zip(bill_keys, cols):
        with col:
            st.session_state[key] = st.number_input(
                label, value=float(st.session_state[key]),
                step=1000.0, key=f"ni_{key}")

    # Payment amounts
    st.markdown("""
    <div class="glass-card" style="margin-top:20px;">
      <div class="card-header">
        <div class="card-icon green">💸</div>
        <div class="card-header-text">
          <h3>Monthly Payment Amounts (NT$)</h3>
          <p>How much the customer actually paid each month</p>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    pay_keys = [
        ("PAY_AMT1","September"),("PAY_AMT2","August"),("PAY_AMT3","July"),
        ("PAY_AMT4","June"),("PAY_AMT5","May"),("PAY_AMT6","April"),
    ]
    p1, p2, p3 = st.columns(3)
    pcols = [p1,p2,p3,p1,p2,p3]
    for (key,label), col in zip(pay_keys, pcols):
        with col:
            st.session_state[key] = st.number_input(
                label, value=float(st.session_state[key]),
                step=500.0, key=f"ni_{key}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_back, _, col_next = st.columns([2, 1, 2])
    with col_back:
        if st.button("← Back", key="back2"):
            st.session_state.step = 1
            st.rerun()
    with col_next:
        if st.button("🔮  Analyze Risk Now", key="next2"):
            st.session_state.step = 3
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:

    # ── Encode & predict
    sex_enc = 1 if st.session_state.SEX == "Male" else 2
    edu_map = {"Graduate School":1,"University":2,"High School":3,"Others":4}
    mar_map = {"Married":1,"Single":2,"Others":3}

    row = [[
        st.session_state.LIMIT_BAL,
        sex_enc,
        edu_map[st.session_state.EDUCATION],
        mar_map[st.session_state.MARRIAGE],
        st.session_state.AGE,
        st.session_state.PAY_0, st.session_state.PAY_1, st.session_state.PAY_2,
        st.session_state.PAY_3, st.session_state.PAY_4,
        st.session_state.PAY_5, st.session_state.PAY_6,
        st.session_state.BILL_AMT1, st.session_state.BILL_AMT2,
        st.session_state.BILL_AMT3, st.session_state.BILL_AMT4,
        st.session_state.BILL_AMT5, st.session_state.BILL_AMT6,
        st.session_state.PAY_AMT1, st.session_state.PAY_AMT2,
        st.session_state.PAY_AMT3, st.session_state.PAY_AMT4,
        st.session_state.PAY_AMT5, st.session_state.PAY_AMT6,
    ]]

    if not model_ok:
        st.error("⚠️ Model files not found. Please place `credit_model.pkl` and `scaler.pkl` in the same folder as `app.py`.")
        st.session_state.step = 1
        st.stop()

    scaled     = scaler.transform(pd.DataFrame(row))
    prediction = model.predict(scaled)[0]
    proba      = model.predict_proba(scaled)[0]
    risk_pct   = proba[1] * 100
    safe_pct   = proba[0] * 100

    # ── Computed factors
    avg_bill  = np.mean([st.session_state[f"BILL_AMT{i}"] for i in range(1,7)])
    avg_paid  = np.mean([st.session_state[f"PAY_AMT{i}"]  for i in range(1,7)])
    util      = (st.session_state.BILL_AMT1 / st.session_state.LIMIT_BAL * 100) if st.session_state.LIMIT_BAL > 0 else 0
    pay_ratio = (avg_paid / avg_bill * 100) if avg_bill > 0 else 100
    avg_delay = np.mean([st.session_state[f"PAY_{k}"] for k in [0,1,2,3,4,5,6]])

    # ── Labels
    if risk_pct < 30:
        verdict, vclass, vdesc = "LOW RISK", "safe", \
            "This customer shows strong creditworthiness with consistent payment behavior and healthy utilization. Approval is recommended."
    elif risk_pct < 65:
        verdict, vclass, vdesc = "MEDIUM RISK", "warn", \
            "This customer presents moderate risk indicators. Consider additional verification or adjusted credit terms before approving."
    else:
        verdict, vclass, vdesc = "HIGH RISK", "danger", \
            "This customer exhibits significant default risk signals. Manual review strongly advised before extending credit."

    if vclass == "safe":   verdict_icon, ring_color = "✅", "#10b981"
    elif vclass == "warn": verdict_icon, ring_color = "⚠️", "#f5c842"
    else:                  verdict_icon, ring_color = "🚨", "#f43f5e"

    # ══ RENDER ══
    st.markdown(f"""
    <div class="glass-card" style="border-color:rgba(255,255,255,0.12);">
      <div class="result-wrap">
        <div class="verdict-tag {vclass}">{verdict_icon}&nbsp; {verdict}</div>
        <br>
    """, unsafe_allow_html=True)

    # Gauge
    st.markdown(render_gauge(risk_pct), unsafe_allow_html=True)

    st.markdown(f"""
        <p class="verdict-desc">{vdesc}</p>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Stats row
    util_color  = "#10b981" if util < 30 else ("#f5c842" if util < 70 else "#f43f5e")
    pay_color   = "#10b981" if pay_ratio >= 50 else ("#f5c842" if pay_ratio >= 20 else "#f43f5e")
    delay_color = "#10b981" if avg_delay <= 0 else ("#f5c842" if avg_delay < 2 else "#f43f5e")

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="sv" style="color:{util_color};">{util:.1f}%</div>
        <div class="sl">Credit Utilization</div>
      </div>
      <div class="stat-card">
        <div class="sv" style="color:{pay_color};">{pay_ratio:.1f}%</div>
        <div class="sl">Payment Ratio</div>
      </div>
      <div class="stat-card">
        <div class="sv" style="color:{delay_color};">{avg_delay:.1f} mo</div>
        <div class="sl">Avg Delay</div>
      </div>
      <div class="stat-card">
        <div class="sv" style="color:#94a3b8;">NT${st.session_state.LIMIT_BAL:,.0f}</div>
        <div class="sl">Credit Limit</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Confidence bars
    st.markdown(f"""
    <div class="glass-card">
      <div class="card-header">
        <div class="card-icon rose">📊</div>
        <div class="card-header-text">
          <h3>Model Confidence</h3>
          <p>Probability breakdown from the ML classifier</p>
        </div>
      </div>
      <div class="conf-bar-wrap">
        <div class="conf-bar-label">
          <span>✅ Will NOT Default</span><span>{safe_pct:.1f}%</span>
        </div>
        <div class="conf-bar-bg">
          <div class="conf-bar-fill"
               style="width:{safe_pct:.1f}%;
                      background:linear-gradient(90deg,#10b981,#34d399);"></div>
        </div>
      </div>
      <div class="conf-bar-wrap">
        <div class="conf-bar-label">
          <span>🚨 Will DEFAULT</span><span>{risk_pct:.1f}%</span>
        </div>
        <div class="conf-bar-bg">
          <div class="conf-bar-fill"
               style="width:{risk_pct:.1f}%;
                      background:linear-gradient(90deg,#f43f5e,#fb7185);"></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Factor pills
    pills = []
    pills.append(("💳 Utilization",  util_color,  f"{util:.0f}%"))
    pills.append(("📅 Avg Delay",    delay_color, f"{avg_delay:.1f} mo"))
    pills.append(("💰 Pay Ratio",    pay_color,   f"{pay_ratio:.0f}%"))
    pills.append(("🎓 Education",    "#94a3b8",   st.session_state.EDUCATION))
    pills.append(("🎂 Age",          "#94a3b8",   f"{st.session_state.AGE} yrs"))
    pills.append(("💍 Marital",      "#94a3b8",   st.session_state.MARRIAGE))

    pills_html = "".join(f"""
    <div class="factor-pill">
      <div class="pill-dot" style="background:{c};box-shadow:0 0 6px {c}66;"></div>
      <span style="color:#94a3b8;font-size:0.75rem;">{n}</span>
      <strong style="font-size:0.8rem;">{v}</strong>
    </div>""" for n,c,v in pills)

    st.markdown(f'<div class="factors-row">{pills_html}</div>', unsafe_allow_html=True)

    # ── Back / New
    col_back, _, col_new = st.columns([2, 1, 2])
    with col_back:
        if st.button("← Edit Billing", key="back3"):
            st.session_state.step = 2
            st.rerun()
    with col_new:
        if st.button("🔄 New Analysis", key="restart"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()