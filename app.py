import streamlit as st
from crewai import Agent, Task, Crew, LLM, Process
import os
from dotenv import load_dotenv

load_dotenv()

## ─── Page Config ───
st.set_page_config(
    page_title="Web Dev Agent",
    page_icon="🤖",
    layout="wide"
)

## ─── Custom Styling ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }

    .main-title {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #a0a0b8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .agent-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(10px);
    }

    .agent-card h4 {
        margin: 0 0 0.3rem 0;
        color: #e0e0ff;
    }

    .agent-card p {
        margin: 0;
        color: #8888aa;
        font-size: 0.9rem;
    }

    .stTextArea textarea {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: #e0e0ff !important;
        font-size: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.25) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        color: #a0a0b8;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(102,126,234,0.2) !important;
        color: #667eea !important;
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

## ─── Header ───
st.markdown('<h1 class="main-title">🤖 Web Dev Multi-Agent System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Describe your website idea and let AI agents build it for you</p>', unsafe_allow_html=True)

## ─── Agent Info Cards ───
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>📋 Requirement Agent</h4>
        <p>Analyzes your input and creates a detailed project specification</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>🎨 UI/UX Agent</h4>
        <p>Gives you working UI/UX code for the website</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>💻 Frontend Agent</h4>
        <p>Writes the complete HTML, CSS & JavaScript code</p>
    </div>
    """, unsafe_allow_html=True)

## ─── LLM Setup ───
llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    max_tokens=4000,
    timeout=120
)

## ─── User Input ───
st.markdown("---")
user_requirement = st.text_area(
    "📝 Describe the website you want to build:",
    placeholder="e.g., Build me a modern portfolio website with a dark theme, a hero section, an about me page, a project showcase with cards, and a contact form...",
    height=150
)

## ─── Run Button ───
if st.button("🚀 Generate Website", type="primary", use_container_width=True):
    if not user_requirement.strip():
        st.warning("⚠️ Please enter your website requirements first!")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error("❌ GEMINI_API_KEY not found in .env file. Please add it.")
    else:
        ## ─── Create Agents ───
        with st.status("🔄 Agents are working on your website...", expanded=True) as status:

            st.write("📋 **Requirement Agent** is analyzing your requirements...")
            requirement_agent = Agent(
                role="you are a requirment agent",
                goal="that will gather the information for the website project",
                backstory="you are an expert in requirement analysis and will gather information for the website project",
                llm=llm,
                verbose=True
            )
            requirement_agent_task = Task(
                description=f"Gather the key requirements for the following website project. Keep your response concise and under 500 words: {user_requirement}",
                agent=requirement_agent,
                expected_output="A concise requirements summary for the website project.",
                output_file="requirement.html"
            )

            st.write("🎨 **UI/UX Agent** is writing the UI/UX code...")
            ui_ux_agent = Agent(
                role="you are a ui/ux agent",
                goal="give concise working HTML and CSS code for the ui/ux of the website",
                backstory="you are an expert in ui/ux development and will give me working code for the ui/ux of the website. Keep code minimal and clean.",
                llm=llm
            )
            ui_ux_agent_task = Task(
                description=f"Write a single concise HTML file with inline CSS for the UI/UX layout of this website. Keep the code minimal but functional: {user_requirement}",
                agent=ui_ux_agent,
                expected_output="A single concise HTML file with inline CSS for the website UI/UX.",
                output_file="ui_ux.html"
            )

            st.write("💻 **Frontend Agent** is writing the complete code...")
            frontend_agent = Agent(
                role="you are a front end agent",
                goal="give me a complete single-file HTML website with inline CSS and JavaScript",
                backstory="you are an expert frontend developer. You write clean, concise, single-file HTML websites with inline CSS and JS.",
                llm=llm
            )
            frontend_agent_task = Task(
                description=f"Create a single complete HTML file with inline CSS and JavaScript for this website. Keep the code clean and concise: {user_requirement}",
                agent=frontend_agent,
                expected_output="A single complete HTML file with inline CSS and JavaScript.",
                output_file="frontend.html"
            )

            ## ─── Run Crew ───
            crew = Crew(
                agents=[requirement_agent, ui_ux_agent, frontend_agent],
                tasks=[requirement_agent_task, ui_ux_agent_task, frontend_agent_task],
                verbose=True
            )

            try:
                result = crew.kickoff()
                status.update(label="✅ All agents have finished!", state="complete")
            except Exception as e:
                status.update(label="❌ An error occurred", state="error")
                st.error(f"Error: {e}")
                st.stop()

        ## ─── Display Results ───
        st.success("🎉 Website generation complete!")

        tab1, tab2, tab3, tab4 = st.tabs(["📋 Requirements", "🎨 UI/UX Design", "💻 Frontend Code", "🌐 Live Preview"])

        with tab1:
            if os.path.exists("requirement.html"):
                with open("requirement.html", "r") as f:
                    st.markdown(f.read(), unsafe_allow_html=True)
            else:
                st.info("No requirement output file was generated.")

        with tab2:
            if os.path.exists("ui_ux.html"):
                with open("ui_ux.html", "r") as f:
                    st.markdown(f.read(), unsafe_allow_html=True)
            else:
                st.info("No UI/UX output file was generated.")

        with tab3:
            if os.path.exists("frontend.html"):
                with open("frontend.html", "r") as f:
                    content = f.read()
                    st.code(content, language="html")
                    st.download_button(
                        label="⬇️ Download frontend.html",
                        data=content,
                        file_name="frontend.html",
                        mime="text/html"
                    )
            else:
                st.info("No frontend output file was generated.")

        with tab4:
            if os.path.exists("frontend.html"):
                with open("frontend.html", "r") as f:
                    content = f.read()
                    st.components.v1.html(content, height=600, scrolling=True)
            else:
                st.info("No frontend output to preview.")

        ## ─── Full Output ───
        with st.expander("📄 View Full Agent Output"):
            st.markdown(str(result))
