import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AI Comic Studio", layout="wide")
st.title("🎨 The Ultimate AI Comic Creator")
st.markdown("---")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("1. Setup")
    api_key = st.text_input("Enter Google API Key:", type="password")
    
    st.header("2. Style Settings")
    art_style = st.selectbox("Choose Art Style:", 
                            ["Classic Superhero", "Japanese Manga", "3D Pixar Style", "Dark Noir", "Water Color"])
    
    panel_count = st.slider("Number of Panels:", 2, 6, 4)

# --- MAIN INTERFACE ---
if api_key:
    genai.configure(api_key=api_key)
    # Using the fast Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.subheader("3. Tell Your Story")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("🎤 **Talk to your app:**")
        audio_bytes = audio_recorder(text="Click to record your idea", icon_size="2x")
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.info("Audio captured! (Type the main idea below to confirm)")

    with col2:
        st.write("⌨️ **Type or summarize here:**")
        user_story = st.text_area("What happens in your comic?", placeholder="e.g. A robot who wants to be a chef...")

    if st.button("🚀 CREATE FULL COMIC BOOK"):
        if user_story:
            with st.spinner("Generating your masterpiece..."):
                # The "Evaluation" Prompt
                prompt = f"""
                Create a comic book script for a story about: {user_story}.
                The art style should be: {art_style}.
                Provide exactly {panel_count} panels plus 1 Cover.
                For each panel, include:
                - PANEL NUMBER
                - VISUAL DESCRIPTION (for an image generator)
                - DIALOGUE
                """
                
                response = model.generate_content(prompt)
                st.session_state.finished_story = response.text
                st.balloons()
        else:
            st.error("Please provide a story idea first!")

    # --- THE SCROLLABLE COMIC DISPLAY ---
    if "finished_story" in st.session_state:
        st.markdown("---")
        st.header("📖 YOUR COMIC BOOK")
        
        # Displaying the story in a nice, scrollable way
        st.markdown(st.session_state.finished_story)
        
        st.success("Scroll up to read your panels! You can copy/paste these into an image generator.")
        
        if st.button("🗑️ Start Over / Delete"):
            del st.session_state.finished_story
            st.rerun()
else:
    st.warning("👈 Please enter your Google API Key in the sidebar to start!")
