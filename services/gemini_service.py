"""
Gemini service for generating interactive stories
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiStoryService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
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
        
        prompt = f"""You are a professional and creative storyteller. Write an engaging interactive short story in {lang_instruction}.

Basic Requirements:
- Main character name (the hero): {user_name}
- Story type/genre: {story_type}
- Other characters: {characters}
- Main events: {events}
{f"- Theme or idea: {theme}" if theme else ""}

Creative Writing Instructions:
1. {lang_style}
2. Make the story interactive and engaging with suspense elements
3. Story length: 400-600 words (medium-length story)
4. Use lively and natural dialogues between characters
5. Add beautiful descriptions of scenes and places
6. Ensure that {user_name} is the main character and central focus of the story
7. Write the story in a beautiful narrative style with clear beginning, middle, and end
8. Use beautiful literary language with some suspense and excitement
9. Make the story suitable for general audience with positive values
10. The story should match the {story_type} genre style and atmosphere

Start the story now with an engaging opening sentence:"""

        try:
            response = self.model.generate_content(prompt)
            story = response.text.strip()
            return story
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")
