# py -3.13 -m streamlit run "Quiz Generator/main.py"

import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()

api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY")

client = genai.Client(api_key=api_key)

st.set_page_config(layout="centered")

# ── Global styles & animations ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Deep space background ── */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > div {
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%,  rgba(99,102,241,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%,  rgba(236,72,153,0.20) 0%, transparent 55%),
        radial-gradient(ellipse 70% 70% at 50% 40%,  rgba(16,185,129,0.08) 0%, transparent 50%),
        linear-gradient(160deg, #07080f 0%, #0d0f1e 40%, #0b0e1b 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}

[data-testid="stMain"], .main, section.main, [data-testid="stBottom"] {
    background: transparent !important;
}

/* ── Font globals ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #e2e8f0;
}

/* ── Star field ── */
.starfield {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}
.star {
    position: absolute;
    border-radius: 50%;
    background: #fff;
    animation: twinkle var(--dur, 4s) var(--delay, 0s) infinite ease-in-out alternate;
}
@keyframes twinkle {
    from { opacity: var(--lo, 0.1); transform: scale(1); }
    to   { opacity: var(--hi, 0.7); transform: scale(1.4); }
}

/* ── Floating orbs ── */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    z-index: 0;
    animation: drift 18s ease-in-out infinite alternate;
}
.orb-1 { width: 420px; height: 420px; top: -120px; left: -100px;  background: rgba(99,102,241,0.18); animation-duration: 20s; }
.orb-2 { width: 300px; height: 300px; bottom: 60px; right: -80px; background: rgba(236,72,153,0.16); animation-duration: 14s; animation-direction: alternate-reverse; }
.orb-3 { width: 250px; height: 250px; top: 40%;   left: 55%;      background: rgba(16,185,129,0.10); animation-duration: 17s; }
@keyframes drift {
    from { transform: translate(0px, 0px) scale(1);   }
    to   { transform: translate(30px, 20px) scale(1.08); }
}

/* ── Bouncing question mark ── */
.bounce-qmark {
    position: fixed;
    bottom: 28px;
    right: 28px;
    font-size: 3rem;
    animation: bounce 1.4s infinite cubic-bezier(.36,.07,.19,.97);
    z-index: 999;
    filter: drop-shadow(0 0 14px rgba(99,102,241,0.9));
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-16px); }
}

/* ── Question heading ── */
h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #f0f4ff !important;
    letter-spacing: 0.01em;
    line-height: 1.55;
    text-shadow: 0 2px 20px rgba(99,102,241,0.4);
}

/* ── Option cards ── */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 6px;
}
div[data-testid="stRadio"] > div > label {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 13px 20px;
    width: 100%;
    border: 1.5px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(6px);
    cursor: pointer;
    transition: all 0.22s ease;
    font-size: 0.93rem;
    color: #c4cde0;
    white-space: normal;
    word-break: break-word;
    line-height: 1.55;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: rgba(99,102,241,0.6);
    background: rgba(99,102,241,0.10);
    color: #ffffff;
    transform: translateX(3px);
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    border-color: rgba(99,102,241,0.85);
    background: rgba(99,102,241,0.18);
    color: #ffffff;
    box-shadow: 0 0 18px rgba(99,102,241,0.25);
}

/* ── Nav number buttons ── */
div[data-testid="stButton"][data-key^="q_"] > button {
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.10) !important;
    color: #a0aec0 !important;
    transition: all 0.18s ease !important;
}
div[data-testid="stButton"][data-key^="q_"] > button:hover {
    background: rgba(99,102,241,0.25) !important;
    border-color: rgba(99,102,241,0.6) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.3) !important;
}

/* ── Submit button (per question) ── */
div[data-testid="stButton"][data-key^="S"] > button {
    width: auto !important;
    height: auto !important;
    padding: 0.5rem 2rem !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    font-family: 'Syne', sans-serif !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: #ffffff !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.4) !important;
}
div[data-testid="stButton"][data-key^="S"] > button:hover {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.55) !important;
}

/* ── Final Submit button ── */
div[data-testid="stButton"][data-key="Final_submit"] > button {
    width: 100% !important;
    padding: 0.7rem 2rem !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border: none !important;
    color: #ffffff !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 6px 24px rgba(16,185,129,0.4) !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stButton"][data-key="Final_submit"] > button:hover {
    background: linear-gradient(135deg, #059669, #047857) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(16,185,129,0.55) !important;
}

/* ── Topic submit button ── */
div[data-testid="stButton"][data-key="topic_submit"] > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.8rem !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"][data-key="topic_submit"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.55) !important;
}

/* ── Text input ── */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(99,102,241,0.35) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,102,241,0.8) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label {
    color: #a0aec0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em;
}

/* ── Question container card ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.07) !important;
}

/* ── Success / Error alerts ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.7); }
</style>

<!-- Star field + orbs -->
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>

<div class="starfield" aria-hidden="true" id="starfield"></div>

<div class="bounce-qmark">🔮</div>

<script>
(function() {
  const sf = document.getElementById('starfield');
  if (!sf) return;
  for (let i = 0; i < 80; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 2.2 + 0.6;
    s.style.cssText = [
      `width:${size}px`, `height:${size}px`,
      `top:${Math.random()*100}%`, `left:${Math.random()*100}%`,
      `--lo:${(Math.random()*0.15+0.05).toFixed(2)}`,
      `--hi:${(Math.random()*0.5+0.3).toFixed(2)}`,
      `--dur:${(Math.random()*4+2).toFixed(1)}s`,
      `--delay:${(Math.random()*5).toFixed(1)}s`
    ].join(';');
    sf.appendChild(s);
  }
})();
</script>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

if "submitted_answers" not in st.session_state:
    st.session_state.submitted_answers = {}

if "results" not in st.session_state:
    st.session_state.results = {}

if "topic_submitted" not in st.session_state:
    st.session_state.topic_submitted = False

if "topic" not in st.session_state:
    st.session_state.topic = None

# ── Topic input screen ────────────────────────────────────────────────────────
if not st.session_state.topic_submitted:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 2rem;">
        <h1 style="font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800;
                   background: linear-gradient(135deg, #a5b4fc, #c084fc, #f9a8d4);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text; letter-spacing:-0.02em; margin-bottom:0.5rem;">
            QuizVerse
        </h1>
        <p style="color:rgba(160,174,192,0.8); font-size:1rem; font-family:'DM Sans',sans-serif;
                  letter-spacing:0.05em; text-transform:uppercase; margin-bottom:2.5rem;">
            ✦ Test your knowledge ✦
        </p>
    </div>
    """, unsafe_allow_html=True)

    topic_input = st.text_input(label="Enter Topic Name of Quiz", key="topic_input")

    if st.button(label="Generate Quiz →", key="topic_submit"):
        if topic_input.strip() != "":
            st.session_state.topic = topic_input.strip()
            st.session_state.topic_submitted = True
            st.rerun()
        else:
            st.warning("Please enter a topic first!")
    st.stop()

# ── Load questions ────────────────────────────────────────────────────────────
if "q_bank" not in st.session_state:
    st.session_state.q_bank = None

if st.session_state.q_bank is None:
    topic = st.session_state.topic
    print(topic)

    prompt = f"""Give me 10 quiz qs in {topic}. question must be in good quiz format no other writing must be there and 
    qs must be in good layout qs must start with '**Q1' '**Q2' like this and after **Q(no) must be an enter then qs start 
    and in option there must not be 'A)' 'B)' like this in between each option there will only an enter and at last there 
    will be an enter after enter there will be answer(answer must be after an enter after options) like this '0 or 1 or 2 
    or 3' according to which option true that's position-1 """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    response = response.text
    questions = response.split("**Q")

    print(response)
    print(questions)

    st.session_state.q_bank = []
    q_bank = st.session_state.q_bank

    for i in range(1, 11):
        q_list = questions[i].split("\n")
        q_list = [line.strip() for line in q_list if line.strip()]
        q_dict = {}
        q_dict["Question"] = q_list[1]
        q_dict["Options"] = q_list[2:6]

        # Robust answer parsing
        raw_answer = q_list[6].strip()
        # Extract just the first digit found
        import re
        match = re.search(r'[0-3]', raw_answer)
        q_dict["answer"] = int(match.group()) if match else 0
        q_bank.append(q_dict)

    print(q_bank)

# ── Quiz UI ───────────────────────────────────────────────────────────────────
q_bank = st.session_state.q_bank

def change_tab(i):
    st.session_state.tab = i

if "tab" not in st.session_state:
    st.session_state.tab = 1

idx = st.session_state.tab
q   = q_bank[idx - 1]

# Topic + progress header
answered = len(st.session_state.results)
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1rem; padding: 0 0.25rem;">
    <span style="font-family:'Syne',sans-serif; font-size:1.35rem; font-weight:700;
                 background:linear-gradient(135deg,#a5b4fc,#c084fc);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">
        {st.session_state.topic}
    </span>
    <span style="font-size:0.82rem; color:rgba(160,174,192,0.7);
                 font-family:'DM Sans',sans-serif; letter-spacing:0.04em;">
        {answered}/10 answered
    </span>
</div>
""", unsafe_allow_html=True)

# Progress bar
prog_pct = answered / 10 * 100
st.markdown(f"""
<div style="width:100%; height:4px; background:rgba(255,255,255,0.06);
            border-radius:2px; margin-bottom:1.4rem; overflow:hidden;">
    <div style="width:{prog_pct}%; height:100%;
                background:linear-gradient(90deg,#6366f1,#a78bfa,#ec4899);
                border-radius:2px; transition:width 0.4s ease;">
    </div>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    # Question number pill + question
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
        <span style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
                     color:#fff; font-family:'Syne',sans-serif; font-weight:700;
                     font-size:0.78rem; padding:4px 12px; border-radius:20px;
                     letter-spacing:0.06em; white-space:nowrap;">
            Q {idx} / 10
        </span>
    </div>
    <h3>{q['Question']}</h3>
    """, unsafe_allow_html=True)

    answer = st.radio("", q["Options"], label_visibility="collapsed", key=f"Q{idx}")

    if st.button("Submit Answer", key=f"S{idx}"):
        options = q["Options"]
        st.session_state.submitted_answers[idx] = answer
        st.session_state.results[idx] = (answer == options[q["answer"]])

    if idx in st.session_state.results:
        options = q["Options"]
        if st.session_state.results[idx]:
            st.success("✅ Correct!")
        else:
            chosen = st.session_state.submitted_answers[idx]
            st.error(f"❌ Wrong! You chose **{chosen}**. Correct answer is **{options[q['answer']]}**.")

# ── Nav buttons ───────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
btn_cols = st.columns(10)
for i in range(10):
    with btn_cols[i]:
        label = str(i + 1)
        # add a checkmark indicator if answered
        if (i + 1) in st.session_state.results:
            label = "✓"
        st.button(label, key=f"q_{i+1}", on_click=change_tab, args=(i + 1,))

# ── Final submit ──────────────────────────────────────────────────────────────
if len(st.session_state.results) == 10:
    if st.button(label="🚀 Submit Quiz", key="Final_submit"):
        st.session_state.quiz_done = True

# ── Results screen ────────────────────────────────────────────────────────────
if st.session_state.get("quiz_done"):
    score = sum(st.session_state.results.values())
    total = 10
    pct   = int(score / total * 100)

    if pct == 100:  emoji, color, grad, msg = "🏆", "#FFD700", "linear-gradient(135deg,#f59e0b,#fbbf24)", "Perfect Score!"
    elif pct >= 70: emoji, color, grad, msg = "🎉", "#10b981", "linear-gradient(135deg,#10b981,#34d399)", "Great Job!"
    elif pct >= 40: emoji, color, grad, msg = "👍", "#f97316", "linear-gradient(135deg,#f97316,#fb923c)", "Good Effort!"
    else:           emoji, color, grad, msg = "📚", "#f87171", "linear-gradient(135deg,#ef4444,#f87171)", "Keep Practicing!"

    radius = 80
    circ   = 2 * 3.14159 * radius
    filled = circ * (score / total)

    svg = (
        f'<svg width="220" height="220" viewBox="0 0 220 220">'
        f'<circle cx="110" cy="110" r="{radius}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="16"/>'
        f'<circle cx="110" cy="110" r="{radius}" fill="none" stroke="{color}" stroke-width="16" '
        f'stroke-linecap="round" stroke-dasharray="{filled:.1f} {circ:.1f}" transform="rotate(-90 110 110)"'
        f' style="filter:drop-shadow(0 0 12px {color});"/>'
        f'<text x="110" y="102" text-anchor="middle" font-size="44" font-weight="800" fill="white" font-family="Syne,sans-serif">{score}</text>'
        f'<text x="110" y="130" text-anchor="middle" font-size="15" fill="rgba(255,255,255,0.35)" font-family="DM Sans,sans-serif">out of {total}</text>'
        f'</svg>'
    )

    html = (
        f'<div style="text-align:center; padding:3rem 0 2rem;">'
        f'<div style="display:inline-block; background:{grad}; -webkit-background-clip:text;'
        f'-webkit-text-fill-color:transparent; background-clip:text;">'
        f'<h2 style="font-family:Syne,sans-serif; font-size:2rem; font-weight:800;'
        f'letter-spacing:-0.01em; margin-bottom:1.5rem;">{emoji} {msg}</h2></div>'
        f'{svg}'
        f'<p style="color:rgba(255,255,255,0.35); font-size:0.9rem; margin-top:1.2rem;'
        f'font-family:DM Sans,sans-serif; letter-spacing:0.05em; text-transform:uppercase;">'
        f'{pct}% correct</p>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)