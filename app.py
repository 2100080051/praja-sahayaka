import streamlit as st
from services.llm_service import planner_agent
from agents.executor import executor_agent, responder_agent
from services.memory_service import save_interaction
from services.voice_service_v2 import get_voice_audio
import sr_handler 

st.set_page_config(page_title="Praja Sahayaka - Voice Agent", layout="wide", page_icon="🇮🇳")

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatInput {
        border-radius: 20px;
    }
    .user-message {
        background-color: #2b313e;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .agent-message {
        background-color: #1c2333;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇳 ప్రజా సహాయక (Praja Sahayaka)")
st.caption("మీ వ్యక్తిగత ప్రభుత్వ పథకాల గైడ్ (Personal Government Scheme Assistant)")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # 1. Load Welcome Message with Audio
    welcome_text = "నమస్కారం! నేను మీ ప్రజా సహాయక్. నేను మీకు ఎలా సహాయపడగలను?"
    # Prefetch welcome audio if possible, or generate on fly
    from services.voice_service_v2 import get_voice_audio
    welcome_audio = get_voice_audio(welcome_text)
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_text, "audio": welcome_audio})
    
    # 2. Load Persistent History
    from services.memory_service import load_history
    history = load_history()
    
    for item in history:
        # We don't regenerate audio for history to save time/resources unless stored
        st.session_state.messages.append({"role": "user", "content": item["user_input"]})
        st.session_state.messages.append({"role": "assistant", "content": item["agent_response"]})

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "audio" in msg and msg["audio"]:
            # Autoplay ONLY the last message to avoid chaos on reload
            # And only if it's an assistant message
            is_last_message = (i == len(st.session_state.messages) - 1)
            st.audio(msg["audio"], format="audio/mp3", start_time=0, autoplay=is_last_message)

user_input = st.chat_input("మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి (లేదా మైక్ ఉపయోగించండి)...")

with st.sidebar:
    st.header("Tools")
    
    # mic
    try:
        from streamlit_mic_recorder import mic_recorder
        audio = mic_recorder(start_prompt="🎤 మాట్లాడండి (Speak)", stop_prompt="⏹️ ఆపండి (Stop)", key='recorder')
    except ImportError:
        st.error("Please install streamlit-mic-recorder")
        audio = None
        
    st.divider()
    
    # File Uploader
    st.subheader("📄 Document Upload")
    uploaded_file = st.file_uploader("Upload PDF / Form", type=["pdf"])
    
    doc_context = ""
    if uploaded_file is not None:
        from services.document_service import extract_text_from_pdf
        with st.spinner("Analyzing document..."):
            text = extract_text_from_pdf(uploaded_file.read())
            if text:
                doc_context = f"\n\n[USER UPLOADED DOCUMENT CONTENT]:\n{text[:4000]}...\n(End of Document)\n"
                st.success("Document Analyzed! You can now ask questions about it.")
            else:
                st.error("Could not read document.")
    
    st.divider()
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "నమస్కారం! నేను మీ ప్రభుత్వ పథకాల సహాయకుడిని. నేను మీకు ఎలా సహాయపడగలను?"})
        st.rerun()

input_text = None

if audio:
    input_text = sr_handler.transcribe_audio(audio['bytes'])

if user_input:
    input_text = user_input

if input_text:
    # Append document context if available
    full_prompt = input_text + doc_context
    
    # Store just the text for display, but use full_prompt for logic
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

    with st.spinner("Processing..."):
        # We pass full_prompt to the planner so it knows about the doc
        plan = planner_agent(full_prompt)
        
        # If the plan is general chat but we have a doc, the agent should handle it via LLM
        # Executor runs as normal
        result = executor_agent(plan)
        
        # Responder usually takes just user_input, but here we want it to know about the doc context too
        # to answer questions like "Is this valid?"
        # So we pass full_prompt to responder as well
        response_text = responder_agent(full_prompt, result)
        
        audio_bytes = get_voice_audio(response_text)
        save_interaction(input_text, response_text, plan)

    st.session_state.messages.append({"role": "assistant", "content": response_text, "audio": audio_bytes})
    with st.chat_message("assistant"):
        st.markdown(response_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

    st.rerun()
