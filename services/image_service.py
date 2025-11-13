"""
Image generation service for stories using Hugging Face API
"""
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv

load_dotenv()

class ImageGenerationService:
    def __init__(self):
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY", "")
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    def generate_story_image(self, story_text: str, user_name: str, language: str = "Arabic") -> Image.Image:
        """
        Generate story image with user name and text
        
        Args:
            story_text: Story text
            user_name: User name
            language: Language of the story (Arabic or English)
        
        Returns:
            PIL Image with user name and story
        """
        # Extract short description from story for image generation
        prompt = self._extract_image_prompt(story_text)
        
        # Generate base image
        if self.hf_token:
            base_image = self._generate_with_hf(prompt)
        else:
            # Use default image if no API key
            base_image = self._create_default_image()
        
        # Add user name and story text to image
        final_image = self._add_text_to_image(base_image, user_name, story_text, language)
        
        return final_image
    
    def _extract_image_prompt(self, story_text: str) -> str:
        """Extract suitable description for image generation from story"""
        # Take first 200 characters of story as description
        prompt = story_text[:200].replace('\n', ' ').strip()
        # Add keywords to improve image
        prompt = f"beautiful illustration, story scene, {prompt}, digital art, vibrant colors"
        return prompt
    
    def _generate_with_hf(self, prompt: str) -> Image.Image:
        """Generate image using Hugging Face API"""
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                return image
            else:
                # On failure, use default image
                return self._create_default_image()
        except Exception as e:
            print(f"Error generating image: {e}")
            return self._create_default_image()
    
    def _create_default_image(self) -> Image.Image:
        """Create beautiful default image"""
        # Create image with beautiful color gradient
        img = Image.new('RGB', (1200, 1600), color=(135, 206, 250))
        draw = ImageDraw.Draw(img)
        
        # Draw decorative shapes
        for i in range(5):
            x = 100 + i * 200
            y = 200 + i * 150
            draw.ellipse([x-50, y-50, x+50, y+50], fill=(255, 182, 193, 100))
        
        return img
    
    def _add_text_to_image(self, base_image: Image.Image, user_name: str, story_text: str, language: str = "Arabic") -> Image.Image:
        """Add user name and story text to image"""
        # Create larger image to accommodate text
        img_width, img_height = base_image.size
        text_area_height = 800  # Increased space for text
        final_height = img_height + text_area_height
        
        # Create new image
        final_image = Image.new('RGB', (img_width, final_height), color=(255, 255, 255))
        
        # Paste base image at top
        final_image.paste(base_image, (0, 0))
        
        draw = ImageDraw.Draw(final_image)
        
        # Try to load font, otherwise use default
        title_font_size = 56
        text_font_size = 28
        
        try:
            # Try to use fonts from system
            import platform
            if platform.system() == "Windows":
                # Try common fonts in Windows
                fonts = [
                    "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/tahoma.ttf",
                    "C:/Windows/Fonts/calibri.ttf",
                    "arial.ttf"
                ]
                title_font = None
                text_font = None
                for font_path in fonts:
                    try:
                        title_font = ImageFont.truetype(font_path, title_font_size)
                        text_font = ImageFont.truetype(font_path, text_font_size)
                        break
                    except:
                        continue
                if title_font is None:
                    raise Exception("No font found")
            else:
                # Linux/Mac - try common fonts
                fonts = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/System/Library/Fonts/Helvetica.ttc"
                ]
                title_font = None
                text_font = None
                for font_path in fonts:
                    try:
                        title_font = ImageFont.truetype(font_path, title_font_size)
                        text_font = ImageFont.truetype(font_path, text_font_size)
                        break
                    except:
                        continue
                if title_font is None:
                    raise Exception("No font found")
        except:
            # Use default font
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw semi-transparent background for text
        text_y_start = img_height + 20
        draw.rectangle([20, text_y_start, img_width - 20, final_height - 20], 
                      fill=(255, 255, 255, 240), outline=(200, 200, 200), width=3)
        
        # Write user name
        if language.lower() == "arabic":
            title_text = f"قصة {user_name}"
        else:
            title_text = f"{user_name}'s Story"
        
        # Calculate text width
        try:
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
        except:
            # Alternative method
            title_width = len(title_text) * 30
        title_x = (img_width - title_width) // 2
        draw.text((title_x, text_y_start + 40), title_text, fill=(50, 50, 50), font=title_font)
        
        # Write story (split into lines)
        story_lines = self._wrap_text(story_text, img_width - 100, text_font, draw)
        y_offset = text_y_start + 140
        
        for line in story_lines:
            if y_offset + 50 > final_height - 40:
                break
            draw.text((50, y_offset), line, fill=(30, 30, 30), font=text_font)
            y_offset += 42
        
        return final_image
    
    def _wrap_text(self, text: str, max_width: int, font, draw: ImageDraw.Draw) -> list:
        """Split text into lines based on available width"""
        words = text.split()
        lines = []
        current_line = ""
        
        # Create temporary image for calculation
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            try:
                bbox = temp_draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
            except:
                # Estimation method if calculation fails
                text_width = len(test_line) * 15
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
