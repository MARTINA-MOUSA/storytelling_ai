"""
Streamlit app for generating interactive stories
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.gemini_service import GeminiStoryService
from services.image_service import ImageGenerationService
from PIL import Image
import io

# Page settings
st.set_page_config(
    page_title="Interactive Story Generator | Storytelling AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .story-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📚 Interactive Story Generator with AI</h1>
    <p>Create your own stories based on your choices!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API information
    st.subheader("API Keys")
    st.info("""
    For best results, add:
    - **GEMINI_API_KEY**: from Google AI Studio
    - **HUGGINGFACE_API_KEY**: (optional) for better image generation
    """)
    
    # Project information
    st.subheader("ℹ️ Information")
    st.markdown("""
    This app uses:
    - 🤖 Google Gemini for story generation
    - 🎨 Hugging Face for image generation
    - 🎯 Easy-to-use interactive interface
    """)

# Initialize services
@st.cache_resource
def init_services():
    try:
        gemini_service = GeminiStoryService()
        image_service = ImageGenerationService()
        return gemini_service, image_service, None
    except Exception as e:
        return None, None, str(e)

gemini_service, image_service, error = init_services()

if error:
    st.error(f"❌ Initialization error: {error}")
    st.info("Make sure to add GEMINI_API_KEY in .env file")
    st.stop()

# Input form
st.header("📝 Enter Your Story Details")

col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("👤 Your Name (will be the hero)", value="Ahmed", help="This name will be used as the main character")
    language = st.selectbox(
        "🌐 Story Language",
        ["Arabic", "English"],
        help="Choose the language for your story"
    )

with col2:
    story_type = st.selectbox(
        "📖 Story Type/Genre",
        ["Adventure", "Science Fiction", "Romance", "Horror", "Comedy", "Historical", "Fantasy", "Realistic", "Mystery", "Thriller"],
        help="Select the genre of your story"
    )
    theme = st.text_input(
        "🎭 Additional Theme (optional)",
        value="",
        help="Additional theme or idea for the story"
    )

characters = st.text_area(
    "👥 Characters",
    value="A loyal friend, a wise teacher",
    help="Mention other characters in the story (separated by commas)"
)

events = st.text_area(
    "🎬 Main Events",
    value="A journey to find a hidden treasure, facing challenges, discovering a surprise",
    help="Describe the events you want to happen in the story"
)

# Generate button
if st.button("✨ Generate Story", type="primary"):
    if not user_name:
        st.warning("⚠️ Please enter your name")
    else:
        with st.spinner("🔄 Generating your story... This may take a few moments"):
            try:
                # Generate story
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📝 Writing your story...")
                progress_bar.progress(30)
                
                story = gemini_service.generate_story(
                    user_name=user_name,
                    story_type=story_type,
                    characters=characters,
                    events=events,
                    language=language,
                    theme=theme if theme else None
                )
                
                status_text.text("🎨 Generating image...")
                progress_bar.progress(60)
                
                # Generate image
                story_image = image_service.generate_story_image(story, user_name, language)
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Display results
                st.success("🎉 Your story has been generated successfully!")
                
                # Display image
                caption = f"{user_name}'s Story" if language == "English" else f"قصة {user_name}"
                st.image(story_image, caption=caption, use_container_width=True)
                
                # Display story as text
                st.markdown("### 📖 The Story:")
                st.markdown(f'<div class="story-container">{story}</div>', unsafe_allow_html=True)
                
                # Download button
                img_buffer = io.BytesIO()
                story_image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                file_name = f"{user_name}_story.png" if language == "English" else f"قصة_{user_name}.png"
                st.download_button(
                    label="💾 Download Image",
                    data=img_buffer,
                    file_name=file_name,
                    mime="image/png"
                )
                
                # Save to session
                st.session_state['last_story'] = story
                st.session_state['last_image'] = story_image
                st.session_state['last_user_name'] = user_name
                st.session_state['last_language'] = language
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Check your API keys settings in .env file")

# Display last generated story
if 'last_story' in st.session_state:
    st.markdown("---")
    st.header("📚 Last Generated Story")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        caption = f"{st.session_state['last_user_name']}'s Story" if st.session_state.get('last_language', 'English') == "English" else f"قصة {st.session_state['last_user_name']}"
        st.image(st.session_state['last_image'], caption=caption)
    
    with col2:
        story_title = f"{st.session_state['last_user_name']}'s Story" if st.session_state.get('last_language', 'English') == "English" else f"قصة {st.session_state['last_user_name']}"
        st.markdown(f"### {story_title}")
        st.markdown(f'<div class="story-container">{st.session_state["last_story"]}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Made with ❤️ using Streamlit and Google Gemini</p>
</div>
""", unsafe_allow_html=True)
