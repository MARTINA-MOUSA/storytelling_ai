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
        # Using better model for higher quality images
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    
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
        # Take first 300 characters and extract key elements
        text_snippet = story_text[:300].replace('\n', ' ').strip()
        
        # Create a better prompt with story elements
        # Remove common words and focus on visual elements
        visual_keywords = []
        words = text_snippet.split()
        for word in words[:20]:  # Take first 20 words
            if len(word) > 3:  # Skip short words
                visual_keywords.append(word)
        
        visual_desc = ' '.join(visual_keywords[:10])  # Use first 10 meaningful words
        
        # Enhanced prompt for better quality
        prompt = f"high quality, detailed, beautiful illustration, storybook style, {visual_desc}, professional digital art, vibrant colors, cinematic lighting, 4k, masterpiece"
        return prompt
    
    def _generate_with_hf(self, prompt: str) -> Image.Image:
        """Generate image using Hugging Face API"""
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 50,  # More steps for better quality
                "guidance_scale": 7.5,
                "width": 1024,
                "height": 1024
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
        """Create beautiful default image with gradient"""
        from PIL import ImageFilter
        
        # Create larger image with gradient
        width, height = 1200, 1600
        img = Image.new('RGB', (width, height), color=(135, 206, 250))
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(height):
            # Gradient from light blue to purple
            r = int(135 + (120 * y / height))
            g = int(206 - (50 * y / height))
            b = int(250 - (100 * y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Draw decorative elements
        for i in range(8):
            x = 150 + (i % 4) * 250
            y = 200 + (i // 4) * 400
            size = 80 + i * 10
            # Draw circles with gradient
            for j in range(size, 0, -10):
                alpha = int(255 * (1 - j/size))
                color = (255 - j, 182 + j//2, 193 + j//3)
                draw.ellipse([x-j, y-j, x+j, y+j], outline=color, width=2)
        
        # Add some stars/sparkles
        for i in range(20):
            x = (i * 67) % width
            y = (i * 89) % height
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 200))
        
        # Apply slight blur for smoother look
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
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
