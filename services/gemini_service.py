"""
Gemini service for generating interactive stories
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load from .env file if it exists (for local development)
load_dotenv()

class GeminiStoryService:
    def __init__(self):
        # Try to load from multiple sources (in order of priority):
        # 1. Streamlit secrets (for Streamlit Cloud - checked first)
        # 2. Environment variables (from .env file or system)
        # 3. config.py file (for local testing)
        
        api_key = None
        
        # First, try to get from Streamlit secrets (for Streamlit Cloud)
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                # Try different ways to access secrets
                if hasattr(st.secrets, 'get'):
                    api_key = st.secrets.get('GEMINI_API_KEY')
                elif isinstance(st.secrets, dict) and 'GEMINI_API_KEY' in st.secrets:
                    api_key = st.secrets['GEMINI_API_KEY']
                elif hasattr(st.secrets, 'GEMINI_API_KEY'):
                    api_key = getattr(st.secrets, 'GEMINI_API_KEY', None)
        except Exception:
            pass
        
        # If not found in secrets, try environment variables
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        # If still not found, try config.py file (for local testing only)
        if not api_key:
            try:
                from pathlib import Path
                project_root = Path(__file__).parent.parent
                config_path = project_root / "config.py"
                if config_path.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("config", config_path)
                    config = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config)
                    if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
                        api_key = config.GEMINI_API_KEY
            except Exception:
                pass
        
        if not api_key:
            # Provide detailed error message
            error_msg = "GEMINI_API_KEY not found.\n\n"
            error_msg += "Tried to load from:\n"
            error_msg += "1. Streamlit Secrets (for Streamlit Cloud)\n"
            error_msg += "2. Environment variables (.env file or system)\n"
            error_msg += "3. config.py file (for local testing)\n\n"
            error_msg += "Please add it in one of these ways:\n"
            error_msg += "1. For Streamlit Cloud: Settings → Secrets → Add: GEMINI_API_KEY = \"your_key\"\n"
            error_msg += "2. Create .env file: GEMINI_API_KEY=your_key\n"
            error_msg += "3. Create config.py: GEMINI_API_KEY = 'your_key'"
            raise ValueError(error_msg)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_story(self, user_name: str, story_type: str, characters: str, 
                      events: str, language: str = "Arabic", theme: str = None) -> str:
        """
        Generate an interactive story based on user choices
        
        Args:
            user_name: User's name (will be the main character)
            story_type: Type of story (adventure, sci-fi, romance, etc.)
            characters: Other characters in the story
            events: Main events to include
            language: Story language - "Arabic" or "English"
            theme: Additional theme or idea (optional)
        
        Returns:
            Generated story in the selected language
        """
        # Determine language instruction
        if language.lower() == "arabic":
            lang_instruction = "Arabic (العربية)"
            lang_style = "Write the story in beautiful Arabic (either Modern Standard Arabic or understandable dialect)"
        else:
            lang_instruction = "English"
            lang_style = "Write the story in fluent, natural English"
        
        prompt = f"""You are a professional and creative storyteller. Write a complete, coherent, and engaging short story in {lang_instruction}.

CRITICAL REQUIREMENTS - MUST FOLLOW:
- Main character name (the hero): {user_name}
- Story type/genre: {story_type}
- Other characters: {characters}
- Main events: {events}
{f"- Theme or idea: {theme}" if theme else ""}

STORY STRUCTURE REQUIREMENTS (VERY IMPORTANT):
1. {lang_style}
2. The story MUST be completely coherent and follow a logical sequence from beginning to end
3. Story length: 500-700 words (complete story)
4. The story MUST have three clear parts:
   - BEGINNING: Introduce {user_name} and the setting, establish the situation
   - MIDDLE: Develop the conflict/challenge, show {user_name}'s journey and interactions with {characters}
   - END: Resolve the story with a satisfying conclusion
5. Events MUST flow naturally and logically - each event should connect smoothly to the next
6. NO abrupt jumps or disconnected scenes - everything must be connected
7. Use smooth transitions between paragraphs and scenes

WRITING QUALITY REQUIREMENTS:
8. Use lively and natural dialogues between characters
9. Add beautiful, vivid descriptions of scenes, places, and emotions
10. Ensure that {user_name} is ALWAYS the main character and central focus
11. Use beautiful literary language appropriate for {story_type} genre
12. Create suspense and excitement naturally through the story progression
13. Make the story suitable for general audience with positive values
14. The story MUST match the {story_type} genre style and atmosphere throughout

STORY FLOW REQUIREMENTS:
- Start with an engaging opening that introduces {user_name} and the world
- Build the story step by step, connecting all events logically
- Each paragraph should flow naturally into the next
- Include the events: {events} in a natural, sequential order
- End with a satisfying conclusion that ties everything together
- The entire story should read as one continuous, connected narrative

Write the complete story now, ensuring it is fully coherent, well-structured, and flows smoothly from start to finish:"""

        try:
            response = self.model.generate_content(prompt)
            story = response.text.strip()
            return story
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")
