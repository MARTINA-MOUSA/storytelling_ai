"""
Gemini service for generating interactive stories
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiStoryService:
    def __init__(self):
        # Try to load from environment variables (works for both .env file and cloud platforms)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please add it in environment variables or .env file. "
                "For Streamlit Cloud: Settings → Secrets → Add GEMINI_API_KEY"
            )
        
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
