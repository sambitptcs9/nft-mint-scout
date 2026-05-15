import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="NFT Mint Scout",
    page_icon="◈",
    layout="wide",
)

# ── Data ─────────────────────────────────────────────────────────────────────

SIGNAL_COLORS = {
    "STRONG_BUY": "#00ff9d",
    "BUY": "#7bff6a",
    "HOLD": "#f5c542",
    "SELL": "#ff6b35",
    "STRONG_SELL": "#ff2255",
}

CHAINS = ["All", "Ethereum", "Solana", "Base", "Polygon"]

POOL = [
    {
        "name": "VoidArchitects", "chain": "Ethereum", "supply": 4444,
        "mintPrice": "0.04 ETH", "baseFloor": 0.09, "baseVol": 62,
        "mintLink": "https://opensea.io",
        "team": 85, "community": 80, "utility": 78, "timing": 72,
        "analysis": "Doxxed team with two prior successful collections; strong Discord engagement and a clear gaming utility roadmap. Floor has held above mint 3x in secondary already — early momentum is real.",
        "risks": ["High gas window", "Competitive PFP market"],
        "sells": [
            {"trigger": "2x flip", "condition": "List at 2x mint if floor hits 0.08 ETH within 72h", "urgency": "high"},
            {"trigger": "Royalty change risk", "condition": "Monitor if team cuts royalties — signals dump incoming", "urgency": "medium"},
            {"trigger": "Volume decay", "condition": "Exit if 7-day volume drops below $20K", "urgency": "low"},
        ],
    },
    {
        "name": "SolShades Gen2", "chain": "Solana", "supply": 3333,
        "mintPrice": "2.2 SOL", "baseFloor": 5.1, "baseVol": 38,
        "mintLink": "https://magiceden.io",
        "team": 70, "community": 88, "utility": 55, "timing": 80,
        "analysis": "Gen1 holders getting guaranteed WL — strong community loyalty signal. Floor on Gen1 pumped 4x post-mint. Utility is thin beyond holder perks but Solana liquidity is hot right now.",
        "risks": ["Weak utility beyond community access", "Solana network congestion risk on mint day"],
        "sells": [
            {"trigger": "Gen1 correlation", "condition": "Sell if Gen1 floor drops more than 20% — contagion risk", "urgency": "high"},
            {"trigger": "48h window", "condition": "Take profit within 48h of mint — momentum fades fast here", "urgency": "medium"},
            {"trigger": "Listing spike", "condition": "Exit if listings jump above 15% of supply overnight", "urgency": "medium"},
        ],
    },
    {
        "name": "BaseLayer Punks", "chain": "Base", "supply": 10000,
        "mintPrice": "0.001 ETH", "baseFloor": 0.003, "baseVol": 18,
        "mintLink": "",
        "team": 45, "community": 60, "utility": 40, "timing": 55,
        "analysis": "Free/near-free mint with high supply is a crowded trade — most holders will flip immediately. Team is anon with no track record. Could 3x on hype but equally likely to go to zero.",
        "risks": ["Anonymous team", "10K supply creates heavy sell pressure", "No roadmap beyond 'community'"],
        "sells": [
            {"trigger": "Flip day-one", "condition": "Only hold if floor 5x within 24h, otherwise exit", "urgency": "high"},
            {"trigger": "Whale watch", "condition": "If top 10 wallets hold >40% of supply, exit fast", "urgency": "high"},
            {"trigger": "Hype decay", "condition": "Twitter mentions drop-off is your exit signal", "urgency": "medium"},
        ],
    },
    {
        "name": "NeuraMesh Collective", "chain": "Ethereum", "supply": 2000,
        "mintPrice": "0.12 ETH", "baseFloor": 0.28, "baseVol": 95,
        "mintLink": "https://opensea.io",
        "team": 92, "community": 85, "utility": 90, "timing": 78,
        "analysis": "Backed by a known web3 studio with two exits. Token-gated AI tool access is live — not vaporware. Low supply + real utility = strong floor support. This is a slow-burn hold, not a flip.",
        "risks": ["High mint price limits audience", "AI tool competitive landscape"],
        "sells": [
            {"trigger": "Utility milestone", "condition": "Sell 50% if floor hits 0.5 ETH, hold rest long-term", "urgency": "medium"},
            {"trigger": "Team wallet", "condition": "Monitor team wallet — they unlock 6 months post-mint", "urgency": "medium"},
            {"trigger": "Bear trigger", "condition": "Exit fully if ETH drops below $1,800", "urgency": "low"},
        ],
    },
    {
        "name": "PolygonPets S3", "chain": "Polygon", "supply": 7500,
        "mintPrice": "15 MATIC", "baseFloor": 12, "baseVol": 9,
        "mintLink": "",
        "team": 38, "community": 42, "utility": 30, "timing": 35,
        "analysis": "Season 3 of a collection that saw declining interest each release. Floor is already below mint on S2. Team communication has been sparse and the roadmap has been quietly pushed back twice.",
        "risks": ["Floor already below S2 mint", "Sparse team comms", "Declining series momentum"],
        "sells": [
            {"trigger": "Do not mint", "condition": "Current signals suggest sitting this one out entirely", "urgency": "high"},
            {"trigger": "If already in", "condition": "List immediately at mint price and accept small loss", "urgency": "high"},
            {"trigger": "Watch S2 floor", "condition": "If S2 floor drops another 20%, S3 will be worse", "urgency": "medium"},
        ],
    },
    {
        "name": "Echelon Protocol", "chain": "Base", "supply": 5000,
        "mintPrice": "0.008 ETH", "baseFloor": 0.018, "baseVol": 44,
        "mintLink": "https://opensea.io",
        "team": 72, "community": 75, "utility": 68, "timing": 70,
        "analysis": "Base ecosystem darling with growing DeFi integration — holders get yield-boosted vault access. Mint price is accessible and team has shipped consistently. Mid-range risk with solid upside.",
        "risks": ["Base ecosystem still maturing", "Yield mechanics unaudited"],
        "sells": [
            {"trigger": "Yield APR drop", "condition": "Exit if vault APR falls below 8% — value prop gone", "urgency": "high"},
            {"trigger": "3x target", "condition": "Take 50% off at 3x mint price (~0.024 ETH floor)", "urgency": "medium"},
            {"trigger": "Protocol audit", "condition": "Hold through audit; sell if critical issues found", "urgency": "low"},
        ],
    },
    {
        "name": "FractalBeings", "chain": "Ethereum", "supply": 1111,
        "mintPrice": "0.08 ETH", "baseFloor": 0.19, "baseVol": 71,
        "mintLink": "https://opensea.io",
        "team": 88, "community": 78, "utility": 60, "timing": 82,
        "analysis": "Ultra-low supply generative art from a gallery-represented artist. 1-of-1 quality within a set — scarcity drives floor. Art market crossover audience means less crypto-native volatility.",
        "risks": ["Art market illiquid vs. PFP", "Niche audience limits liquidity"],
        "sells": [
            {"trigger": "Art auction signal", "condition": "If pieces start appearing on Foundation/SuperRare, hold — price discovery upward", "urgency": "low"},
            {"trigger": "ETH macro", "condition": "Sell 30% if ETH breaks down hard — art NFTs bleed slower but they bleed", "urgency": "medium"},
            {"trigger": "Long hold", "condition": "12+ month horizon recommended; short flippers will be left out", "urgency": "low"},
        ],
    },
    {
        "name": "RuneWalkers", "chain": "Solana", "supply": 6666,
        "mintPrice": "1.5 SOL", "baseFloor": 1.2, "baseVol": 14,
        "mintLink": "",
        "team": 30, "community": 35, "utility": 28, "timing": 25,
        "analysis": "Gaming NFT with no playable game after 9 months. Community sentiment has turned negative and multiple mods have left the Discord. Floor is already below mint with no catalyst in sight.",
        "risks": ["No playable product", "Staff departures", "Floor already below mint", "Treasury wallet movement flagged"],
        "sells": [
            {"trigger": "Avoid entirely", "condition": "All signals point to project abandonment — do not mint", "urgency": "high"},
            {"trigger": "If holding", "condition": "Exit at any price above 0.8 SOL and cut losses", "urgency": "high"},
            {"trigger": "Watch treasury", "condition": "If team treasury moves large SOL, rug risk is high", "urgency": "high"},
        ],
    },
]


def score_to_signal(score):
    if score >= 75: return "STRONG_BUY"
    if score >= 55: return "BUY"
    if score >= 40: return "HOLD"
    if score >= 25: return "SELL"
    return "STRONG_SELL"


def generate_mints(chain_filter):
    pool = POOL if chain_filter == "All" else [p for p in POOL if p["chain"] == chain_filter]
    source = pool if len(pool) >= 6 else POOL
    shuffled = random.sample(source, min(6, len(source)))
    mints = []
    for p in shuffled:
        jitter = random.randint(-8, 8)
        team = min(99, max(10, p["team"] + random.randint(-5, 5)))
        community = min(99, max(10, p["community"] + random.randint(-5, 5)))
        utility = min(99, max(10, p["utility"] + random.randint(-5, 5)))
        timing = min(99, max(10, p["timing"] + random.randint(-5, 5)))
        mint_price_score = min(99, max(10, round((team + community + utility + timing) / 4)))
        mint_score = min(97, max(10, round((team + community + utility + timing + mint_price_score) / 5) + jitter))
        floor_num = round(p["baseFloor"] * (0.85 + random.random() * 0.4), 3)
        vol_num = random.randint(max(5, p["baseVol"] - 15), p["baseVol"] + 20)

        if "SOL" in p["mintPrice"]:
            floor_str = f"{floor_num} SOL"
        elif "MATIC" in p["mintPrice"]:
            floor_str = f"{round(floor_num * 1000)} MATIC"
        else:
            floor_str = f"{floor_num} ETH"

        mints.append({
            "name": p["name"],
            "chain": p["chain"],
            "supply": p["supply"],
            "mintPrice": p["mintPrice"],
            "floorEst": floor_str,
            "volume24h": f"${vol_num}K",
            "mintScore": mint_score,
            "signal": score_to_signal(mint_score),
            "aiAnalysis": p["analysis"],
            "scoreBreakdown": [
                {"label": "Team Credibility", "score": team},
                {"label": "Community Traction", "score": community},
                {"label": "Utility / Roadmap", "score": utility},
                {"label": "Market Timing", "score": timing},
                {"label": "Mint Price Value", "score": mint_price_score},
            ],
            "sellSignals": p["sells"],
            "risks": p["risks"],
            "mintLink": p.get("mintLink", ""),
        })
    return mints


# ── Session state ─────────────────────────────────────────────────────────────

if "nfts" not in st.session_state:
    st.session_state.nfts = generate_mints("All")
if "chain" not in st.session_state:
    st.session_state.chain = "All"
if "selected" not in st.session_state:
    st.session_state.selected = None
if "last_updated" not in st.session_state:
    st.session_state.last_updated = datetime.now()

# ── Styling ───────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Space Mono', 'Courier New', monospace;
    background-color: #05071a;
    color: #c8d0ff;
  }
  .stApp { background-color: #05071a; }
  header[data-testid="stHeader"] { background-color: #07091f; border-bottom: 1px solid #111830; }

  /* Cards */
  .nft-card {
    background: #090d1f;
    border: 1px solid #141830;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 16px;
    transition: all 0.2s;
  }
  .nft-card:hover {
    background: #0d1433;
    border-color: #2a3a6e;
    box-shadow: 0 8px 30px #00ff9d12;
    transform: translateY(-2px);
  }
  .card-title {
    color: #e8ecff;
    font-weight: 700;
    font-size: 15px;
    margin: 0 0 2px 0;
  }
  .card-subtitle { color: #4a5580; font-size: 12px; margin: 0 0 10px 0; }

  .signal-badge {
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    border: 1px solid;
    display: inline-block;
    margin-bottom: 10px;
  }

  .score-bar-track {
    background: #1a1a2e;
    border-radius: 3px;
    height: 6px;
    overflow: hidden;
    flex: 1;
  }
  .metric-box {
    background: #0c1020;
    border-radius: 6px;
    padding: 6px 8px;
    text-align: center;
  }
  .metric-label { color: #3a4466; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; }
  .metric-value { color: #c8d0ff; font-size: 13px; font-family: monospace; }

  /* Detail panel */
  .detail-section {
    background: #07091a;
    border: 1px solid #1a2040;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 20px;
  }
  .detail-title { color: #e8ecff; font-size: 19px; font-weight: 700; margin-bottom: 6px; }
  .analysis-box {
    color: #9ba8cc;
    font-size: 13px;
    line-height: 1.75;
    background: #0c1020;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 20px;
  }
  .section-label {
    color: #4a5580;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
  }
  .sell-signal {
    background: #0c1020;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 6px;
  }
  .sell-trigger { color: #c8d0ff; font-size: 13px; }
  .sell-condition { color: #4a5580; font-size: 11px; margin-top: 2px; }
  .risk-item { color: #ff6b3599; font-size: 12px; padding: 5px 0; border-bottom: 1px solid #0f1525; }

  /* Disclaimer */
  .disclaimer {
    background: #0a0c1f;
    border: 1px solid #1a2040;
    border-left: 3px solid #f5c54240;
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 11px;
    color: #3a4466;
    margin-bottom: 18px;
  }

  /* Buttons override */
  .stButton > button {
    background: none;
    border: 1px solid #1a2040;
    color: #4a5580;
    border-radius: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
    transition: all 0.15s;
    padding: 4px 11px;
  }
  .stButton > button:hover {
    background: #00ff9d18;
    border-color: #00ff9d55;
    color: #00ff9d;
  }

  div[data-testid="stHorizontalBlock"] .stButton > button { width: 100%; }

  /* Hide default streamlit chrome elements */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .viewerBadge_container__1QSob { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def score_bar_html(score, height=6):
    pct = min(100, max(0, score))
    if pct >= 75:   color = "#00ff9d"
    elif pct >= 55: color = "#7bff6a"
    elif pct >= 40: color = "#f5c542"
    elif pct >= 25: color = "#ff6b35"
    else:           color = "#ff2255"
    return f"""
    <div style="display:flex;align-items:center;gap:8px;">
      <div class="score-bar-track" style="flex:1;">
        <div style="width:{pct}%;height:{height}px;background:{color};border-radius:3px;box-shadow:0 0 8px {color}80;"></div>
      </div>
      <span style="color:{color};font-size:12px;font-family:monospace;min-width:28px;">{pct}</span>
    </div>"""


def signal_badge_html(signal):
    color = SIGNAL_COLORS.get(signal, "#888")
    label = signal.replace("_", " ")
    return f'<span class="signal-badge" style="color:{color};border-color:{color}88;background:{color}18;">{label}</span>'


def render_card(nft, idx):
    color = SIGNAL_COLORS.get(nft["signal"], "#888")
    st.markdown(f"""
    <div class="nft-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
        <div>
          <p class="card-title">{nft["name"]}</p>
          <p class="card-subtitle">{nft["chain"]} · {nft["supply"]:,} supply</p>
        </div>
        {signal_badge_html(nft["signal"])}
      </div>
      {score_bar_html(nft["mintScore"])}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px;">
        <div class="metric-box">
          <div class="metric-label">Mint Price</div>
          <div class="metric-value">{nft["mintPrice"]}</div>
        </div>
        <div class="metric-box">
          <div class="metric-label">Floor Est.</div>
          <div class="metric-value">{nft["floorEst"]}</div>
        </div>
        <div class="metric-box">
          <div class="metric-label">Vol 24h</div>
          <div class="metric-value">{nft["volume24h"]}</div>
        </div>
      </div>
      {f'''<a href="{nft["mintLink"]}" target="_blank" style="display:block;margin-top:12px;text-align:center;background:#00ff9d18;border:1px solid #00ff9d55;color:#00ff9d;border-radius:6px;padding:7px 0;font-size:12px;font-weight:700;letter-spacing:1px;text-decoration:none;box-shadow:0 0 12px #00ff9d22;">⚡ MINT NOW →</a>''' if nft["signal"] == "STRONG_BUY" and nft.get("mintLink") else ""}
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Details", key=f"detail_{idx}"):
        if st.session_state.selected and st.session_state.selected["name"] == nft["name"]:
            st.session_state.selected = None
        else:
            st.session_state.selected = nft
        st.rerun()


def render_detail(nft):
    urgency_colors = {"high": "#ff6b35", "medium": "#f5c542", "low": "#2a3560"}
    breakdown_html = "".join(
        f'<div style="margin-bottom:10px;"><div style="color:#7a88b0;font-size:12px;margin-bottom:4px;">{b["label"]}</div>{score_bar_html(b["score"])}</div>'
        for b in nft["scoreBreakdown"]
    )
    sell_html = "".join(
        f'<div class="sell-signal" style="border-left:3px solid {urgency_colors.get(s["urgency"], "#2a3560")};">'
        f'<div class="sell-trigger">{s["trigger"]}</div>'
        f'<div class="sell-condition">{s["condition"]}</div></div>'
        for s in nft["sellSignals"]
    )
    risk_html = "".join(
        f'<div class="risk-item">⚠ {r}</div>' for r in nft["risks"]
    )

    st.markdown(f"""
    <div class="detail-section">
      <p class="detail-title">{nft["name"]}</p>
      <div style="display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;align-items:center;">
        {signal_badge_html(nft["signal"])}
        <span style="color:#3a5080;font-size:12px;padding:2px 8px;border:1px solid #1a2040;border-radius:4px;">{nft["chain"]}</span>
        {f'<a href="{nft["mintLink"]}" target="_blank" style="margin-left:auto;background:#00ff9d18;border:1px solid #00ff9d55;color:#00ff9d;border-radius:6px;padding:5px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-decoration:none;box-shadow:0 0 12px #00ff9d22;">⚡ MINT NOW →</a>' if nft["signal"] == "STRONG_BUY" and nft.get("mintLink") else ""}
      </div>
      <div class="analysis-box">{nft["aiAnalysis"]}</div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;">
        <div>
          <div class="section-label">Score Breakdown</div>
          {breakdown_html}
        </div>
        <div>
          <div class="section-label">Sell Signals</div>
          {sell_html}
          <div class="section-label" style="margin-top:18px;">Risk Factors</div>
          {risk_html}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✕  Close", key="close_detail"):
        st.session_state.selected = None
        st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────

hdr_left, hdr_right = st.columns([5, 1])
with hdr_left:
    st.markdown(f"""
    <div style="padding:4px 0 8px 0;">
      <div style="font-size:17px;font-weight:700;color:#e8ecff;letter-spacing:1px;">◈ NFT MINT SCOUT</div>
      <div style="font-size:11px;color:#3a4466;margin-top:2px;">
        AI mint intelligence &nbsp;·&nbsp; Updated {st.session_state.last_updated.strftime("%H:%M:%S")}
      </div>
    </div>
    """, unsafe_allow_html=True)

with hdr_right:
    if st.button("↻  REFRESH"):
        st.session_state.nfts = generate_mints(st.session_state.chain)
        st.session_state.last_updated = datetime.now()
        st.session_state.selected = None
        st.rerun()

st.markdown('<hr style="border:none;border-top:1px solid #111830;margin:0 0 16px 0;">', unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────

chain_cols = st.columns(len(CHAINS))
for i, c in enumerate(CHAINS):
    with chain_cols[i]:
        active_style = ""
        if st.session_state.chain == c:
            st.markdown(f'<style>div[data-testid="column"]:nth-child({i+1}) .stButton>button{{background:#00ff9d18!important;border-color:#00ff9d55!important;color:#00ff9d!important;}}</style>', unsafe_allow_html=True)
        if st.button(c, key=f"chain_{c}"):
            st.session_state.chain = c
            st.session_state.nfts = generate_mints(c)
            st.session_state.selected = None
            st.rerun()

st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

filter_col, score_col = st.columns([3, 1])
with score_col:
    min_score = st.slider("Min Score", 0, 70, 0, 10, label_visibility="collapsed")
    st.markdown(f'<div style="text-align:right;color:#3a4466;font-size:11px;margin-top:-8px;">MIN SCORE &nbsp;<span style="color:#00ff9d;">{min_score}</span></div>', unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="disclaimer">
  ⚠ Simulated signals for research only — not financial advice. NFTs are high-risk assets. Verify independently before minting.
</div>
""", unsafe_allow_html=True)

# ── Card grid ─────────────────────────────────────────────────────────────────

filtered = [
    n for n in st.session_state.nfts
    if n["mintScore"] >= min_score
    and (st.session_state.chain == "All" or n["chain"] == st.session_state.chain)
]

if not filtered:
    st.markdown('<div style="color:#3a4466;font-size:14px;text-align:center;padding:40px;">No mints match current filters.</div>', unsafe_allow_html=True)
else:
    cols = st.columns(3)
    for idx, nft in enumerate(filtered):
        with cols[idx % 3]:
            render_card(nft, idx)

# ── Detail panel ──────────────────────────────────────────────────────────────

if st.session_state.selected:
    render_detail(st.session_state.selected)

# ── Summary footer ────────────────────────────────────────────────────────────

st.markdown('<hr style="border:none;border-top:1px solid #111830;margin:24px 0 12px 0;">', unsafe_allow_html=True)

signal_order = ["STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"]
signal_counts = {sig: sum(1 for n in st.session_state.nfts if n["signal"] == sig) for sig in signal_order}
summary_parts = []
for sig, count in signal_counts.items():
    if count:
        color = SIGNAL_COLORS[sig]
        label = sig.replace("_", " ")
        summary_parts.append(
            f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:16px;">'
            f'<span style="width:7px;height:7px;border-radius:50%;background:{color};display:inline-block;"></span>'
            f'<span style="color:#4a5580;font-size:11px;">{label}</span>'
            f'<span style="color:{color};font-size:13px;font-weight:700;">{count}</span>'
            f'</span>'
        )

shown = f'<span style="margin-left:auto;color:#3a4466;font-size:11px;">{len(filtered)}/{len(st.session_state.nfts)} shown</span>'
st.markdown(
    f'<div style="display:flex;align-items:center;flex-wrap:wrap;">{"".join(summary_parts)}{shown}</div>',
    unsafe_allow_html=True,
)
