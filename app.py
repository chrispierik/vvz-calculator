import streamlit as st
from calculations import (
    calculate_fysio, VERZUIM_KLASSEN, WACHTWEKEN_OPTIES,
    format_currency,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VVZ Calculator Fysiotherapie – verzekerverzuim.nl",
    page_icon="💼",
    layout="centered",
)

# ── State ──────────────────────────────────────────────────────────────────────
for k, v in {"submitted": False, "loonsom_touched": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def mark_loonsom():
    st.session_state.loonsom_touched = True

# ── Constants ─────────────────────────────────────────────────────────────────
ACCENT = "#0b349d"

LOGO_SVG = """<svg width="115" height="36" viewBox="0 0 230 72" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M40.2852 64.1741C38.2328 67.7164 33.1005 67.7164 31.0477 64.1741L1.60286 13.3644C-0.449942 9.82215 2.11606 5.39429 6.2217 5.39429H65.1114C69.2172 5.39429 71.783 9.82215 69.7301 13.3644L40.2852 64.1741Z" fill="#015EE1"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M38.4077 23.4377H32.4816V29.3414H26.5557V35.2455H32.4816V41.1492H38.4077V35.2455H44.3334V29.3414H38.4077V23.4377Z" fill="white"/>
<path d="M26.7118 39.9742C24.6512 43.4753 19.5709 43.4753 17.5103 39.9742L1.80171 13.2848C-0.283092 9.74264 2.28086 5.28369 6.40246 5.28369H37.8195C41.9413 5.28369 44.5053 9.74264 42.4204 13.2848L26.7118 39.9742Z" fill="#1040C5"/>
<path d="M21.8888 48.4551L35.2222 25.2088L27.4444 21.2238L11.4444 7.94019L1.22217 12.368L21.8888 48.4551Z" fill="#1040C5"/>
<path d="M91.4426 14.1219H96.38L90.724 30.9651H86.1613L80.4897 14.1219H85.4582L88.4426 25.2054L91.4426 14.1219ZM106.193 31.2764C104.412 31.2764 102.885 30.908 101.615 30.1712C100.354 29.4344 99.3853 28.4483 98.7084 27.2135C98.0417 25.9786 97.7084 24.6139 97.7084 23.1195V22.5124C97.7084 20.8312 98.0262 19.3368 98.6613 18.0292C99.3071 16.7216 100.224 15.6942 101.412 14.947C102.599 14.1894 104.016 13.8106 105.661 13.8106C108.109 13.8106 109.974 14.5682 111.255 16.0833C112.536 17.5881 113.177 19.591 113.177 22.0921V24.0846H102.505C102.672 25.112 103.099 25.937 103.787 26.5597C104.484 27.172 105.385 27.4782 106.49 27.4782C107.292 27.4782 108.036 27.3329 108.724 27.0423C109.422 26.7413 110.021 26.2743 110.521 25.6413L112.802 28.2411C112.271 28.9987 111.448 29.6939 110.333 30.327C109.219 30.9598 107.839 31.2764 106.193 31.2764ZM105.63 17.5933C104.703 17.5933 103.995 17.9046 103.505 18.5273C103.016 19.1396 102.693 19.9387 102.536 20.9246H108.536V20.551C108.526 19.6896 108.287 18.9839 107.818 18.4339C107.36 17.8735 106.63 17.5933 105.63 17.5933ZM120.364 30.9651H115.646V14.1219H120.084L120.24 16.13C120.646 15.4036 121.161 14.838 121.787 14.4333C122.412 14.0182 123.136 13.8106 123.958 13.8106C124.198 13.8106 124.448 13.8314 124.708 13.8728C124.979 13.904 125.198 13.9507 125.364 14.0129L125.302 18.5429C125.073 18.5117 124.797 18.4858 124.474 18.465C124.161 18.4339 123.885 18.4184 123.646 18.4184C121.969 18.4184 120.875 18.9632 120.364 20.0529V30.9651ZM140.99 30.9651H126.88V28.1476L134.677 17.9046H127.13V14.1219H140.755V16.8616L132.912 27.1824H140.99V30.9651ZM151.661 31.2764C149.88 31.2764 148.354 30.908 147.084 30.1712C145.823 29.4344 144.854 28.4483 144.177 27.2135C143.51 25.9786 143.177 24.6139 143.177 23.1195V22.5124C143.177 20.8312 143.495 19.3368 144.13 18.0292C144.776 16.7216 145.693 15.6942 146.88 14.947C148.068 14.1894 149.484 13.8106 151.13 13.8106C153.578 13.8106 155.443 14.5682 156.724 16.0833C158.005 17.5881 158.646 19.591 158.646 22.0921V24.0846H147.974C148.14 25.112 148.568 25.937 149.255 26.5597C149.953 27.172 150.854 27.4782 151.958 27.4782C152.76 27.4782 153.505 27.3329 154.193 27.0423C154.891 26.7413 155.49 26.2743 155.99 25.6413L158.271 28.2411C157.74 28.9987 156.916 29.6939 155.802 30.327C154.688 30.9598 153.307 31.2764 151.661 31.2764ZM151.099 17.5933C150.172 17.5933 149.464 17.9046 148.974 18.5273C148.484 19.1396 148.161 19.9387 148.005 20.9246H154.005V20.551C153.995 19.6896 153.755 18.9839 153.287 18.4339C152.828 17.8735 152.099 17.5933 151.099 17.5933ZM165.833 30.9651H161.115V7.03906H165.833V20.1151L166.63 19.1033L170.818 14.1219H176.49L170.443 21.1114L176.99 30.9651H171.568L167.412 24.3493L165.833 25.9215V30.9651ZM186.224 31.2764C184.443 31.2764 182.916 30.908 181.646 30.1712C180.385 29.4344 179.417 28.4483 178.74 27.2135C178.073 25.9786 177.74 24.6139 177.74 23.1195V22.5124C177.74 20.8312 178.057 19.3368 178.693 18.0292C179.339 16.7216 180.255 15.6942 181.443 14.947C182.63 14.1894 184.047 13.8106 185.693 13.8106C188.14 13.8106 190.005 14.5682 191.287 16.0833C192.568 17.5881 193.208 19.591 193.208 22.0921V24.0846H182.536C182.703 25.112 183.13 25.937 183.818 26.5597C184.516 27.172 185.417 27.4782 186.521 27.4782C187.323 27.4782 188.068 27.3329 188.755 27.0423C189.453 26.7413 190.052 26.2743 190.552 25.6413L192.833 28.2411C192.302 28.9987 191.479 29.6939 190.364 30.327C189.25 30.9598 187.87 31.2764 186.224 31.2764ZM185.661 17.5933C184.734 17.5933 184.026 17.9046 183.536 18.5273C183.047 19.1396 182.724 19.9387 182.568 20.9246H188.568V20.551C188.557 19.6896 188.318 18.9839 187.849 18.4339C187.391 17.8735 186.661 17.5933 185.661 17.5933ZM200.396 30.9651H195.677V14.1219H200.115L200.271 16.13C200.677 15.4036 201.193 14.838 201.818 14.4333C202.443 14.0182 203.167 13.8106 203.99 13.8106C204.229 13.8106 204.479 13.8314 204.74 13.8728C205.01 13.904 205.229 13.9507 205.396 14.0129L205.333 18.5429C205.104 18.5117 204.828 18.4858 204.505 18.465C204.193 18.4339 203.916 18.4184 203.677 18.4184C202 18.4184 200.906 18.9632 200.396 20.0529V30.9651ZM91.8333 46.0026H95.8489L90.0053 62.8457H86.552L80.6613 46.0026H84.6929L88.2866 57.9888L91.8333 46.0026ZM105.646 63.157C103.969 63.157 102.521 62.7992 101.302 62.0828C100.084 61.3566 99.1457 60.3811 98.4897 59.1564C97.8333 57.9215 97.5053 56.5413 97.5053 55.0155V54.3774C97.5053 52.6235 97.8386 51.0981 98.5053 49.8008C99.172 48.4932 100.084 47.4815 101.24 46.7655C102.406 46.049 103.724 45.6913 105.193 45.6913C106.818 45.6913 108.167 46.0442 109.24 46.7495C110.312 47.4451 111.115 48.4153 111.646 49.6609C112.177 50.8958 112.443 52.3277 112.443 53.9572V55.623H101.412C101.516 56.8991 101.958 57.9578 102.74 58.7982C103.521 59.6284 104.568 60.0437 105.88 60.0437C106.787 60.0437 107.588 59.8671 108.287 59.5146C108.984 59.1617 109.594 58.653 110.115 57.9888L112.146 60.0127C111.604 60.8115 110.802 61.5381 109.74 62.1917C108.677 62.8355 107.312 63.157 105.646 63.157ZM105.177 48.789C104.146 48.789 103.318 49.1521 102.693 49.8787C102.068 50.6049 101.667 51.591 101.49 52.8365H108.615V52.5407C108.594 51.8867 108.464 51.2744 108.224 50.7036C107.995 50.1329 107.63 49.671 107.13 49.3181C106.64 48.9652 105.99 48.789 105.177 48.789ZM119.224 62.8457H115.349V46.0026H119.036L119.146 47.9482C119.573 47.253 120.104 46.703 120.74 46.2983C121.385 45.8936 122.14 45.6913 123.005 45.6913C123.224 45.6913 123.469 45.7121 123.74 45.7533C124.01 45.7949 124.213 45.8418 124.349 45.8936L124.318 49.5519C124.078 49.5205 123.823 49.4948 123.552 49.474C123.292 49.4426 123.031 49.4271 122.771 49.4271C121.854 49.4271 121.104 49.6037 120.521 49.9566C119.937 50.3095 119.505 50.8072 119.224 51.451V62.8457ZM139.802 62.8457H126.036V60.355L134.552 49.1158H126.224V46.0026H139.474V48.3998L130.896 59.748H139.802V62.8457ZM152.943 46.0026H156.818V62.8457H153.161L153.068 61.1489C152.536 61.7821 151.88 62.2749 151.099 62.6278C150.318 62.9807 149.391 63.157 148.318 63.157C146.651 63.157 145.302 62.6695 144.271 61.6936C143.24 60.7181 142.724 59.1148 142.724 56.8836V46.0026H146.599V56.9146C146.599 58.0875 146.864 58.8969 147.396 59.3433C147.927 59.779 148.557 59.9968 149.287 59.9968C150.245 59.9968 151.016 59.8259 151.599 59.4832C152.193 59.1303 152.64 58.6583 152.943 58.0667V46.0026ZM160.63 41.5973C160.63 41.0057 160.823 40.5178 161.208 40.1339C161.594 39.7393 162.13 39.5423 162.818 39.5423C163.505 39.5423 164.047 39.7393 164.443 40.1339C164.839 40.5178 165.036 41.0057 165.036 41.5973C165.036 42.1782 164.839 42.6662 164.443 43.0602C164.047 43.4446 163.505 43.6363 162.818 43.6363C162.13 43.6363 161.594 43.4446 161.208 43.0602C160.823 42.6662 160.63 42.1782 160.63 41.5973ZM164.755 62.8457H160.88V46.0026H164.755V62.8457ZM172.724 62.8457H168.833V46.0026H172.49L172.615 47.8392C173.177 47.1649 173.864 46.6406 174.677 46.2673C175.5 45.883 176.448 45.6913 177.521 45.6913C178.563 45.6913 179.484 45.8989 180.287 46.3138C181.088 46.7292 181.708 47.388 182.146 48.2909C182.698 47.5023 183.406 46.8744 184.271 46.4073C185.146 45.9299 186.167 45.6913 187.333 45.6913C189.052 45.6913 190.401 46.1739 191.38 47.1387C192.37 48.104 192.864 49.718 192.864 51.9802V62.8457H188.974V51.9492C188.974 50.7142 188.703 49.8889 188.161 49.474C187.63 49.0587 186.912 48.8514 186.005 48.8514C185.161 48.8514 184.469 49.0742 183.927 49.5205C183.385 49.9668 183.005 50.5482 182.787 51.2642C182.787 51.3784 182.787 51.4975 182.787 51.6219V62.8457H178.912V51.9802C178.912 50.7869 178.64 49.9668 178.099 49.5205C177.568 49.0742 176.844 48.8514 175.927 48.8514C175.125 48.8514 174.464 49.0223 173.943 49.3651C173.422 49.6972 173.016 50.1537 172.724 50.7346V62.8457ZM196.677 60.4639C196.677 59.7271 196.927 59.1148 197.427 58.6273C197.927 58.1393 198.588 57.8953 199.412 57.8953C200.234 57.8953 200.891 58.1393 201.38 58.6273C201.88 59.1148 202.13 59.7271 202.13 60.4639C202.13 61.1906 201.88 61.7976 201.38 62.2851C200.891 62.7731 200.234 63.017 199.412 63.017C198.588 63.017 197.927 62.7731 197.427 62.2851C196.927 61.7976 196.677 61.1906 196.677 60.4639ZM210.677 62.8457H205.802V46.0026H210.38L210.536 47.9017C211.734 46.4281 213.339 45.6913 215.349 45.6913C216.412 45.6913 217.344 45.8989 218.146 46.3138C218.948 46.7185 219.573 47.3982 220.021 48.3533C220.469 49.2973 220.693 50.5792 220.693 52.198V62.8457H215.787V52.167C215.787 51.1601 215.568 50.4858 215.13 50.143C214.693 49.8008 214.068 49.6294 213.255 49.6294C212.651 49.6294 212.136 49.749 211.708 49.9876C211.292 50.2263 210.948 50.5584 210.677 50.9839V62.8457ZM229.052 62.8457H224.161V38.9352H229.052V62.8457Z" fill="white"/>
</svg>"""

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    padding: 0 1rem 4rem !important;
    max-width: 720px !important;
}}
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    color: #111827;
}}
.stApp {{ background: #ffffff; }}

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
    transition: color 0.2s;
}}
.vvz-header a.meer:hover {{ color: #fff; }}

.vvz-hero {{
    text-align: center;
    padding: 36px 0 24px;
}}
.vvz-hero h1 {{
    font-size: 34px;
    font-weight: 900;
    color: #111827;
    line-height: 1.2;
    margin-bottom: 12px;
}}
.vvz-hero .accent {{ color: {ACCENT}; }}
.vvz-hero p {{
    color: #6b7280;
    font-size: 15px;
    max-width: 440px;
    margin: 0 auto;
}}

.vvz-progress {{
    display: flex;
    align-items: flex-start;
    justify-content: center;
    margin-bottom: 1.5rem;
}}
.step-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.step-circle {{
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600;
    border: 2px solid #e2e8f0;
    color: #4b5563;
    background: transparent;
}}
.step-circle.done {{ background: {ACCENT}; border-color: {ACCENT}; color: #fff; }}
.step-circle.active {{ border-color: {ACCENT}; color: {ACCENT}; }}
.step-label {{ font-size: 12px; font-weight: 500; color: #6b7280; margin-top: 6px; }}
.step-label.hi {{ color: {ACCENT}; }}
.step-connector {{
    width: 80px; height: 2px; background: #e2e8f0;
    margin: 17px 8px 0; overflow: hidden; position: relative;
}}
.step-connector-fill {{
    position: absolute; top: 0; left: 0;
    height: 100%; background: {ACCENT};
}}

.calc-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
}}
.calc-sep {{ border: none; border-top: 1px solid #e2e8f0; margin: 0 0 20px; }}
.slider-row {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }}
.slider-lbl {{ font-size: 14px; font-weight: 500; color: #4b5563; }}
.slider-sub {{ font-size: 12px; color: #9ca3af; margin-top: 2px; }}
.slider-val {{ font-size: 19px; font-weight: 700; color: #111827; text-align: right; }}
.slider-minmax {{ display: flex; justify-content: space-between; font-size: 11px; color: #9ca3af; margin-top: 2px; margin-bottom: 6px; }}

.stSelectbox label {{ font-size: 14px !important; font-weight: 500 !important; color: #4b5563 !important; }}
.stNumberInput label {{ font-size: 14px !important; font-weight: 500 !important; color: #4b5563 !important; }}
.stNumberInput input {{
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}}
.stNumberInput input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT} !important;
}}
.premie-hint {{
    font-size: 12px;
    color: #9ca3af;
    margin-top: 4px;
    margin-bottom: 0;
}}

.savings-card {{
    background: #f8fafc;
    border: 1px solid rgba(11,52,157,0.2);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 12px;
    background-image: linear-gradient(135deg, rgba(11,52,157,0.04) 0%, transparent 60%);
}}
.savings-tag {{
    font-size: 11px; font-weight: 700; color: {ACCENT};
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;
}}
.savings-amount {{
    font-size: 52px; font-weight: 900; color: #111827;
    letter-spacing: -0.02em; line-height: 1.05; margin-bottom: 6px;
}}
.savings-note {{ font-size: 14px; color: #6b7280; }}
.aanvraag-card {{
    background: #f8fafc;
    border: 1px solid rgba(11,52,157,0.2);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 12px;
}}
.metric-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
.metric-card {{ background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 16px; }}
.metric-lbl {{
    font-size: 10px; font-weight: 600; color: #9ca3af;
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;
}}
.metric-val {{ font-size: 22px; font-weight: 700; color: #111827; }}
.metric-val.green {{ color: #16a34a; }}
.metric-sub {{ font-size: 11px; color: #9ca3af; margin-top: 2px; }}
.results-cta {{ text-align: center; font-size: 14px; color: #6b7280; margin-bottom: 20px; }}

.form-header {{ margin-bottom: 20px; }}
.form-header h2 {{ font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 4px; }}
.form-header p {{ font-size: 14px; color: #6b7280; }}

.stTextInput input {{
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}}
.stTextInput input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT} !important;
}}
.stTextInput label {{
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4b5563 !important;
}}

div[data-testid="stFormSubmitButton"] button, .stButton > button {{
    width: 100% !important;
    background-color: {ACCENT} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: background-color 0.2s !important;
}}
div[data-testid="stFormSubmitButton"] button:hover, .stButton > button:hover {{
    background-color: #092a7a !important;
}}

.success-card {{
    background: #f8fafc;
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 16px;
    padding: 36px 24px;
    text-align: center;
    margin-bottom: 12px;
}}
.success-icon {{
    width: 56px; height: 56px;
    background: rgba(34,197,94,0.1);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 14px;
}}
.success-card h2 {{ font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 6px; }}
.success-card p {{ font-size: 14px; color: #6b7280; max-width: 320px; margin: 0 auto 16px; }}
.success-badge {{
    display: inline-block;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 13px; font-weight: 500; color: #16a34a;
}}

.vvz-disclaimer {{
    font-size: 11px; color: #9ca3af; text-align: center; line-height: 1.6;
    border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 8px;
    font-style: italic;
}}
.vvz-footer {{
    border-top: 1px solid #e2e8f0;
    padding: 20px 0;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #9ca3af;
    margin-top: 8px;
}}
</style>
""", unsafe_allow_html=True)


# ── HTML helpers ───────────────────────────────────────────────────────────────
def render_progress(completed: int) -> str:
    steps = ["Verzuim", "Loonsom", "Premie"]
    check = """<svg width="16" height="16" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>"""
    html = '<div class="vvz-progress">'
    for i, label in enumerate(steps):
        done   = i < completed
        active = i == completed
        c_cls  = "step-circle done" if done else ("step-circle active" if active else "step-circle")
        l_cls  = "step-label hi" if (done or active) else "step-label"
        html += f"""
        <div class="step-wrap">
            <div class="{c_cls}">{check if done else i + 1}</div>
            <div class="{l_cls}">{label}</div>
        </div>"""
        if i < len(steps) - 1:
            fill = "100%" if done else "0%"
            html += f"""
        <div class="step-connector">
            <div class="step-connector-fill" style="width:{fill}"></div>
        </div>"""
    return html + "</div>"


def render_results(results: dict, verzuimklasse: str, wachtweken: int) -> str:
    rate      = results["rate"]
    onze      = results["onzePremie"]
    huidige   = results["huidigePremie"]
    besparing = results["besparing"]
    bes_pct   = results["besparingPct"]

    if huidige and besparing is not None:
        bes_display = max(0, besparing)
        pct_display = max(0.0, bes_pct) if bes_pct is not None else 0.0
        main = f"""
        <div class="savings-card">
            <div class="savings-tag">Geschatte jaarlijkse besparing</div>
            <div class="savings-amount">{format_currency(bes_display)}</div>
            <div class="savings-note">{pct_display:.0f}% minder dan uw huidige premie</div>
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-lbl">Uw huidige premie</div>
                <div class="metric-val">{format_currency(huidige)}</div>
                <div class="metric-sub">per jaar</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">Premie met ons</div>
                <div class="metric-val green">{format_currency(onze)}</div>
                <div class="metric-sub">{rate:.3f}% van loonsom</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">Wachttijd</div>
                <div class="metric-val">{wachtweken} wkn</div>
                <div class="metric-sub">Klasse {verzuimklasse}</div>
            </div>
        </div>"""
    else:
        main = f"""
        <div class="savings-card">
            <div class="savings-tag">Uw premie bij verzekerverzuim.nl</div>
            <div class="savings-amount">{format_currency(onze)}</div>
            <div class="savings-note">{rate:.3f}% van uw jaarloonsom · {wachtweken} weken wachttijd</div>
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-lbl">Premiepercentage</div>
                <div class="metric-val green">{rate:.3f}%</div>
                <div class="metric-sub">van jaarloonsom</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">Verzuimklasse</div>
                <div class="metric-val">{verzuimklasse}</div>
                <div class="metric-sub">gemiddeld 3 jaar</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">Wachttijd</div>
                <div class="metric-val">{wachtweken} wkn</div>
                <div class="metric-sub">eigen risico</div>
            </div>
        </div>"""

    return main + """<p class="results-cta">
        Mandaat Fysiotherapie 100%/100%/70%/70% · database van 6 verzekeraars
    </p>"""


def render_op_aanvraag() -> str:
    return """
    <div class="aanvraag-card">
        <div class="savings-tag">Maatwerk offerte</div>
        <div style="font-size:28px; font-weight:800; color:#111827; margin-bottom:8px;">
            Op aanvraag
        </div>
        <div class="savings-note">
            Bij een verzuimpercentage van 8% of hoger stellen wij een persoonlijke offerte op.
            Vul het formulier in — u ontvangt binnen 24 uur een berekening op maat.
        </div>
    </div>"""


def render_success(onze_premie: float | None) -> str:
    badge = f'<div class="success-badge">Uw premie met ons: {format_currency(onze_premie)} per jaar</div>' if onze_premie else '<div class="success-badge">Offerte op maat volgt binnen 24 uur</div>'
    return f"""
    <div class="success-card">
        <div class="success-icon">
            <svg width="28" height="28" fill="none" stroke="#16a34a" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
        </div>
        <h2>Aanvraag ontvangen!</h2>
        <p>U ontvangt binnen 24 uur uw persoonlijke verzuimrapport met offertes in uw inbox.</p>
        {badge}
    </div>"""


# ── Layout ─────────────────────────────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="vvz-header">
    <a href="https://verzekerverzuim.nl">{LOGO_SVG}</a>
    <a class="meer" href="https://verzekerverzuim.nl">Meer informatie →</a>
</div>""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="vvz-hero">
    <h1>Hoeveel kun jij besparen<br><span class="accent">als fysiotherapeut?</span></h1>
    <p>Beantwoord 3 vragen. Wij berekenen je premie op basis van
    jouw verzuimprofiel — direct en zonder verplichtingen.</p>
</div>""", unsafe_allow_html=True)

# Read session state for progress
verzuim_key  = st.session_state.get("verzuim_select",  "Selecteer...")
wachttijd_key = st.session_state.get("wachttijd_select", None)
premie_key   = st.session_state.get("premie_input", 0) or 0

steps_done = (
    (1 if (verzuim_key != "Selecteer..." and wachttijd_key is not None) else 0)
    + (1 if st.session_state.loonsom_touched else 0)
    + (1 if premie_key > 0 else 0)
)

st.markdown(render_progress(steps_done), unsafe_allow_html=True)

# ── Calculator card ────────────────────────────────────────────────────────────
st.markdown('<div class="calc-card">', unsafe_allow_html=True)

# Verzuim inputs (two columns)
col_l, col_r = st.columns(2)
with col_l:
    verzuimklasse = st.selectbox(
        "Gemiddeld verzuim (afgelopen 3 jaar)",
        ["Selecteer..."] + VERZUIM_KLASSEN,
        key="verzuim_select",
    )
with col_r:
    wachtweken = st.selectbox(
        "Wachttijd huidige polis",
        WACHTWEKEN_OPTIES,
        format_func=lambda x: f"{x} weken",
        key="wachttijd_select",
        index=None,
        placeholder="Selecteer...",
    )

st.markdown('<hr class="calc-sep">', unsafe_allow_html=True)

# Loonsom slider
loonsom_val = st.session_state.get("loonsom_slider", 800_000)
st.markdown(f"""
<div class="slider-row">
    <div>
        <div class="slider-lbl">Totale bruto jaarloonsom</div>
        <div class="slider-sub">Inclusief alle medewerkers</div>
    </div>
    <div class="slider-val">{format_currency(loonsom_val)}</div>
</div>""", unsafe_allow_html=True)
loonsom = st.slider(
    "loonsom", 100_000, 3_000_000, 800_000, 50_000,
    key="loonsom_slider", on_change=mark_loonsom, label_visibility="collapsed",
)
st.markdown(f"""<div class="slider-minmax">
    <span>{format_currency(100_000)}</span>
    <span>{format_currency(3_000_000)}</span>
</div>""", unsafe_allow_html=True)

st.markdown('<hr class="calc-sep">', unsafe_allow_html=True)

# Huidige premie (optional)
huidige_premie = st.number_input(
    "Uw huidige jaarpremie (€) — optioneel",
    min_value=0,
    max_value=500_000,
    step=500,
    value=None,
    placeholder="bijv. 12500",
    key="premie_input",
)
huidige_premie = huidige_premie or 0
st.markdown(
    '<p class="premie-hint">Staat op uw factuur of polisblad · vul in voor een besparingesschatting</p>',
    unsafe_allow_html=True,
)

verzuim_ok = verzuimklasse != "Selecteer..." and wachtweken is not None
if not verzuim_ok:
    st.markdown(
        '<p style="text-align:center;font-size:12px;color:#9ca3af;margin-top:8px">'
        'Selecteer uw verzuimklasse en wachttijd om uw premie te berekenen</p>',
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ── Results & lead form ────────────────────────────────────────────────────────
if verzuim_ok and not st.session_state.submitted:
    results = calculate_fysio(loonsom, verzuimklasse, wachtweken, huidige_premie)

    if results is None:
        st.markdown(render_op_aanvraag(), unsafe_allow_html=True)
        onze_premie_for_success = None
    else:
        st.markdown(render_results(results, verzuimklasse, wachtweken), unsafe_allow_html=True)
        onze_premie_for_success = results["onzePremie"]

    # Lead form (always shown)
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-header">
        <h2>Vraag gratis offertes aan bij 6 verzekeraars</h2>
        <p>Binnen 24 uur de beste offertes voor fysiotherapeuten in uw inbox — zonder verdere verplichtingen.</p>
    </div>""", unsafe_allow_html=True)

    with st.form("lead_form"):
        c1, c2 = st.columns(2)
        with c1:
            naam    = st.text_input("Naam *",         placeholder="Jan de Vries")
        with c2:
            bedrijf = st.text_input("Praktijknaam *", placeholder="Fysiotherapie Centrum")
        email    = st.text_input("E-mailadres *",    placeholder="jan@mijnpraktijk.nl")
        telefoon = st.text_input("Telefoonnummer",   placeholder="06 12 34 56 78")
        submitted = st.form_submit_button("Ontvang mijn gratis offertes →")
        if submitted:
            st.session_state.submitted = True
            st.session_state._onze_premie = onze_premie_for_success
            st.rerun()
        st.markdown(
            '<p style="text-align:center;font-size:12px;color:#9ca3af;margin-top:4px">'
            'Geen spam. U ontvangt het verzuimrapport + offertes per e-mail.</p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.submitted:
    onze_premie_stored = st.session_state.get("_onze_premie", None)
    st.markdown(render_success(onze_premie_stored), unsafe_allow_html=True)

# ── Disclaimer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vvz-disclaimer">
    Deze berekening is gebaseerd op het mandaat Fysiotherapie 100%/100%/70%/70% en uw opgegeven verzuimprofiel.
    De werkelijke premie wordt vastgesteld na een officiële offerteaanvraag.
    Aan deze berekening kunnen geen rechten worden ontleend.
</div>""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
from datetime import date
year = date.today().year
st.markdown(f"""
<div class="vvz-footer">
    <span>© {year} du Gardijn Verzekeringen · verzekerverzuim.nl</span>
    <span>AVG-proof · geen cookies zonder toestemming</span>
</div>""", unsafe_allow_html=True)
