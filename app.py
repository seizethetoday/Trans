import streamlit as st

from translator import TranslationError, translate

MAX_CHARS = 5000
WARN_CHARS = int(MAX_CHARS * 0.9)
LANGS = {
    "English": ("English", "English"),
    "日本語": ("日本語", "Japanese"),
    "Tiếng Việt": ("Tiếng Việt", "Vietnamese"),
}

st.set_page_config(page_title="다국어 번역기", page_icon="🌐", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap');
    html, body, [class*="css"], .stApp, textarea, button {
        font-family: 'Noto Sans KR', 'Noto Sans JP', 'Segoe UI', sans-serif;
    }
    .block-container { max-width: 760px; padding-top: 2.5rem; padding-bottom: 3rem; }
    .stMarkdown p.app-title { font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; line-height: 1.3; }
    .stMarkdown p.app-sub { opacity: .65; margin: .25rem 0 1.5rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 14px; }
    .counter { text-align: right; font-size: .8rem; opacity: .6; margin-top: -.5rem; }
    .counter.warn { color: #d97706; opacity: 1; font-weight: 600; }
    .counter.over { color: #dc2626; opacity: 1; font-weight: 700; }
    .stButton > button {
        border-radius: 10px; font-weight: 600; padding: .6rem 0; width: 100%;
        border: 1px solid rgba(128,128,128,.35);
    }
    .stButton > button:hover { border-color: #4f46e5; color: #4f46e5; }
    .result-lang { font-weight: 700; margin-bottom: .4rem; }
    @media (max-width: 640px) {
        .stMarkdown p.app-title { font-size: 1.6rem; }
        div[data-testid="stHorizontalBlock"] { flex-direction: column; gap: .5rem; }
        div[data-testid="stHorizontalBlock"] > div { width: 100% !important; flex: 1 1 100% !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="app-title">🌐 다국어 번역기</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-sub">글을 입력하고 번역할 언어 버튼을 누르세요.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    text = st.text_area(
        "번역할 글", height=180, key="source", label_visibility="collapsed",
        placeholder="여기에 번역할 글을 입력하세요",
    )
    length = len(text)
    over = length > MAX_CHARS
    cls = "over" if over else "warn" if length >= WARN_CHARS else ""
    st.markdown(
        f'<div class="counter {cls}">{length:,} / {MAX_CHARS:,}자</div>',
        unsafe_allow_html=True,
    )
    if over:
        st.error(f"입력은 {MAX_CHARS:,}자까지 가능합니다. {length - MAX_CHARS:,}자를 줄여 주세요.")

    cols = st.columns(3)
    clicked = None
    for col, label in zip(cols, LANGS):
        if col.button(label, use_container_width=True):
            clicked = label

if clicked:
    if not text.strip():
        st.session_state.pop("result", None)
        st.warning("번역할 내용을 입력해 주세요.")
    elif over:
        st.session_state.pop("result", None)
    else:
        name, api_lang = LANGS[clicked]
        try:
            with st.spinner(f"{name}(으)로 번역 중..."):
                result = translate(text, api_lang)
            st.session_state["result"] = {"lang": name, "text": result}
        except TranslationError as e:
            st.session_state.pop("result", None)
            st.error(str(e))

if "result" in st.session_state:
    res = st.session_state["result"]
    with st.container(border=True):
        st.markdown(
            f'<div class="result-lang">{res["lang"]} 번역 결과</div>',
            unsafe_allow_html=True,
        )
        st.code(res["text"], language=None, wrap_lines=True)
