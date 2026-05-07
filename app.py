import streamlit as st
from calculations import (
    calculate_fysio, VERZUIM_KLASSEN, WACHTWEKEN_OPTIES,
    format_currency, MARKT_GEMIDDELD,
)

st.set_page_config(
    page_title="VVZ Calculator Fysiotherapie – verzekerverzuim.nl",
    page_icon="💼",
    layout="centered",
)

for k, v in {
    "page": "calculator",
    "submitted": False,
    "result_verzuimklasse": None,
    "result_wachtweken": None,
    "result_loonsom": 800_000,
    "result_current_pct": MARKT_GEMIDDELD,
    "_onze_premie": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

ACCENT = "#0b349d"

LOGO_SVG = """<svg width="115" height="36" viewBox="0 0 230 72" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M40.2852 64.1741C38.2328 67.7164 33.1005 67.7164 31.0477 64.1741L1.60286 13.3644C-0.449942 9.82215 2.11606 5.39429 6.2217 5.39429H65.1114C69.2172 5.39429 71.783 9.82215 69.7301 13.3644L40.2852 64.1741Z" fill="#015EE1"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M38.4077 23.4377H32.4816V29.3414H26.5557V35.2455H32.4816V41.1492H38.4077V35.2455H44.3334V29.3414H38.4077V23.4377Z" fill="white"/>
<path d="M26.7118 39.9742C24.6512 43.4753 19.5709 43.4753 17.5103 39.9742L1.80171 13.2848C-0.283092 9.74264 2.28086 5.28369 6.40246 5.28369H37.8195C41.9413 5.28369 44.5053 9.74264 42.4204 13.2848L26.7118 39.9742Z" fill="#1040C5"/>
<path d="M21.8888 48.4551L35.2222 25.2088L27.4444 21.2238L11.4444 7.94019L1.22217 12.368L21.8888 48.4551Z" fill="#1040C5"/>
<path d="M91.4426 14.1219H96.38L90.724 30.9651H86.1613L80.4897 14.1219H85.4582L88.4426 25.2054L91.4426 14.1219ZM106.193 31.2764C104.412 31.2764 102.885 30.908 101.615 30.1712C100.354 29.4344 99.3853 28.4483 98.7084 27.2135C98.0417 25.9786 97.7084 24.6139 97.7084 23.1195V22.5124C97.7084 20.8312 98.0262 19.3368 98.6613 18.0292C99.3071 16.7216 100.224 15.6942 101.412 14.947C102.599 14.1894 104.016 13.8106 105.661 13.8106C108.109 13.8106 109.974 14.5682 111.255 16.0833C112.536 17.5881 113.177 19.591 113.177 22.0921V24.0846H102.505C102.672 25.112 103.099 25.937 103.787 26.5597C104.484 27.172 105.385 27.4782 106.49 27.4782C107.292 27.4782 108.036 27.3329 108.724 27.0423C109.422 26.7413 110.021 26.2743 110.521 25.6413L112.802 28.2411C112.271 28.9987 111.448 29.6939 110.333 30.327C109.219 30.9598 107.839 31.2764 106.193 31.2764ZM105.63 17.5933C104.703 17.5933 103.995 17.9046 103.505 18.5273C103.016 19.1396 102.693 19.9387 102.536 20.9246H108.536V20.551C108.526 19.6896 108.287 18.9839 107.818 18.4339C107.36 17.8735 106.63 17.5933 105.63 17.5933ZM120.364 30.9651H115.646V14.1219H120.084L120.24 16.13C120.646 15.4036 121.161 14.838 121.787 14.4333C122.412 14.0182 123.136 13.8106 123.958 13.8106C124.198 13.8106 124.448 13.8314 124.708 13.8728C124.979 13.904 125.198 13.9507 125.364 14.0129L125.302 18.5429C125.073 18.5117 124.797 18.4858 124.474 18.465C124.161 18.4339 123.885 18.4184 123.646 18.4184C121.969 18.4184 120.875 18.9632 120.364 20.0529V30.9651ZM140.99 30.9651H126.88V28.1476L134.677 17.9046H127.13V14.1219H140.755V16.8616L132.912 27.1824H140.99V30.9651ZM151.661 31.2764C149.88 31.2764 148.354 30.908 147.084 30.1712C145.823 29.4344 144.854 28.4483 144.177 27.2135C143.51 25.9786 143.177 24.6139 143.177 23.1195V22.5124C143.177 20.8312 143.495 19.3368 144.13 18.0292C144.776 16.7216 145.693 15.6942 146.88 14.947C148.068 14.1894 149.484 13.8106 151.13 13.8106C153.578 13.8106 155.443 14.5682 156.724 16.0833C158.005 17.5881 158.646 19.591 158.646 22.0921V24.0846H147.974C148.14 25.112 148.568 25.937 149.255 26.5597C149.953 27.172 150.854 27.4782 151.958 27.4782C152.76 27.4782 153.505 27.3329 154.193 27.0423C154.891 26.7413 155.49 26.2743 155.99 25.6413L158.271 28.2411C157.74 28.9987 156.916 29.6939 155.802 30.327C154.688 30.9598 153.307 31.2764 151.661 31.2764ZM151.099 17.5933C150.172 17.5933 149.464 17.9046 148.974 18.5273C148.484 19.1396 148.161 19.9387 148.005 20.9246H154.005V20.551C153.995 19.6896 153.755 18.9839 153.287 18.4339C152.828 17.8735 152.099 17.5933 151.099 17.5933ZM165.833 30.9651H161.115V7.03906H165.833V20.1151L166.63 19.1033L170.818 14.1219H176.49L170.443 21.1114L176.99 30.9651H171.568L167.412 24.3493L165.833 25.9215V30.9651ZM186.224 31.2764C184.443 31.2764 182.916 30.908 181.646 30.1712C180.385 29.4344 179.417 28.4483 178.74 27.2135C178.073 25.9786 177.74 24.6139 177.74 23.1195V22.5124C177.74 20.8312 178.057 19.3368 178.693 18.0292C179.339 16.7216 180.255 15.6942 181.443 14.947C182.63 14.1894 184.047 13.8106 185.693 13.8106C188.14 13.8106 190.005 14.5682 191.287 16.0833C192.568 17.5881 193.208 19.591 193.208 22.0921V24.0846H182.536C182.703 25.112 183.13 25.937 183.818 26.5597C184.516 27.172 185.417 27.4782 186.521 27.4782C187.323 27.4782 188.068 27.3329 188.755 27.0423C189.453 26.7413 190.052 26.2743 190.552 25.6413L192.833 28.2411C192.302 28.9987 191.479 29.6939 190.364 30.327C189.25 30.9598 187.87 31.2764 186.224 31.2764ZM185.661 17.5933C184.734 17.5933 184.026 17.9046 183.536 18.5273C183.047 19.1396 182.724 19.9387 182.568 20.9246H188.568V20.551C188.557 19.6896 188.318 18.9839 187.849 18.4339C187.391 17.8735 186.661 17.5933 185.661 17.5933ZM200.396 30.9651H195.677V14.1219H200.115L200.271 16.13C200.677 15.4036 201.193 14.838 201.818 14.4333C202.443 14.0182 203.167 13.8106 203.99 13.8106C204.229 13.8106 204.479 13.8314 204.74 13.8728C205.01 13.904 205.229 13.9507 205.396 14.0129L205.333 18.5429C205.104 18.5117 204.828 18.4858 204.505 18.465C204.193 18.4339 203.916 18.4184 203.677 18.4184C202 18.4184 200.906 18.9632 200.396 20.0529V30.9651ZM91.8333 46.0026H95.8489L90.0053 62.8457H86.552L80.6613 46.0026H84.6929L88.2866 57.9888L91.8333 46.0026ZM105.646 63.157C103.969 63.157 102.521 62.7992 101.302 62.0828C100.084 61.3566 99.1457 60.3811 98.4897 59.1564C97.8333 57.9215 97.5053 56.5413 97.5053 55.0155V54.3774C97.5053 52.6235 97.8386 51.0981 98.5053 49.8008C99.172 48.4932 100.084 47.4815 101.24 46.7655C102.406 46.049 103.724 45.6913 105.193 45.6913C106.818 45.6913 108.167 46.0442 109.24 46.7495C110.312 47.4451 111.115 48.4153 111.646 49.6609C112.177 50.8958 112.443 52.3277 112.443 53.9572V55.623H101.412C101.516 56.8991 101.958 57.9578 102.74 58.7982C103.521 59.6284 104.568 60.0437 105.88 60.0437C106.787 60.0437 107.588 59.8671 108.287 59.5146C108.984 59.1617 109.594 58.653 110.115 57.9888L112.146 60.0127C111.604 60.8115 110.802 61.5381 109.74 62.1917C108.677 62.8355 107.312 63.157 105.646 63.157ZM105.177 48.789C104.146 48.789 103.318 49.1521 102.693 49.8787C102.068 50.6049 101.667 51.591 101.49 52.8365H108.615V52.5407C108.594 51.8867 108.464 51.2744 108.224 50.7036C107.995 50.1329 107.63 49.671 107.13 49.3181C106.64 48.9652 105.99 48.789 105.177 48.789ZM119.224 62.8457H115.349V46.0026H119.036L119.146 47.9482C119.573 47.253 120.104 46.703 120.74 46.2983C121.385 45.8936 122.14 45.6913 123.005 45.6913C123.224 45.6913 123.469 45.7121 123.74 45.7533C124.01 45.7949 124.213 45.8418 124.349 45.8936L124.318 49.5519C124.078 49.5205 123.823 49.4948 123.552 49.474C123.292 49.4426 123.031 49.4271 122.771 49.4271C121.854 49.4271 121.104 49.6037 120.521 49.9566C119.937 50.3095 119.505 50.8072 119.224 51.451V62.8457ZM139.802 62.8457H126.036V60.355L134.552 49.1158H126.224V46.0026H139.474V48.3998L130.896 59.748H139.802V62.8457ZM152.943 46.0026H156.818V62.8457H153.161L153.068 61.1489C152.536 61.7821 151.88 62.2749 151.099 62.6278C150.318 62.9807 149.391 63.157 148.318 63.157C146.651 63.157 145.302 62.6695 144.271 61.6936C143.24 60.7181 142.724 59.1148 142.724 56.8836V46.0026H146.599V56.9146C146.599 58.0875 146.864 58.8969 147.396 59.3433C147.927 59.779 148.557 59.9968 149.287 59.9968C150.245 59.9968 151.016 59.8259 151.599 59.4832C152.193 59.1303 152.64 58.6583 152.943 58.0667V46.0026ZM160.63 41.5973C160.63 41.0057 160.823 40.5178 161.208 40.1339C161.594 39.7393 162.13 39.5423 162.818 39.5423C163.505 39.5423 164.047 39.7393 164.443 40.1339C164.839 40.5178 165.036 41.0057 165.036 41.5973C165.036 42.1782 164.839 42.6662 164.443 43.0602C164.047 43.4446 163.505 43.6363 162.818 43.6363C162.13 43.6363 161.594 43.4446 161.208 43.0602C160.823 42.6662 160.63 42.1782 160.63 41.5973ZM164.755 62.8457H160.88V46.0026H164.755V62.8457ZM172.724 62.8457H168.833V46.0026H172.49L172.615 47.8392C173.177 47.1649 173.864 46.6406 174.677 46.2673C175.5 45.883 176.448 45.6913 177.521 45.6913C178.563 45.6913 179.484 45.8989 180.287 46.3138C181.088 46.7292 181.708 47.388 182.146 48.2909C182.698 47.5023 183.406 46.8744 184.271 46.4073C185.146 45.9299 186.167 45.6913 187.333 45.6913C189.052 45.6913 190.401 46.1739 191.38 47.1387C192.37 48.104 192.864 49.718 192.864 51.9802V62.8457H188.974V51.9492C188.974 50.7142 188.703 49.8889 188.161 49.474C187.63 49.0587 186.912 48.8514 186.005 48.8514C185.161 48.8514 184.469 49.0742 183.927 49.5205C183.385 49.9668 183.005 50.5482 182.787 51.2642C182.787 51.3784 182.787 51.4975 182.787 51.6219V62.8457H178.912V51.9802C178.912 50.7869 178.64 49.9668 178.099 49.5205C177.568 49.0742 176.844 48.8514 175.927 48.8514C175.125 48.8514 174.464 49.0223 173.943 49.3651C173.422 49.6972 173.016 50.1537 172.724 50.7346V62.8457ZM196.677 60.4639C196.677 59.7271 196.927 59.1148 197.427 58.6273C197.927 58.1393 198.588 57.8953 199.412 57.8953C200.234 57.8953 200.891 58.1393 201.38 58.6273C201.88 59.1148 202.13 59.7271 202.13 60.4639C202.13 61.1906 201.88 61.7976 201.38 62.2851C200.891 62.7731 200.234 63.017 199.412 63.017C198.588 63.017 197.927 62.7731 197.427 62.2851C196.927 61.7976 196.677 61.1906 196.677 60.4639ZM210.677 62.8457H205.802V46.0026H210.38L210.536 47.9017C211.734 46.4281 213.339 45.6913 215.349 45.6913C216.412 45.6913 217.344 45.8989 218.146 46.3138C218.948 46.7185 219.573 47.3982 220.021 48.3533C220.469 49.2973 220.693 50.5792 220.693 52.198V62.8457H215.787V52.167C215.787 51.1601 215.568 50.4858 215.13 50.143C214.693 49.8008 214.068 49.6294 213.255 49.6294C212.651 49.6294 212.136 49.749 211.708 49.9876C211.292 50.2263 210.948 50.5584 210.677 50.9839V62.8457ZM229.052 62.8457H224.161V38.9352H229.052V62.8457Z" fill="white"/>
</svg>"""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    padding: 0 1rem 5rem !important;
    max-width: 640px !important;
}}
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    color: #111827;
}}
.stApp {{ background: #ffffff; }}

/* ── Header ── */
.vvz-header {{
    background-color: {ACCENT};
    padding: 14px 24px;
    margin: 0 -1rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.vvz-header a.meer {{
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    font-size: 12px;
}}
.vvz-header a.meer:hover {{ color: #fff; }}

/* ── Hero ── */
.vvz-hero {{
    text-align: center;
    padding: 40px 0 28px;
}}
.vvz-hero h1 {{
    font-size: 30px;
    font-weight: 900;
    color: #111827;
    line-height: 1.25;
    margin-bottom: 12px;
}}
.vvz-hero .accent {{ color: {ACCENT}; }}
.vvz-hero p {{
    color: #6b7280;
    font-size: 15px;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* ── Step indicator ── */
.step-bar {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin-bottom: 28px;
}}
.step-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}}
.step-dot {{
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700;
    border: 2px solid #e2e8f0;
    color: #9ca3af;
    background: #fff;
}}
.step-dot.active {{ border-color: {ACCENT}; color: {ACCENT}; background: #fff; }}
.step-dot.done {{ border-color: {ACCENT}; color: #fff; background: {ACCENT}; }}
.step-name {{
    font-size: 11px; font-weight: 600;
    color: #9ca3af; white-space: nowrap;
}}
.step-name.active, .step-name.done {{ color: {ACCENT}; }}
.step-line {{
    width: 48px; height: 2px;
    background: #e2e8f0;
    margin: 0 4px 18px;
    flex-shrink: 0;
}}
.step-line.done {{ background: {ACCENT}; }}

/* ── Card ── */
.card {{
    background: #ffffff;
    border: 1.5px solid #e8edf5;
    border-radius: 18px;
    padding: 32px 28px;
    margin-bottom: 16px;
}}

/* ── Input labels ── */
.q-label {{
    display: block;
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
    line-height: 1.3;
}}
.q-hint {{
    display: block;
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 12px;
    line-height: 1.5;
}}
.q-optional {{
    font-size: 11px;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-left: 8px;
    vertical-align: middle;
}}
.q-sep {{
    border: none;
    border-top: 1px solid #f1f5f9;
    margin: 28px 0;
}}

/* ── Selectbox ── */
.stSelectbox label {{ display: none !important; }}
.stSelectbox [data-baseweb="select"] > div:first-child {{
    background: #f8fafc !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    min-height: 54px !important;
    padding: 0 18px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #111827 !important;
    cursor: pointer !important;
    transition: border-color 0.15s !important;
}}
.stSelectbox [data-baseweb="select"] > div:first-child:hover {{
    border-color: {ACCENT} !important;
    background: #fff !important;
}}

/* ── Slider ── */
.slider-top {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
}}
.slider-amount {{
    font-size: 22px;
    font-weight: 800;
    color: {ACCENT};
}}
.slider-minmax {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #9ca3af;
    margin-top: 6px;
}}

/* ── Number input ── */
.stNumberInput label {{ display: none !important; }}
.stNumberInput input {{
    background: #f8fafc !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
    min-height: 54px !important;
    padding: 0 18px !important;
}}
.stNumberInput input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT}40 !important;
    background: #fff !important;
    outline: none !important;
}}

/* ── Buttons ── */
.stButton > button {{
    width: 100% !important;
    background-color: {ACCENT} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 18px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
    transition: background-color 0.15s, transform 0.1s !important;
    margin-top: 8px !important;
}}
.stButton > button:hover {{ background-color: #092a7a !important; }}
.stButton > button:disabled {{
    background-color: #e2e8f0 !important;
    color: #9ca3af !important;
    cursor: not-allowed !important;
}}
div[data-testid="stFormSubmitButton"] button {{
    width: 100% !important;
    background-color: {ACCENT} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 18px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    margin-top: 8px !important;
}}
div[data-testid="stFormSubmitButton"] button:hover {{
    background-color: #092a7a !important;
}}

/* ── Results ── */
.result-card {{
    background: linear-gradient(145deg, #f0f4ff 0%, #f8fafc 100%);
    border: 1.5px solid #c7d4f5;
    border-radius: 18px;
    padding: 40px 28px 32px;
    text-align: center;
    margin-bottom: 16px;
}}
.result-tag {{
    font-size: 11px;
    font-weight: 800;
    color: {ACCENT};
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 14px;
}}
.result-amount {{
    font-size: 60px;
    font-weight: 900;
    color: #111827;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 10px;
}}
.result-sub {{
    font-size: 15px;
    color: #6b7280;
    line-height: 1.5;
}}
.result-detail {{
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid #dde4f0;
}}
.result-detail-item {{
    text-align: center;
}}
.result-detail-lbl {{
    font-size: 11px;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 4px;
}}
.result-detail-val {{
    font-size: 17px;
    font-weight: 800;
    color: #111827;
}}
.result-detail-val.green {{ color: #16a34a; }}

/* ── Op aanvraag ── */
.aanvraag-card {{
    background: #f8fafc;
    border: 1.5px solid #e8edf5;
    border-radius: 18px;
    padding: 40px 28px;
    text-align: center;
    margin-bottom: 16px;
}}

/* ── Lead form ── */
.form-title {{
    font-size: 20px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 6px;
}}
.form-sub {{
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 24px;
    line-height: 1.5;
}}
.stTextInput label {{
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #374151 !important;
}}
.stTextInput input {{
    background: #f8fafc !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
    min-height: 48px !important;
    padding: 0 16px !important;
}}
.stTextInput input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT}40 !important;
    background: #fff !important;
    outline: none !important;
}}

/* ── Success ── */
.success-card {{
    background: #f0fdf4;
    border: 1.5px solid #bbf7d0;
    border-radius: 18px;
    padding: 48px 28px;
    text-align: center;
    margin-bottom: 16px;
}}
.success-icon {{
    width: 64px; height: 64px;
    background: #dcfce7;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 18px;
}}
.success-card h2 {{ font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 10px; }}
.success-card p {{ font-size: 15px; color: #6b7280; max-width: 340px; margin: 0 auto 20px; line-height: 1.6; }}
.success-badge {{
    display: inline-block;
    background: #dcfce7;
    border: 1px solid #86efac;
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 14px; font-weight: 700; color: #16a34a;
}}

/* ── Disclaimer / footer ── */
.vvz-disclaimer {{
    font-size: 11px; color: #9ca3af; text-align: center; line-height: 1.7;
    border-top: 1px solid #e8edf5; padding-top: 24px; margin-top: 8px;
    font-style: italic;
}}
.vvz-footer {{
    border-top: 1px solid #e8edf5;
    padding: 20px 0;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #9ca3af;
    margin-top: 4px;
}}
</style>
""", unsafe_allow_html=True)


# ── Helper: step bar ───────────────────────────────────────────────────────────
def step_bar(active: int) -> str:
    labels = ["Uw situatie", "Uw besparing", "Uw gegevens"]
    check  = '<svg width="14" height="14" fill="none" stroke="white" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'
    html   = '<div class="step-bar">'
    for i, lbl in enumerate(labels):
        done   = i < active
        cur    = i == active
        d_cls  = "step-dot done" if done else ("step-dot active" if cur else "step-dot")
        n_cls  = "step-name done" if done else ("step-name active" if cur else "step-name")
        inner  = check if done else str(i + 1)
        html  += f'<div class="step-item"><div class="{d_cls}">{inner}</div><div class="{n_cls}">{lbl}</div></div>'
        if i < len(labels) - 1:
            l_cls = "step-line done" if done else "step-line"
            html += f'<div class="{l_cls}"></div>'
    return html + "</div>"


# ── Shared header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="vvz-header">
    <a href="https://verzekerverzuim.nl">{LOGO_SVG}</a>
    <a class="meer" href="https://verzekerverzuim.nl">Meer informatie →</a>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STAP 1 — UW SITUATIE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "calculator":

    st.markdown("""
    <div class="vvz-hero">
        <h1>Betaalt u te veel voor uw<br><span class="accent">verzuimverzekering?</span></h1>
        <p>Beantwoord 3 korte vragen. We berekenen direct hoeveel u kunt besparen.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(step_bar(0), unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Vraag 1
    st.markdown("""
    <span class="q-label">Hoe hoog is het ziekteverzuim in uw praktijk?</span>
    <span class="q-hint">Kijk naar het gemiddelde van de afgelopen 3 jaar.
    Weet u het niet precies? Kies dan de klasse iets hoger.</span>
    """, unsafe_allow_html=True)
    verzuimklasse = st.selectbox(
        "verzuim", ["Kies uw verzuimpercentage..."] + VERZUIM_KLASSEN,
        key="verzuim_select", label_visibility="collapsed",
    )

    st.markdown('<hr class="q-sep">', unsafe_allow_html=True)

    # Vraag 2
    st.markdown("""
    <span class="q-label">Hoelang betaalt u zelf het loon door als iemand ziek is?</span>
    <span class="q-hint">Dit noemen we de wachttijd. Het staat op uw polisblad als
    "eigen risico" of "wachttijd". Weet u het niet? Bel ons even.</span>
    """, unsafe_allow_html=True)
    wachtweken = st.selectbox(
        "wachttijd", WACHTWEKEN_OPTIES,
        format_func=lambda x: f"{x} weken",
        key="wachttijd_select", index=None,
        placeholder="Kies uw wachttijd...",
        label_visibility="collapsed",
    )

    st.markdown('<hr class="q-sep">', unsafe_allow_html=True)

    # Vraag 3
    loonsom_val = st.session_state.get("loonsom_slider", 800_000)
    st.markdown(f"""
    <div class="slider-top">
        <span class="q-label" style="margin-bottom:0">Hoeveel loon betaalt u in totaal per jaar?</span>
        <span class="slider-amount">{format_currency(loonsom_val)}</span>
    </div>
    <span class="q-hint">Tel alle salarissen van uw medewerkers bij elkaar op (vóór belasting).</span>
    """, unsafe_allow_html=True)
    loonsom = st.slider(
        "loonsom", 100_000, 3_000_000, 800_000, 50_000,
        key="loonsom_slider", label_visibility="collapsed",
    )
    st.markdown(f"""<div class="slider-minmax">
        <span>{format_currency(100_000)}</span>
        <span>{format_currency(3_000_000)}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="q-sep">', unsafe_allow_html=True)

    # Vraag 4 — huidig premiepercentage (slider, default marktgemiddelde)
    current_pct = st.session_state.get("current_pct_slider", MARKT_GEMIDDELD)
    huidig_euros = loonsom * (current_pct / 100)
    st.markdown(f"""
    <div class="slider-top">
        <span class="q-label" style="margin-bottom:0">Welk premiepercentage betaalt u nu?</span>
        <span class="slider-amount">{current_pct:.1f}%</span>
    </div>
    <span class="q-hint">Het gemiddelde in de markt is <strong>{MARKT_GEMIDDELD}%</strong> —
    weet u uw exacte tarief? Pas de slider dan aan.</span>
    """, unsafe_allow_html=True)
    current_pct = st.slider(
        "current_pct", 0.0, 8.0, MARKT_GEMIDDELD, 0.1,
        key="current_pct_slider", label_visibility="collapsed",
        format="%.1f%%",
    )
    huidig_euros = loonsom * (current_pct / 100)
    st.markdown(f"""
    <div style="text-align:right; font-size:13px; color:#6b7280; margin-top:4px;">
        = circa {format_currency(huidig_euros)} per jaar
    </div>""", unsafe_allow_html=True)

    # Kleinere optionele euros-invoer onderaan
    st.markdown("""
    <div style="margin-top:20px;">
        <span style="font-size:13px;font-weight:600;color:#6b7280;">
            Of: weet u uw exacte jaarpremie?
            <span class="q-optional">Optioneel</span>
        </span>
    </div>""", unsafe_allow_html=True)
    huidige_premie_euros = st.number_input(
        "premie_euros", min_value=0, max_value=500_000, step=500,
        value=None, placeholder="bijv. 12.500",
        key="premie_input", label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    all_required = (
        verzuimklasse != "Kies uw verzuimpercentage..."
        and wachtweken is not None
    )

    if st.button("Bereken mijn besparing →", use_container_width=True, disabled=not all_required):
        # Als exacte euros ingevuld: reken terug naar %; anders gebruik slider
        if huidige_premie_euros and huidige_premie_euros > 0 and loonsom > 0:
            effective_pct = (huidige_premie_euros / loonsom) * 100
        else:
            effective_pct = current_pct
        st.session_state.result_verzuimklasse = verzuimklasse
        st.session_state.result_wachtweken    = wachtweken
        st.session_state.result_loonsom       = loonsom
        st.session_state.result_current_pct   = effective_pct
        st.session_state.page = "results"
        st.rerun()

    if not all_required:
        st.markdown(
            '<p style="text-align:center;font-size:13px;color:#9ca3af;margin-top:10px">'
            'Kies eerst uw verzuimpercentage en wachttijd om verder te gaan</p>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# STAP 2 — UW BESPARING
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":

    st.markdown('<div style="margin: 24px 0 16px;">', unsafe_allow_html=True)
    if st.button("← Terug", use_container_width=False):
        st.session_state.page = "calculator"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(step_bar(1), unsafe_allow_html=True)

    verzuimklasse = st.session_state.result_verzuimklasse
    wachtweken    = st.session_state.result_wachtweken
    loonsom       = st.session_state.result_loonsom
    current_pct   = st.session_state.result_current_pct

    results = calculate_fysio(loonsom, verzuimklasse, wachtweken, current_pct)

    if results is None:
        # 8%+ → op aanvraag
        st.markdown("""
        <div class="aanvraag-card">
            <div class="result-tag">Persoonlijke berekening nodig</div>
            <div style="font-size:28px;font-weight:900;color:#111827;margin-bottom:12px;">
                Maatwerk offerte
            </div>
            <div class="result-sub">
                Bij een verzuim van 8% of hoger maken wij een offerte speciaal voor uw situatie.
                Vul uw gegevens in — binnen 24 uur ontvangt u een persoonlijke berekening.
            </div>
        </div>""", unsafe_allow_html=True)
        onze_premie_display = None

    else:
        our_rate  = results["our_rate"]
        onze      = results["onzePremie"]
        huidig    = results["huidigePremie"]
        besparing = results["besparing"]
        bes_pct   = results["besparingPct"]
        bes_show  = max(0, besparing)
        pct_show  = max(0.0, bes_pct)
        onze_premie_display = onze

        st.markdown(f"""
        <div class="result-card">
            <div class="result-tag">U kunt mogelijk dit bedrag besparen via verzekerverzuim.nl</div>
            <div class="result-amount">{format_currency(bes_show)}</div>
            <div class="result-sub">per jaar — {pct_show:.0f}% minder dan u nu betaalt</div>
            <div class="result-detail">
                <div class="result-detail-item">
                    <div class="result-detail-lbl">U betaalt nu</div>
                    <div class="result-detail-val">{format_currency(huidig)}</div>
                    <div style="font-size:11px;color:#9ca3af;margin-top:2px;">{current_pct:.1f}%</div>
                </div>
                <div class="result-detail-item" style="color:#d1d5db;font-size:24px;font-weight:300;padding-top:8px;">→</div>
                <div class="result-detail-item">
                    <div class="result-detail-lbl">Met ons betaalt u</div>
                    <div class="result-detail-val green">{format_currency(onze)}</div>
                    <div style="font-size:11px;color:#9ca3af;margin-top:2px;">{our_rate:.3f}%</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.session_state._onze_premie = onze_premie_display

    if st.button("Vraag deze besparing aan →", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()

    st.markdown(
        '<p style="text-align:center;font-size:13px;color:#9ca3af;margin-top:12px">'
        'Vrijblijvend · geen verplichtingen · binnen 24 uur offertes in uw inbox</p>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# STAP 3 — UW GEGEVENS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "form":

    st.markdown('<div style="margin: 24px 0 16px;">', unsafe_allow_html=True)
    if st.button("← Terug naar uw besparing", use_container_width=False):
        st.session_state.page = "results"
        st.session_state.submitted = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(step_bar(2), unsafe_allow_html=True)

    if not st.session_state.submitted:
        onze_premie = st.session_state.get("_onze_premie", None)
        premie_txt  = f" van {format_currency(onze_premie)} per jaar" if onze_premie else ""

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="form-title">Ontvang uw offertes gratis in uw inbox</div>
        <div class="form-sub">
            Wij vragen offertes op bij 6 verzekeraars op basis van uw profiel{premie_txt}.
            U ontvangt alles binnen 24 uur — geheel vrijblijvend.
        </div>""", unsafe_allow_html=True)

        with st.form("lead_form"):
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Uw naam *",       placeholder="Jan de Vries")
            with c2:
                st.text_input("Praktijknaam *",  placeholder="Fysiotherapie Centrum")
            st.text_input("E-mailadres *",        placeholder="jan@mijnpraktijk.nl")
            st.text_input("Telefoonnummer",       placeholder="06 12 34 56 78")
            submitted = st.form_submit_button("Stuur mij de offertes →")
            if submitted:
                st.session_state.submitted = True
                st.rerun()
            st.markdown(
                '<p style="text-align:center;font-size:12px;color:#9ca3af;margin-top:8px">'
                'Geen spam · uw gegevens worden nooit doorverkocht</p>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        onze_premie = st.session_state.get("_onze_premie", None)
        badge = (
            f'<div class="success-badge">Uw premie met ons: {format_currency(onze_premie)} per jaar</div>'
            if onze_premie
            else '<div class="success-badge">Uw offerte op maat volgt binnen 24 uur</div>'
        )
        st.markdown(f"""
        <div class="success-card">
            <div class="success-icon">
                <svg width="30" height="30" fill="none" stroke="#16a34a" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
            </div>
            <h2>Aanvraag verstuurd!</h2>
            <p>Wij gaan voor u aan de slag. U ontvangt binnen 24 uur offertes
            van 6 verzekeraars in uw inbox.</p>
            {badge}
        </div>""", unsafe_allow_html=True)


# ── Disclaimer & footer ────────────────────────────────────────────────────────
st.markdown("""
<div class="vvz-disclaimer">
    Deze berekening is een schatting op basis van het mandaat Fysiotherapie 100%/100%/70%/70%
    en uw opgegeven verzuimprofiel. De werkelijke premie wordt vastgesteld na een officiële offerteaanvraag.
    Aan deze berekening kunnen geen rechten worden ontleend.
</div>""", unsafe_allow_html=True)

from datetime import date
st.markdown(f"""
<div class="vvz-footer">
    <span>© {date.today().year} du Gardijn Verzekeringen · verzekerverzuim.nl</span>
    <span>AVG-proof · geen cookies zonder toestemming</span>
</div>""", unsafe_allow_html=True)
