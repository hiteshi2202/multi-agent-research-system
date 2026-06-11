import streamlit as st
import sys
import os
import time
from io import StringIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Background */
  .stApp {
    background: #0d0f14;
    color: #e8eaf0;
  }

  /* Hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
  }
  .hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: #5b6af0;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }
  .hero-title {
    font-size: 2.8rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, #e8eaf0 30%, #5b6af0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.6rem;
  }
  .hero-sub {
    font-size: 1rem;
    color: #7a7f9a;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
  }

  /* ── Input area ── */
  .stTextInput > div > div > input {
    background: #161a26 !important;
    border: 1px solid #252a3d !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s;
  }
  .stTextInput > div > div > input:focus {
    border-color: #5b6af0 !important;
    box-shadow: 0 0 0 3px rgba(91,106,240,0.15) !important;
  }

  /* ── Run button ── */
  .stButton > button {
    background: #5b6af0 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.01em;
    transition: background 0.2s, transform 0.1s;
  }
  .stButton > button:hover {
    background: #4757e8 !important;
    transform: translateY(-1px);
  }
  .stButton > button:active {
    transform: translateY(0);
  }

  /* ── Pipeline step cards ── */
  .step-card {
    background: #161a26;
    border: 1px solid #252a3d;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .step-card.active {
    border-color: #5b6af0;
    box-shadow: 0 0 0 1px #5b6af0, 0 4px 24px rgba(91,106,240,0.12);
  }
  .step-card.done {
    border-color: #2a9d5c;
    opacity: 0.85;
  }
  .step-icon {
    font-size: 1.4rem;
    flex-shrink: 0;
    width: 2rem;
    text-align: center;
  }
  .step-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #c8ccde;
    flex: 1;
  }
  .step-status {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7a7f9a;
  }
  .step-status.running { color: #5b6af0; }
  .step-status.done    { color: #2a9d5c; }

  /* ── Output panels ── */
  .panel-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5b6af0;
    margin-bottom: 0.5rem;
  }
  .output-box {
    background: #161a26;
    border: 1px solid #252a3d;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    color: #b0b5cc;
    font-size: 0.88rem;
    line-height: 1.75;
    max-height: 340px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Mono', monospace;
  }

  /* ── Final report ── */
  .report-box {
    background: #161a26;
    border: 1px solid #2a9d5c44;
    border-radius: 12px;
    padding: 2rem 2.2rem;
    color: #dde0ec;
    font-size: 0.96rem;
    line-height: 1.85;
  }
  .report-box h1, .report-box h2, .report-box h3 {
    color: #e8eaf0;
    margin-top: 1.4rem;
  }

  /* ── Divider ── */
  .divider {
    border: none;
    border-top: 1px solid #1e2235;
    margin: 2rem 0;
  }

  /* ── Spinner override ── */
  .stSpinner > div { border-top-color: #5b6af0 !important; }

  /* scrollbar */
  .output-box::-webkit-scrollbar { width: 4px; }
  .output-box::-webkit-scrollbar-track { background: transparent; }
  .output-box::-webkit-scrollbar-thumb { background: #252a3d; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Multi-Agent Research System</div>
  <div class="hero-title">Deep Research,<br>On Demand</div>
  <div class="hero-sub">Enter any topic. Three specialized agents search, scrape, and synthesize a structured report in minutes.</div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1], gap="small")
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g. Advances in quantum error correction 2024",
        label_visibility="collapsed",
    )
with col_btn:
    run = st.button("Run Research")


# ── Pipeline Steps Helper ─────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",   "Finding recent, reliable sources"),
    ("📄", "Reader Agent",   "Scraping top URLs for deep content"),
    ("✍️",  "Writer Chain",  "Drafting the research report"),
]

def render_pipeline(current: int):
    """Render step cards. current=-1 idle, 0-2 active step, 3 all done."""
    html = ""
    for i, (icon, label, desc) in enumerate(STEPS):
        if current == -1:
            css, status = "step-card", "waiting"
        elif i < current:
            css, status = "step-card done", "done ✓"
        elif i == current:
            css, status = "step-card active", "running…"
        else:
            css, status = "step-card", "waiting"

        status_cls = "done" if "done" in status else ("running" if "running" in status else "")
        html += f"""
        <div class="{css}">
          <div class="step-icon">{icon}</div>
          <div>
            <div class="step-label">{label}</div>
            <div style="font-size:0.78rem;color:#55596e;">{desc}</div>
          </div>
          <div class="step-status {status_cls}">{status}</div>
        </div>"""
    return html


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("ran", "search_results", "scraped_content", "report", "error"):
    if key not in st.session_state:
        st.session_state[key] = None


# ── Run Pipeline ──────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        left, right = st.columns([1, 2], gap="large")

        with left:
            st.markdown('<div class="panel-header">Pipeline</div>', unsafe_allow_html=True)
            pipeline_placeholder = st.empty()

        with right:
            st.markdown('<div class="panel-header">Live Output</div>', unsafe_allow_html=True)
            output_placeholder = st.empty()

        # Step 0 – import pipeline (may take a moment for model init)
        pipeline_placeholder.markdown(render_pipeline(0), unsafe_allow_html=True)

        try:
            # We import here so Streamlit doesn't fail on load if deps missing
            from agents import build_reader_agent, build_search_agent, writer_chain

            # ── Step 1: Search Agent ──────────────────────────────────────
            pipeline_placeholder.markdown(render_pipeline(0), unsafe_allow_html=True)
            output_placeholder.markdown(
                '<div class="output-box">⏳ Search agent is querying the web…</div>',
                unsafe_allow_html=True,
            )

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [
                    ("user", f"Find recent, reliable and detailed information about: {topic}")
                ]
            })
            search_results = search_result["messages"][-1].content
            st.session_state["search_results"] = search_results

            output_placeholder.markdown(
                f'<div class="output-box">{search_results[:1200]}{"…" if len(search_results)>1200 else ""}</div>',
                unsafe_allow_html=True,
            )

            # ── Step 2: Reader Agent ──────────────────────────────────────
            pipeline_placeholder.markdown(render_pipeline(1), unsafe_allow_html=True)
            output_placeholder.markdown(
                '<div class="output-box">⏳ Reader agent is scraping top resource…</div>',
                unsafe_allow_html=True,
            )

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{search_results[:800]}"
                )]
            })
            scraped_content = reader_result["messages"][-1].content
            st.session_state["scraped_content"] = scraped_content

            output_placeholder.markdown(
                f'<div class="output-box">{scraped_content[:1200]}{"…" if len(scraped_content)>1200 else ""}</div>',
                unsafe_allow_html=True,
            )

            # ── Step 3: Writer Chain ──────────────────────────────────────
            pipeline_placeholder.markdown(render_pipeline(2), unsafe_allow_html=True)
            output_placeholder.markdown(
                '<div class="output-box">⏳ Writer is composing the report…</div>',
                unsafe_allow_html=True,
            )

            research_combined = (
                f"SEARCH RESULTS:\n{search_results}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
            )
            report = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            st.session_state["report"] = report

            # All done
            pipeline_placeholder.markdown(render_pipeline(3), unsafe_allow_html=True)
            output_placeholder.markdown(
                '<div class="output-box" style="color:#2a9d5c;">✅ Report ready — see below.</div>',
                unsafe_allow_html=True,
            )
            st.session_state["ran"] = topic

        except ImportError as e:
            st.error(f"Could not import pipeline modules: {e}\n\nMake sure `agents.py` is in the same directory and dependencies are installed.")
            st.session_state["error"] = str(e)
        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.session_state["error"] = str(e)


# ── Render Results (persisted in session) ─────────────────────────────────────
if st.session_state.get("report"):
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">Final Report</div>', unsafe_allow_html=True)

    # Download button
    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button(
            label="⬇ Download .txt",
            data=st.session_state["report"],
            file_name=f"report_{st.session_state['ran'][:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    st.markdown(
        f'<div class="report-box">{st.session_state["report"]}</div>',
        unsafe_allow_html=True,
    )

    # Expanders for raw intermediate outputs
    with st.expander("Search results (raw)"):
        st.code(st.session_state.get("search_results", ""), language=None)
    with st.expander("Scraped content (raw)"):
        st.code(st.session_state.get("scraped_content", ""), language=None)

elif not run:
    # Idle state – show empty pipeline
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    left, _ = st.columns([1, 2], gap="large")
    with left:
        st.markdown('<div class="panel-header">Pipeline</div>', unsafe_allow_html=True)
        st.markdown(render_pipeline(-1), unsafe_allow_html=True)