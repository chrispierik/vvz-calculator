import streamlit as st
from calculations import (
    calculate_fysio, WACHTDAGEN_OPTIES, DEFAULT_WACHTDAGEN,
    MARKT_GEMIDDELD,
)

st.set_page_config(
    page_title="Besparing-check – verzekerverzuim.nl",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "step": 1,
    "verzuim": None,
    "loon": 800_000,
    "wachttijd": DEFAULT_WACHTDAGEN,
    "premie_pct": MARKT_GEMIDDELD,
    "jaarpremie": 0,
    "bedrijf": "",
    "email": "",
    "tel": "",
    "submitted": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Logo SVG ──────────────────────────────────────────────────────────────────
LOGO_DARK = """<svg width="230" height="72" viewBox="0 0 230 72" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M40.2852 64.1741C38.2328 67.7164 33.1005 67.7164 31.0477 64.1741L1.60286 13.3644C-0.449942 9.82215 2.11606 5.39429 6.2217 5.39429H65.1114C69.2172 5.39429 71.783 9.82215 69.7301 13.3644L40.2852 64.1741Z" fill="#015EE1"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M38.4077 23.4377H32.4816V29.3414H26.5557V35.2455H32.4816V41.1492H38.4077V35.2455H44.3334V29.3414H38.4077V23.4377Z" fill="white"/>
<path d="M26.7118 39.9742C24.6512 43.4753 19.5709 43.4753 17.5103 39.9742L1.80171 13.2848C-0.283092 9.74264 2.28086 5.28369 6.40246 5.28369H37.8195C41.9413 5.28369 44.5053 9.74264 42.4204 13.2848L26.7118 39.9742Z" fill="#1040C5"/>
<path d="M21.8888 48.4551L35.2222 25.2088L27.4444 21.2238L11.4444 7.94019L1.22217 12.368L21.8888 48.4551Z" fill="#1040C5"/>
<path d="M91.4426 14.1219H96.38L90.724 30.9651H86.1613L80.4897 14.1219H85.4582L88.4426 25.2054L91.4426 14.1219ZM106.193 31.2764C104.412 31.2764 102.885 30.908 101.615 30.1712C100.354 29.4344 99.3853 28.4483 98.7084 27.2135C98.0417 25.9786 97.7084 24.6139 97.7084 23.1195V22.5124C97.7084 20.8312 98.0262 19.3368 98.6613 18.0292C99.3071 16.7216 100.224 15.6942 101.412 14.947C102.599 14.1894 104.016 13.8106 105.661 13.8106C108.109 13.8106 109.974 14.5682 111.255 16.0833C112.536 17.5881 113.177 19.591 113.177 22.0921V24.0846H102.505C102.672 25.112 103.099 25.937 103.787 26.5597C104.484 27.172 105.385 27.4782 106.49 27.4782C107.292 27.4782 108.036 27.3329 108.724 27.0423C109.422 26.7413 110.021 26.2743 110.521 25.6413L112.802 28.2411C112.271 28.9987 111.448 29.6939 110.333 30.327C109.219 30.9598 107.839 31.2764 106.193 31.2764ZM105.63 17.5933C104.703 17.5933 103.995 17.9046 103.505 18.5273C103.016 19.1396 102.693 19.9387 102.536 20.9246H108.536V20.551C108.526 19.6896 108.287 18.9839 107.818 18.4339C107.36 17.8735 106.63 17.5933 105.63 17.5933ZM120.364 30.9651H115.646V14.1219H120.084L120.24 16.13C120.646 15.4036 121.161 14.838 121.787 14.4333C122.412 14.0182 123.136 13.8106 123.958 13.8106C124.198 13.8106 124.448 13.8314 124.708 13.8728C124.979 13.904 125.198 13.9507 125.364 14.0129L125.302 18.5429C125.073 18.5117 124.797 18.4858 124.474 18.465C124.161 18.4339 123.885 18.4184 123.646 18.4184C121.969 18.4184 120.875 18.9632 120.364 20.0529V30.9651ZM140.99 30.9651H126.88V28.1476L134.677 17.9046H127.13V14.1219H140.755V16.8616L132.912 27.1824H140.99V30.9651ZM151.661 31.2764C149.88 31.2764 148.354 30.908 147.084 30.1712C145.823 29.4344 144.854 28.4483 144.177 27.2135C143.51 25.9786 143.177 24.6139 143.177 23.1195V22.5124C143.177 20.8312 143.495 19.3368 144.13 18.0292C144.776 16.7216 145.693 15.6942 146.88 14.947C148.068 14.1894 149.484 13.8106 151.13 13.8106C153.578 13.8106 155.443 14.5682 156.724 16.0833C158.005 17.5881 158.646 19.591 158.646 22.0921V24.0846H147.974C148.14 25.112 148.568 25.937 149.255 26.5597C149.953 27.172 150.854 27.4782 151.958 27.4782C152.76 27.4782 153.505 27.3329 154.193 27.0423C154.891 26.7413 155.49 26.2743 155.99 25.6413L158.271 28.2411C157.74 28.9987 156.916 29.6939 155.802 30.327C154.688 30.9598 153.307 31.2764 151.661 31.2764ZM151.099 17.5933C150.172 17.5933 149.464 17.9046 148.974 18.5273C148.484 19.1396 148.161 19.9387 148.005 20.9246H154.005V20.551C153.995 19.6896 153.755 18.9839 153.287 18.4339C152.828 17.8735 152.099 17.5933 151.099 17.5933ZM165.833 30.9651H161.115V7.03906H165.833V20.1151L166.63 19.1033L170.818 14.1219H176.49L170.443 21.1114L176.99 30.9651H171.568L167.412 24.3493L165.833 25.9215V30.9651ZM186.224 31.2764C184.443 31.2764 182.916 30.908 181.646 30.1712C180.385 29.4344 179.417 28.4483 178.74 27.2135C178.073 25.9786 177.74 24.6139 177.74 23.1195V22.5124C177.74 20.8312 178.057 19.3368 178.693 18.0292C179.339 16.7216 180.255 15.6942 181.443 14.947C182.63 14.1894 184.047 13.8106 185.693 13.8106C188.14 13.8106 190.005 14.5682 191.287 16.0833C192.568 17.5881 193.208 19.591 193.208 22.0921V24.0846H182.536C182.703 25.112 183.13 25.937 183.818 26.5597C184.516 27.172 185.417 27.4782 186.521 27.4782C187.323 27.4782 188.068 27.3329 188.755 27.0423C189.453 26.7413 190.052 26.2743 190.552 25.6413L192.833 28.2411C192.302 28.9987 191.479 29.6939 190.364 30.327C189.25 30.9598 187.87 31.2764 186.224 31.2764ZM185.661 17.5933C184.734 17.5933 184.026 17.9046 183.536 18.5273C183.047 19.1396 182.724 19.9387 182.568 20.9246H188.568V20.551C188.557 19.6896 188.318 18.9839 187.849 18.4339C187.391 17.8735 186.661 17.5933 185.661 17.5933ZM200.396 30.9651H195.677V14.1219H200.115L200.271 16.13C200.677 15.4036 201.193 14.838 201.818 14.4333C202.443 14.0182 203.167 13.8106 203.99 13.8106C204.229 13.8106 204.479 13.8314 204.74 13.8728C205.01 13.904 205.229 13.9507 205.396 14.0129L205.333 18.5429C205.104 18.5117 204.828 18.4858 204.505 18.465C204.193 18.4339 203.916 18.4184 203.677 18.4184C202 18.4184 200.906 18.9632 200.396 20.0529V30.9651ZM91.8333 46.0026H95.8489L90.0053 62.8457H86.552L80.6613 46.0026H84.6929L88.2866 57.9888L91.8333 46.0026ZM105.646 63.157C103.969 63.157 102.521 62.7992 101.302 62.0828C100.084 61.3566 99.1457 60.3811 98.4897 59.1564C97.8333 57.9215 97.5053 56.5413 97.5053 55.0155V54.3774C97.5053 52.6235 97.8386 51.0981 98.5053 49.8008C99.172 48.4932 100.084 47.4815 101.24 46.7655C102.406 46.049 103.724 45.6913 105.193 45.6913C106.818 45.6913 108.167 46.0442 109.24 46.7495C110.312 47.4451 111.115 48.4153 111.646 49.6609C112.177 50.8958 112.443 52.3277 112.443 53.9572V55.623H101.412C101.516 56.8991 101.958 57.9578 102.74 58.7982C103.521 59.6284 104.568 60.0437 105.88 60.0437C106.787 60.0437 107.588 59.8671 108.287 59.5146C108.984 59.1617 109.594 58.653 110.115 57.9888L112.146 60.0127C111.604 60.8115 110.802 61.5381 109.74 62.1917C108.677 62.8355 107.312 63.157 105.646 63.157ZM105.177 48.789C104.146 48.789 103.318 49.1521 102.693 49.8787C102.068 50.6049 101.667 51.591 101.49 52.8365H108.615V52.5407C108.594 51.8867 108.464 51.2744 108.224 50.7036C107.995 50.1329 107.63 49.671 107.13 49.3181C106.64 48.9652 105.99 48.789 105.177 48.789ZM119.224 62.8457H115.349V46.0026H119.036L119.146 47.9482C119.573 47.253 120.104 46.703 120.74 46.2983C121.385 45.8936 122.14 45.6913 123.005 45.6913C123.224 45.6913 123.469 45.7121 123.74 45.7533C124.01 45.7949 124.213 45.8418 124.349 45.8936L124.318 49.5519C124.078 49.5205 123.823 49.4948 123.552 49.474C123.292 49.4426 123.031 49.4271 122.771 49.4271C121.854 49.4271 121.104 49.6037 120.521 49.9566C119.937 50.3095 119.505 50.8072 119.224 51.451V62.8457ZM139.802 62.8457H126.036V60.355L134.552 49.1158H126.224V46.0026H139.474V48.3998L130.896 59.748H139.802V62.8457ZM152.943 46.0026H156.818V62.8457H153.161L153.068 61.1489C152.536 61.7821 151.88 62.2749 151.099 62.6278C150.318 62.9807 149.391 63.157 148.318 63.157C146.651 63.157 145.302 62.6695 144.271 61.6936C143.24 60.7181 142.724 59.1148 142.724 56.8836V46.0026H146.599V56.9146C146.599 58.0875 146.864 58.8969 147.396 59.3433C147.927 59.779 148.557 59.9968 149.287 59.9968C150.245 59.9968 151.016 59.8259 151.599 59.4832C152.193 59.1303 152.64 58.6583 152.943 58.0667V46.0026ZM160.63 41.5973C160.63 41.0057 160.823 40.5178 161.208 40.1339C161.594 39.7393 162.13 39.5423 162.818 39.5423C163.505 39.5423 164.047 39.7393 164.443 40.1339C164.839 40.5178 165.036 41.0057 165.036 41.5973C165.036 42.1782 164.839 42.6662 164.443 43.0602C164.047 43.4446 163.505 43.6363 162.818 43.6363C162.13 43.6363 161.594 43.4446 161.208 43.0602C160.823 42.6662 160.63 42.1782 160.63 41.5973ZM164.755 62.8457H160.88V46.0026H164.755V62.8457ZM172.724 62.8457H168.833V46.0026H172.49L172.615 47.8392C173.177 47.1649 173.864 46.6406 174.677 46.2673C175.5 45.883 176.448 45.6913 177.521 45.6913C178.563 45.6913 179.484 45.8989 180.287 46.3138C181.088 46.7292 181.708 47.388 182.146 48.2909C182.698 47.5023 183.406 46.8744 184.271 46.4073C185.146 45.9299 186.167 45.6913 187.333 45.6913C189.052 45.6913 190.401 46.1739 191.38 47.1387C192.37 48.104 192.864 49.718 192.864 51.9802V62.8457H188.974V51.9492C188.974 50.7142 188.703 49.8889 188.161 49.474C187.63 49.0587 186.912 48.8514 186.005 48.8514C185.161 48.8514 184.469 49.0742 183.927 49.5205C183.385 49.9668 183.005 50.5482 182.787 51.2642C182.787 51.3784 182.787 51.4975 182.787 51.6219V62.8457H178.912V51.9802C178.912 50.7869 178.64 49.9668 178.099 49.5205C177.568 49.0742 176.844 48.8514 175.927 48.8514C175.125 48.8514 174.464 49.0223 173.943 49.3651C173.422 49.6972 173.016 50.1537 172.724 50.7346V62.8457ZM196.677 60.4639C196.677 59.7271 196.927 59.1148 197.427 58.6273C197.927 58.1393 198.588 57.8953 199.412 57.8953C200.234 57.8953 200.891 58.1393 201.38 58.6273C201.88 59.1148 202.13 59.7271 202.13 60.4639C202.13 61.1906 201.88 61.7976 201.38 62.2851C200.891 62.7731 200.234 63.017 199.412 63.017C198.588 63.017 197.927 62.7731 197.427 62.2851C196.927 61.7976 196.677 61.1906 196.677 60.4639ZM210.677 62.8457H205.802V46.0026H210.38L210.536 47.9017C211.734 46.4281 213.339 45.6913 215.349 45.6913C216.412 45.6913 217.344 45.8989 218.146 46.3138C218.948 46.7185 219.573 47.3982 220.021 48.3533C220.469 49.2973 220.693 50.5792 220.693 52.198V62.8457H215.787V52.167C215.787 51.1601 215.568 50.4858 215.13 50.143C214.693 49.8008 214.068 49.6294 213.255 49.6294C212.651 49.6294 212.136 49.749 211.708 49.9876C211.292 50.2263 210.948 50.5584 210.677 50.9839V62.8457ZM229.052 62.8457H224.161V38.9352H229.052V62.8457Z" fill="white"/>
</svg>"""

# ── Step metadata ─────────────────────────────────────────────────────────────
STEP_LABELS = ["Verzuimcijfer", "Loonsom", "Wachttijd", "Huidige premie", "Uw besparing", "Uw gegevens"]
VERZUIM_OPTS = ["0–2%", "2–4%", "4–6%", "6–8%", "8%+"]
VERZUIM_KEYS = ["0-2", "2-4", "4-6", "6-8", "8+"]
TOTAL_Q = 5  # questions (excl. result + done)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800&family=JetBrains+Mono:wght@400;500;600&display=swap');

#MainMenu, footer, header { visibility: hidden; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2A8A 0%, #1040C5 100%) !important;
    min-width: 340px !important;
    max-width: 340px !important;
}
section[data-testid="stSidebar"] > div { background: transparent !important; }
section[data-testid="stSidebar"] .block-container {
    padding: 36px 28px 28px !important;
}
section[data-testid="stSidebar"] .stMarkdown * { color: white !important; }

/* ── Main content ── */
.main .block-container {
    padding: 56px 60px 80px !important;
    max-width: 760px !important;
}
.stApp { background: #FAFBFE !important; }

/* ── Question pill + head ── */
.q-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #015EE1;
    background: #E6EEFB;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
}
.q-pill.result {
    color: #0E7C66;
    background: #D6F2EB;
}
h1.q-title {
    font-size: 34px !important;
    font-weight: 700 !important;
    color: #0B1530 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.15 !important;
    margin: 14px 0 0 !important;
}
p.q-helper {
    margin-top: 14px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    color: #5A6488 !important;
}

/* ── Hero number (loonsom / premie) ── */
.hero-wrap { text-align: center; margin-top: 36px; }
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #8089A8;
    letter-spacing: .1em;
    text-transform: uppercase;
}
.hero-num {
    font-size: 64px;
    font-weight: 700;
    color: #0B1530;
    letter-spacing: -0.04em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    margin-top: 8px;
}
.hero-num .eur { color: #8089A8; }
.hero-pct {
    font-size: 84px;
    font-weight: 700;
    letter-spacing: -0.05em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    transition: color .3s;
}
.hero-pct .unit { font-size: 44px; color: #8089A8; }

/* ── Market pill ── */
.market-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px; border-radius: 999px;
    font-size: 13px; font-weight: 600;
    margin-top: 12px;
}
.market-pill.above { background: #FFF1EB; color: #A8401A; }
.market-pill.below { background: #D6F2EB; color: #0E7C66; }

/* ── Slider ── */
.stSlider { margin-top: 28px !important; }
.stSlider [data-baseweb="slider"] [role="slider"] { background: #015EE1 !important; }
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackFill"] { background: #015EE1 !important; }
div[data-testid="stSlider"] label { display: none !important; }

/* ── Navigation & CTA buttons ── */
button[kind="primary"] {
    background: #1ABC9C !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 14px 26px !important;
    box-shadow: 0 12px 28px -10px rgba(26,188,156,.5) !important;
    transition: background .2s !important;
}
button[kind="primary"]:hover { background: #16A085 !important; }
button[kind="primary"]:disabled {
    background: #EBEEF5 !important;
    color: #8089A8 !important;
    box-shadow: none !important;
}
button[kind="secondary"] {
    background: transparent !important;
    color: #5A6488 !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 4px !important;
    box-shadow: none !important;
}
button[kind="secondary"]:hover {
    background: transparent !important;
    color: #0B1530 !important;
    border: none !important;
}

/* ── Pills (loonsom chips) ── */
[data-testid="stPillsInput"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    justify-content: center !important;
    margin-top: 20px !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stPillsInput"] button {
    padding: 7px 14px !important;
    border-radius: 999px !important;
    border: 1px solid #DCE0EC !important;
    background: #fff !important;
    color: #2A3454 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: all .15s !important;
    width: auto !important;
}
[data-testid="stPillsInput"] button:hover {
    background: #0B1530 !important;
    color: #fff !important;
    border-color: #0B1530 !important;
}
[data-testid="stPillsInput"] button[aria-pressed="true"] {
    background: #0B1530 !important;
    color: #fff !important;
    border-color: #0B1530 !important;
}

/* ── Result hero card ── */
.result-hero {
    background: linear-gradient(135deg, #1040C5 0%, #015EE1 100%);
    border-radius: 24px;
    padding: 36px 40px;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 40px -12px rgba(1,94,225,.35);
    margin: 28px 0 16px;
}
.result-hero-glow {
    position: absolute; top: -80px; right: -80px;
    width: 280px; height: 280px; border-radius: 50%;
    background: radial-gradient(circle, rgba(26,188,156,.4), transparent 70%);
    pointer-events: none;
}
.result-save-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: .14em; text-transform: uppercase; opacity: .7;
}
.result-save-amount {
    font-size: 72px; font-weight: 700; margin-top: 6px;
    letter-spacing: -0.04em; line-height: 1;
    font-variant-numeric: tabular-nums;
}
.result-save-amount .eur { opacity: .6; font-size: 42px; }
.result-save-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 5px 14px; border-radius: 999px;
    background: #1ABC9C; color: #fff;
    font-weight: 700; font-size: 13px; margin-top: 12px;
}
.compare-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 0;
}
.compare-card {
    border-radius: 16px; padding: 20px 22px;
}
.compare-card .cc-label {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .08em; color: #5A6488;
}
.compare-card .cc-amount {
    font-size: 26px; font-weight: 700; margin-top: 6px;
    font-variant-numeric: tabular-nums; letter-spacing: -.02em;
}
.compare-card .cc-sub { font-size: 12px; color: #8089A8; margin-top: 3px; }

/* ── Besparing reminder card ── */
.besparing-reminder {
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    padding: 16px 20px; border-radius: 14px;
    background: #EBF8F4; border: 1px solid #1ABC9C;
    margin: 20px 0 32px;
}

/* ── Form fields ── */
div[data-testid="stTextInput"] label {
    font-size: 13px !important; font-weight: 600 !important; color: #2A3454 !important;
    margin-bottom: 6px !important;
}
div[data-testid="stTextInput"] input {
    background: #fff !important;
    border: 1.5px solid #DCE0EC !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
    min-height: 52px !important;
    font-family: 'Inter', sans-serif !important;
    color: #0B1530 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #1040C5 !important;
    box-shadow: 0 0 0 2px rgba(16,64,197,.12) !important;
    outline: none !important;
}
div[data-testid="stFormSubmitButton"] button {
    background: #1ABC9C !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 14px 26px !important;
    width: 100% !important;
    box-shadow: 0 12px 28px -10px rgba(26,188,156,.5) !important;
    margin-top: 8px !important;
}
div[data-testid="stFormSubmitButton"] button:hover { background: #16A085 !important; }

/* ── Done screen ── */
.done-check {
    width: 64px; height: 64px; border-radius: 999px;
    background: #1ABC9C; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: 700;
    margin-bottom: 20px;
}

/* ── Disclaimer ── */
.vvz-disclaimer {
    font-size: 11px; color: #8089A8; line-height: 1.7; font-style: italic;
    border-top: 1px solid #EBEEF5; padding-top: 20px; margin-top: 12px;
}

/* ── Sidebar step list ── */
.sb-step {
    display: flex; align-items: center; gap: 14px;
    padding: 13px 0;
    border-bottom: 1px solid rgba(255,255,255,.12);
    transition: opacity .25s;
}
.sb-step:last-child { border-bottom: none; }
.sb-dot {
    width: 28px; height: 28px; border-radius: 999px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.sb-dot.done { background: #1ABC9C; color: #fff; }
.sb-dot.active { background: #fff; color: #1040C5; }
.sb-dot.upcoming {
    background: transparent;
    border: 1.5px solid rgba(255,255,255,.4);
    color: rgba(255,255,255,.6);
}
.sb-label { font-size: 14px; font-weight: 500; color: white; flex: 1; }
.sb-label.active { font-weight: 700; }
.sb-label.upcoming { opacity: .55; }
.sb-val { font-size: 13px; color: rgba(255,255,255,.7); font-variant-numeric: tabular-nums; }

/* ── Sidebar misc ── */
.sb-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: .16em; text-transform: uppercase; opacity: .6;
    color: white;
}
.sb-title {
    font-size: 28px; font-weight: 700; color: white;
    letter-spacing: -.02em; line-height: 1.2;
    margin: 12px 0 0;
}
.sb-sub { font-size: 14px; color: rgba(255,255,255,.8); line-height: 1.55; margin-top: 10px; }
.sb-stars { color: #1ABC9C; font-size: 14px; }
.sb-review { font-size: 13px; color: rgba(255,255,255,.85); font-style: italic; line-height: 1.5; margin: 8px 0 0; }
.sb-reviewer { font-size: 12px; color: rgba(255,255,255,.6); margin-top: 6px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def go_next():
    st.session_state.step = min(7, st.session_state.step + 1)
    st.rerun()

def go_back():
    st.session_state.step = max(1, st.session_state.step - 1)
    st.rerun()

def q_head(num, total, title, helper=""):
    pill = f"Vraag {num:02d} / {total:02d}"
    h = f'<div class="q-pill">{pill}</div><h1 class="q-title">{title}</h1>'
    if helper:
        h += f'<p class="q-helper">{helper}</p>'
    return h

def nav(back_lbl="← Terug", next_lbl="Volgende →", next_disabled=False, next_key="nav_next", back_key="nav_back"):
    st.markdown('<div style="margin-top:48px;"></div>', unsafe_allow_html=True)
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button(back_lbl, key=back_key, type="secondary"):
            go_back()
    with col_n:
        if st.button(next_lbl, key=next_key, disabled=next_disabled,
                     type="primary", use_container_width=True):
            go_next()

def verzuim_label(v):
    mapping = {"0-2": "0–2%", "2-4": "2–4%", "4-6": "4–6%", "6-8": "6–8%", "8+": "8%+", "unk": "gem."}
    return mapping.get(v, "—")

def wacht_summary(w):
    return f"{w} d."

def loon_summary(v):
    return f"€ {int(v/1000)}k"

def premie_summary(p):
    return f"{p:.1f}%"


# ── Sidebar ───────────────────────────────────────────────────────────────────
step = st.session_state.step

with st.sidebar:
    summaries = {
        1: verzuim_label(st.session_state.verzuim) if st.session_state.verzuim else None,
        2: loon_summary(st.session_state.loon),
        3: wacht_summary(st.session_state.wachttijd),
        4: premie_summary(st.session_state.premie_pct),
    }

    # Logo
    st.markdown(f'<div style="margin-bottom:40px;">{LOGO_DARK}</div>', unsafe_allow_html=True)

    # Tagline
    st.markdown("""
    <div class="sb-mono">Besparing-check</div>
    <div class="sb-title">Ontdek of u te veel betaalt voor uw verzuimverzekering.</div>
    <div class="sb-sub">5 korte vragen. Onafhankelijk vergeleken met 6 verzekeraars. Klanten besparen gemiddeld 18%.</div>
    """, unsafe_allow_html=True)

    # Step list
    step_labels_display = ["Verzuimcijfer", "Loonsom", "Wachttijd", "Huidige premie", "Uw besparing", "Uw gegevens"]
    st.markdown('<div style="margin-top:36px;">', unsafe_allow_html=True)
    for i, lbl in enumerate(step_labels_display):
        idx = i + 1
        done   = idx < step
        active = idx == step
        dot_cls = "done" if done else ("active" if active else "upcoming")
        lbl_cls = "active" if active else ("upcoming" if not done else "")
        inner = "✓" if done else str(idx)
        val_html = f'<span class="sb-val">{summaries.get(idx, "")}</span>' if (done and summaries.get(idx)) else ""
        opacity = "1" if (done or active) else ".55"
        st.markdown(f"""
        <div class="sb-step" style="opacity:{opacity};">
            <div class="sb-dot {dot_cls}">{inner}</div>
            <div class="sb-label {lbl_cls}">{lbl}</div>
            {val_html}
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Testimonial
    st.markdown("""
    <div style="margin-top:auto;padding-top:32px;border-top:1px solid rgba(255,255,255,.15);margin-top:28px;">
        <div>
            <span class="sb-stars">★★★★★</span>
            <span style="font-size:13px;font-weight:600;color:white;margin-left:6px;">4,8 / 5</span>
            <span style="font-size:12px;color:rgba(255,255,255,.6);margin-left:4px;">· 312 reviews</span>
        </div>
        <div class="sb-review">"We bespaarden € 8.400 per jaar zonder iets in te leveren op de dekking. Alles via één gesprek."</div>
        <div class="sb-reviewer">— Marieke V., praktijkhouder fysiotherapie</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — VERZUIM
# ══════════════════════════════════════════════════════════════════════════════
if step == 1:
    st.markdown(q_head(1, TOTAL_Q,
        "Hoe hoog is het ziekteverzuim in uw praktijk?",
        "Kijk naar het gemiddelde van de laatste 3 jaar. Bij twijfel: kies de klasse iets hoger."
    ), unsafe_allow_html=True)

    st.markdown("""<style>
    [data-testid="stSegmentedControl"] { margin-top: 36px !important; }
    [data-testid="stSegmentedControl"] > div {
        background: #F5F7FB !important;
        border-radius: 16px !important;
        padding: 6px !important;
        gap: 4px !important;
        border: none !important;
        width: 100% !important;
        display: flex !important;
    }
    [data-testid="stSegmentedControl"] button {
        flex: 1 !important;
        padding: 14px 4px !important;
        border-radius: 12px !important;
        background: transparent !important;
        border: none !important;
        color: #5A6488 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: none !important;
        letter-spacing: -0.01em !important;
    }
    [data-testid="stSegmentedControl"] button[aria-pressed="true"],
    [data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background: white !important;
        color: #0B1530 !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(11,21,48,.08) !important;
    }
    </style>""", unsafe_allow_html=True)

    all_opts = VERZUIM_OPTS + ["Weet ik niet"]
    cur_v = st.session_state.verzuim
    default_val = None
    if cur_v in VERZUIM_KEYS:
        default_val = all_opts[VERZUIM_KEYS.index(cur_v)]
    elif cur_v == "unk":
        default_val = "Weet ik niet"

    chosen = st.segmented_control(
        "verzuim", all_opts,
        default=default_val,
        selection_mode="single",
        label_visibility="collapsed",
        key="verzuim_seg",
    )

    if chosen is not None:
        if chosen == "Weet ik niet":
            st.session_state.verzuim = "unk"
        else:
            idx = VERZUIM_OPTS.index(chosen)
            st.session_state.verzuim = VERZUIM_KEYS[idx]

    nav(back_lbl="← Terug", next_lbl="Volgende →",
        next_disabled=(chosen is None),
        next_key="v1_next", back_key="v1_back")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — LOONSOM
# ══════════════════════════════════════════════════════════════════════════════
elif step == 2:
    st.markdown(q_head(2, TOTAL_Q,
        "Wat is uw totale loonsom per jaar?",
        "Tel alle bruto salarissen van uw medewerkers bij elkaar op (vóór belasting). Dit is de basis waarover de premie wordt berekend."
    ), unsafe_allow_html=True)

    loon_val = st.session_state.get("loon_slider", st.session_state.loon)
    loon_formatted = f"{loon_val:,}".replace(",", ".")
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-label">Loonsom per jaar</div>
        <div class="hero-num"><span class="eur">€&nbsp;</span>{loon_formatted}</div>
    </div>""", unsafe_allow_html=True)

    loon = st.slider("loon", 100_000, 3_000_000, st.session_state.loon, 10_000,
                     key="loon_slider", label_visibility="collapsed")
    st.session_state.loon = loon

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:12px;color:#8089A8;margin-top:6px;">
        <span>€ 100k</span><span>€ 3M</span>
    </div>""", unsafe_allow_html=True)

    CHIP_VALS = {"€ 250k": 250_000, "€ 500k": 500_000, "€ 1M": 1_000_000, "€ 2M": 2_000_000}
    selected_chip = st.pills(
        "Snelkeuze", list(CHIP_VALS.keys()),
        selection_mode="single",
        label_visibility="collapsed",
        key="loon_chips",
    )
    if selected_chip and CHIP_VALS[selected_chip] != st.session_state.loon:
        st.session_state.loon = CHIP_VALS[selected_chip]
        st.rerun()

    nav(back_lbl="← Terug", next_lbl="Volgende →",
        next_key="v2_next", back_key="v2_back")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — WACHTTIJD
# ══════════════════════════════════════════════════════════════════════════════
elif step == 3:
    st.markdown(q_head(3, TOTAL_Q,
        "Hoeveel dagen wachttijd heeft u?",
        'De periode dat u zelf het loon doorbetaalt voordat de verzekering uitkeert. Op uw polisblad als <strong>"eigen risico"</strong>. Hoe langer de wachttijd, hoe lager de premie.'
    ), unsafe_allow_html=True)

    st.markdown("""<style>
    [data-testid="stPillsInput"] {
        display: grid !important;
        grid-template-columns: repeat(6, 1fr) !important;
        gap: 10px !important;
        margin-top: 36px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        justify-content: unset !important;
        flex-wrap: unset !important;
    }
    [data-testid="stPillsInput"] button {
        padding: 0 6px !important;
        border-radius: 16px !important;
        border: 1.5px solid #EBEEF5 !important;
        background: #fff !important;
        color: #0B1530 !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        min-height: 80px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 16px !important;
        transition: border-color .15s, background .15s !important;
    }
    [data-testid="stPillsInput"] button[aria-pressed="true"] {
        border-color: #015EE1 !important;
        background: #F4F7FD !important;
        color: #1040C5 !important;
    }
    [data-testid="stPillsInput"] button:hover {
        background: #F5F7FB !important;
        border-color: #DCE0EC !important;
        color: #0B1530 !important;
    }
    </style>""", unsafe_allow_html=True)

    wacht_opts_str = [str(w) for w in WACHTDAGEN_OPTIES]
    cur_wacht_str = str(st.session_state.wachttijd) if st.session_state.wachttijd in WACHTDAGEN_OPTIES else "30"

    chosen_w = st.pills(
        "wachttijd", wacht_opts_str,
        selection_mode="single",
        default=cur_wacht_str,
        label_visibility="collapsed",
        key="wacht_pills",
    )

    if chosen_w is not None:
        st.session_state.wachttijd = int(chosen_w)

    st.markdown('<p style="font-size:13px;color:#8089A8;margin-top:14px;">Op uw polisblad staat dit als <em>"eigen risico periode"</em></p>', unsafe_allow_html=True)

    nav(back_lbl="← Terug", next_lbl="Volgende →",
        next_key="v3_next", back_key="v3_back")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — PREMIE
# ══════════════════════════════════════════════════════════════════════════════
elif step == 4:
    st.markdown(q_head(4, TOTAL_Q,
        "Welk premiepercentage betaalt u nu?",
        f'Het marktgemiddelde voor fysiotherapeuten is <strong style="color:#0B1530">{MARKT_GEMIDDELD}%</strong>. Sleep de slider, of vul uw exacte jaarpremie in.'
    ), unsafe_allow_html=True)

    pct = st.session_state.get("premie_slider", st.session_state.premie_pct)
    above = pct > MARKT_GEMIDDELD
    pct_color = "#D14D2C" if above else "#0B1530"
    pill_cls = "above" if above else "below"
    diff = abs(pct - MARKT_GEMIDDELD)
    pill_txt = f"↑ {diff:.1f}% boven marktgemiddelde" if above else f"↓ Onder of gelijk aan marktgemiddelde"

    pct_formatted = f"{pct:.1f}"
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-pct" style="color:{pct_color};">
            {pct_formatted}<span class="unit">%</span>
        </div>
        <div><span class="market-pill {pill_cls}">{pill_txt}</span></div>
    </div>""", unsafe_allow_html=True)

    pct_new = st.slider("premie_pct", 0.0, 12.0, st.session_state.premie_pct, 0.1,
                        key="premie_slider", label_visibility="collapsed", format="%.1f%%")
    st.session_state.premie_pct = pct_new

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:12px;color:#8089A8;margin-top:6px;position:relative;">
        <span>0%</span>
        <span style="position:absolute;left:{((MARKT_GEMIDDELD)/12*100):.1f}%;transform:translateX(-50%);
            font-size:10px;background:#fff;padding:2px 8px;border-radius:4px;border:1px solid #DCE0EC;
            color:#5A6488;letter-spacing:.08em;text-transform:uppercase;top:-22px;">{MARKT_GEMIDDELD}% markt</span>
        <span>12%</span>
    </div>""", unsafe_allow_html=True)

    # "Comes to" card
    euros_calc = st.session_state.loon * (pct_new / 100)
    euros_fmt = f"{int(round(euros_calc)):,}".replace(",", ".")
    st.markdown(f"""
    <div style="margin-top:28px;padding:18px 22px;background:#F5F7FB;border-radius:14px;
        display:flex;align-items:center;justify-content:space-between;gap:16px;">
        <div>
            <div style="font-size:12px;color:#5A6488;text-transform:uppercase;letter-spacing:.08em;">Komt neer op</div>
            <div style="font-size:22px;font-weight:700;color:#0B1530;margin-top:4px;font-variant-numeric:tabular-nums;">
                € {euros_fmt} / jaar
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Optional exact euros
    st.markdown('<div style="margin-top:16px;"><span style="font-size:13px;color:#5A6488;">Of vul uw exacte jaarpremie in <span style="font-size:10px;background:#EBEEF5;padding:2px 6px;border-radius:4px;margin-left:4px;font-weight:600;letter-spacing:.08em;">OPTIONEEL</span></span></div>', unsafe_allow_html=True)
    jp = st.number_input("jaarpremie", min_value=0, max_value=999_999, step=500,
                         value=st.session_state.jaarpremie or None,
                         placeholder="bijv. 12.500",
                         key="jaarpremie_input", label_visibility="collapsed")
    if jp:
        st.session_state.jaarpremie = int(jp)

    nav(back_lbl="← Terug", next_lbl="Bereken mijn besparing →",
        next_key="v4_next", back_key="v4_back")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif step == 5:
    loon     = st.session_state.loon
    wachttijd = st.session_state.wachttijd
    jp       = st.session_state.jaarpremie

    if jp and jp > 0 and loon > 0:
        eff_pct = (jp / loon) * 100
    else:
        eff_pct = st.session_state.premie_pct

    results = calculate_fysio(loon, wachttijd, eff_pct)
    our_rate = results["our_rate"]
    onze     = results["onzePremie"]
    huidig   = results["huidigePremie"]
    besparing = results["besparing"]
    bes_pct  = results["besparingPct"]

    bes_fmt  = f"{int(round(besparing)):,}".replace(",", ".")
    huid_fmt = f"{int(round(huidig)):,}".replace(",", ".")
    onze_fmt = f"{int(round(onze)):,}".replace(",", ".")
    pct_show = round(bes_pct)

    st.markdown(f"""
    <div class="q-pill result">✓ Resultaat</div>
    <h1 class="q-title">U bespaart naar verwachting <span style="color:#1040C5;">{pct_show}%</span> op uw verzuimverzekering.</h1>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-hero">
        <div class="result-hero-glow"></div>
        <div style="position:relative;z-index:1;">
            <div class="result-save-label">Geschatte jaarbesparing</div>
            <div class="result-save-amount"><span class="eur">€&nbsp;</span>{bes_fmt}</div>
            <div><span class="result-save-pill">↓ {pct_show}% lager dan uw huidige premie</span></div>
        </div>
    </div>
    <div class="compare-grid">
        <div class="compare-card" style="background:#F5F7FB;">
            <div class="cc-label">Uw huidige premie</div>
            <div class="cc-amount" style="color:#2A3454;">€ {huid_fmt}</div>
            <div class="cc-sub">per jaar · {eff_pct:.1f}%</div>
        </div>
        <div class="compare-card" style="background:#F4F7FD;">
            <div class="cc-label">Verwachte nieuwe premie</div>
            <div class="cc-amount" style="color:#1040C5;">€ {onze_fmt}</div>
            <div class="cc-sub">per jaar · {our_rate:.3f}%</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.session_state["_besparing"] = int(round(besparing))
    st.session_state["_huidig_pct"] = eff_pct

    st.markdown('<div style="margin-top:36px;"></div>', unsafe_allow_html=True)

    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("← Terug", key="v5_back", type="secondary"):
            go_back()
    with col_n:
        if st.button("Claim deze besparing →", key="v5_next",
                     type="primary", use_container_width=True):
            go_next()

    st.markdown("""
    <p style="margin-top:24px;font-size:12px;color:#8089A8;line-height:1.6;font-style:italic;">
        Schatting op basis van mandaat Fysiotherapie 100%/100%/70%/70%. De werkelijke premie wordt vastgesteld na een officiële offerteaanvraag.
    </p>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — GEGEVENS
# ══════════════════════════════════════════════════════════════════════════════
elif step == 6:
    if not st.session_state.submitted:
        besparing = st.session_state.get("_besparing", 0)
        bes_fmt = f"{besparing:,}".replace(",", ".")

        st.markdown(q_head(5, TOTAL_Q,
            "Naar wie sturen we uw besparing?",
            "Persoonlijk overzicht in uw inbox binnen 1 minuut. Geen verkooppraatjes — eerlijke vergelijking met 6 verzekeraars."
        ), unsafe_allow_html=True)

        if besparing:
            st.markdown(f"""
            <div class="besparing-reminder">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#0E7C66;font-weight:600;">Klaar om verzonden te worden</div>
                    <div style="font-size:15px;font-weight:600;color:#0B1530;margin-top:4px;">
                        Uw besparing van <span style="color:#1040C5;font-variant-numeric:tabular-nums;">€ {bes_fmt}</span> per jaar
                    </div>
                </div>
                <div style="width:36px;height:36px;border-radius:999px;background:#1ABC9C;color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">✉</div>
            </div>""", unsafe_allow_html=True)

        with st.form("lead_form"):
            st.text_input("Bedrijfsnaam *", placeholder="Fysiotherapie Voorbeeld B.V.",
                          value=st.session_state.bedrijf, key="form_bedrijf")
            st.text_input("E-mailadres *", placeholder="naam@bedrijf.nl",
                          value=st.session_state.email, key="form_email")
            st.text_input("Telefoonnummer *", placeholder="06 12 34 56 78",
                          value=st.session_state.tel, key="form_tel")
            st.markdown('<p style="font-size:12px;color:#8089A8;margin-top:4px;">🔒 Versleuteld verzonden · we delen niets met derden</p>', unsafe_allow_html=True)
            sub = st.form_submit_button("Stuur naar mij →", use_container_width=True)
            if sub:
                st.session_state.bedrijf = st.session_state.form_bedrijf
                st.session_state.email   = st.session_state.form_email
                st.session_state.tel     = st.session_state.form_tel
                st.session_state.submitted = True
                go_next()

        st.markdown('<div class="nav-back" style="margin-top:8px;">', unsafe_allow_html=True)
        if st.button("← Terug naar uw besparing", key="v6_back"):
            go_back()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        go_next()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — DONE
# ══════════════════════════════════════════════════════════════════════════════
elif step == 7:
    besparing = st.session_state.get("_besparing", 0)
    bes_fmt   = f"{besparing:,}".replace(",", ".")
    bedrijf   = st.session_state.bedrijf
    email_addr = st.session_state.email

    st.markdown(f"""
    <div class="done-check">✓</div>
    <h1 class="q-title">Bedankt{", " + bedrijf if bedrijf else ""}.</h1>
    <p class="q-helper" style="margin-top:14px;">
        Uw persoonlijke overzicht — met een verwachte besparing van
        <strong style="color:#0B1530;">€ {bes_fmt} per jaar</strong> — is onderweg
        naar <strong style="color:#0B1530;">{email_addr or "uw inbox"}</strong>.
        Een adviseur belt u binnen 1 werkdag.
    </p>""", unsafe_allow_html=True)

    st.markdown('<div style="margin-top:32px;"></div>', unsafe_allow_html=True)
    if st.button("Nieuwe berekening", key="restart"):
        for k in ["step","verzuim","loon","wachttijd","premie_pct","jaarpremie",
                  "bedrijf","email","tel","submitted","_besparing","_huidig_pct"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()


# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vvz-disclaimer">
    Deze berekening is een schatting op basis van het mandaat Fysiotherapie 100%/100%/70%/70%
    en uw opgegeven verzuimprofiel. De werkelijke premie wordt vastgesteld na een officiële offerteaanvraag.
    Aan deze berekening kunnen geen rechten worden ontleend.
</div>""", unsafe_allow_html=True)
