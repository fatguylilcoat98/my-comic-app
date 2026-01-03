import streamlit as st
import google.generativeai as genai

# Setup the AI
st.set_page_config(page_title="Comic Maker", layout="wide")
st.title("📚 My AI Comic Book Creator")

# Get the API Key safely
api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Input section
    topic = st.text_input("What is your story about?", "A cat who is a secret astronaut")
    
    if st.button("Create Comic"):
        with st.spinner("Writing and drawing..."):
            # 1. Generate Story
            prompt = f"Write a 4-panel comic script about {topic}. For each panel, give a visual description and dialogue."
            story = model.generate_content(prompt)
            st.session_state.story_text = story.text
            
    if "story_text" in st.session_state:
        st.write("### Your Story Script")
        st.write(st.session_state.story_text)
        st.info("To see the art, you can copy the panel descriptions into an AI image generator like Canva or Midjourney while Google updates the image feature!")

else:
    st.warning("Please enter your API Key in the sidebar to start!")
