import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder # New tool for talking!

st.set_page_config(page_title="Comic Maker", layout="wide")
st.title("📚 My AI Comic Book Creator")

# Sidebar for the API Key
api_key = st.sidebar.text_input("1. Paste your Google API Key here:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using the latest model for better storytelling
    model = genai.GenerativeModel('gemini-2.0-flash')

    st.subheader("2. Tell your story")
    
    # --- VOICE OPTION ---
    st.write("🎤 **Option A: Speak your story** (Click the mic, talk, then click again)")
    audio_bytes = audio_recorder(text="Click to record", icon_size="2x")
    
    # --- TYPING OPTION ---
    st.write("⌨️ **Option B: Type your story**")
    user_story = st.text_area("What is your story about?", placeholder="Once upon a time, a dragon discovered a smartphone...")

    # If you spoke, we try to use that (Note: This requires a small extra step to process audio)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.info("Audio recorded! (Note: In a full version, this would be sent to Google to turn into text automatically).")

    if st.button("🚀 Create My Comic Book"):
        if not user_story:
            st.error("Please type a story or record one first!")
        else:
            with st.spinner("Writing and drawing your comic..."):
                # We tell the AI to be a professional comic writer
                prompt = f"""
                Act as a professional comic book writer. 
                Based on this story idea: '{user_story}', 
                create a 5-panel comic script. 
                Include:
                1. A cool Cover Title and Description.
                2. Detailed visual descriptions for each panel.
                3. Character dialogue for each panel.
                """
                story = model.generate_content(prompt)
                
                # Display the result in a scrollable view
                st.markdown("---")
                st.header("📖 Your Custom Comic Book")
                st.write(story.text)
                st.balloons()
else:
    st.warning("Please enter your API Key in the sidebar to start!")
