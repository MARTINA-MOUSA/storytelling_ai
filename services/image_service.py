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
        Generate story image that represents the story content
        
        Args:
            story_text: Story text
            user_name: User name (main character)
            language: Language of the story (Arabic or English)
        
        Returns:
            PIL Image representing the story (without text overlay)
        """
        # Extract detailed description from story for image generation
        prompt = self._extract_image_prompt(story_text, user_name)
        
        # Generate base image
        if self.hf_token:
            base_image = self._generate_with_hf(prompt)
        else:
            # Use default image if no API key
            base_image = self._create_default_image()
        
        # Return image only, without text overlay
        return base_image
    
    def _extract_image_prompt(self, story_text: str, user_name: str) -> str:
        """Extract detailed visual description from story for image generation"""
        # Take first 500 characters to get more context
        text_snippet = story_text[:500].replace('\n', ' ').strip()
        
        # Extract key visual elements from the story
        # Look for descriptive words, locations, actions, characters
        import re
        
        # Remove common Arabic/English stop words and focus on visual elements
        # Extract nouns, adjectives, and action words
        words = text_snippet.split()
        visual_keywords = []
        
        # Focus on meaningful words (longer words are usually more descriptive)
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w\s]', '', word)
            if len(clean_word) > 4:  # Focus on longer, more descriptive words
                visual_keywords.append(clean_word)
        
        # Take first 15-20 meaningful words
        visual_desc = ' '.join(visual_keywords[:20])
        
        # If description is too short, use more of the story
        if len(visual_desc) < 50:
            visual_desc = text_snippet[:200].replace('\n', ' ')
        
        # Create a comprehensive prompt that represents the story scene
        prompt = f"beautiful detailed illustration, storybook art style, scene showing: {visual_desc}, main character {user_name}, professional digital art, vibrant colors, cinematic composition, high quality, 4k, masterpiece, children's book illustration style"
        
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
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                image_bytes = response.content
                # Check if response is actually an image
                if image_bytes.startswith(b'\xff\xd8') or image_bytes.startswith(b'\x89PNG'):
                    image = Image.open(io.BytesIO(image_bytes))
                    # Resize to match expected dimensions
                    if image.size != (1024, 1024):
                        image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
                    return image
                else:
                    # Response might be JSON error
                    print(f"API returned non-image response: {response.text[:200]}")
                    return self._create_default_image()
            elif response.status_code == 503:
                # Model is loading, wait a bit and retry or use default
                print("Hugging Face model is loading. Using default image.")
                return self._create_default_image()
            else:
                # On failure, use default image
                print(f"Hugging Face API error (status {response.status_code}): {response.text[:200]}")
                return self._create_default_image()
        except requests.exceptions.Timeout:
            print("Image generation timeout. Using default image.")
            return self._create_default_image()
        except Exception as e:
            print(f"Error generating image: {e}")
            return self._create_default_image()
    
    def _create_default_image(self) -> Image.Image:
        """Create beautiful storybook-style default image"""
        from PIL import ImageFilter
        import math
        
        # Create larger image with beautiful gradient
        width, height = 1200, 1600
        img = Image.new('RGB', (width, height), color=(240, 248, 255))
        draw = ImageDraw.Draw(img)
        
        # Create beautiful multi-color gradient (sky to sunset)
        for y in range(height):
            # Gradient from light blue to warm orange/pink
            progress = y / height
            if progress < 0.3:
                # Sky blue section
                r = int(135 + progress * 30)
                g = int(206 + progress * 20)
                b = int(250 - progress * 30)
            elif progress < 0.7:
                # Transition section
                local_progress = (progress - 0.3) / 0.4
                r = int(165 + local_progress * 60)
                g = int(226 - local_progress * 40)
                b = int(220 - local_progress * 50)
            else:
                # Warm sunset section
                local_progress = (progress - 0.7) / 0.3
                r = int(225 + local_progress * 30)
                g = int(180 - local_progress * 30)
                b = int(170 - local_progress * 20)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Draw beautiful clouds
        for i in range(5):
            x = (i * 280) % (width - 200) + 100
            y = 150 + (i * 120) % 400
            cloud_size = 80 + (i % 3) * 30
            # Draw fluffy cloud with white color
            for offset_x in [-cloud_size//2, 0, cloud_size//2]:
                for offset_y in [0, -cloud_size//3]:
                    draw.ellipse(
                        [x + offset_x - cloud_size//3, y + offset_y - cloud_size//3,
                         x + offset_x + cloud_size//3, y + offset_y + cloud_size//3],
                        fill=(255, 255, 255), outline=(250, 250, 255)
                    )
        
        # Draw mountains silhouette at bottom
        mountain_points = []
        for x in range(0, width, 20):
            y_base = height - 200
            # Create mountain peaks
            peak_height = 150 + 50 * math.sin(x / 100) + 30 * math.sin(x / 50)
            mountain_points.append((x, y_base - peak_height))
        mountain_points.append((width, height))
        mountain_points.append((0, height))
        draw.polygon(mountain_points, fill=(100, 120, 140), outline=(80, 100, 120))
        
        # Draw trees (simple triangles)
        for i in range(8):
            x = 100 + (i * 150) % (width - 200)
            y_base = height - 250 + (i % 3) * 30
            # Tree trunk
            draw.rectangle([x-8, y_base, x+8, y_base+40], fill=(101, 67, 33))
            # Tree top (triangle)
            tree_points = [(x, y_base-60), (x-40, y_base-10), (x+40, y_base-10)]
            draw.polygon(tree_points, fill=(34, 139, 34))
        
        # Add sun/moon
        sun_x, sun_y = width - 200, 200
        sun_radius = 80
        # Draw sun with rays
        draw.ellipse([sun_x-sun_radius, sun_y-sun_radius, sun_x+sun_radius, sun_y+sun_radius],
                    fill=(255, 215, 0), outline=(255, 200, 0), width=3)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = sun_x + (sun_radius + 10) * math.cos(rad)
            y1 = sun_y + (sun_radius + 10) * math.sin(rad)
            x2 = sun_x + (sun_radius + 25) * math.cos(rad)
            y2 = sun_y + (sun_radius + 25) * math.sin(rad)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 215, 0), width=3)
        
        # Add decorative stars
        for i in range(30):
            x = (i * 137) % width
            y = (i * 89) % (height // 2)
            size = 2 + (i % 3)
            # Draw star shape
            star_points = []
            for j in range(5):
                angle = math.radians(j * 144 - 90)
                px = x + size * 3 * math.cos(angle)
                py = y + size * 3 * math.sin(angle)
                star_points.append((px, py))
            draw.polygon(star_points, fill=(255, 255, 200))
        
        # Add floating particles/magic sparkles
        for i in range(15):
            x = (i * 97) % width
            y = (i * 67) % height
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255))
        
        # Apply gentle blur for dreamy effect
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
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
            # Try to use fonts from system with Arabic support
            import platform
            if platform.system() == "Windows":
                # Try Arabic-supporting fonts first, then fallback
                arabic_fonts = [
                    "C:/Windows/Fonts/arial.ttf",  # Arial supports Arabic
                    "C:/Windows/Fonts/segoeui.ttf",  # Segoe UI - excellent Arabic support
                    "C:/Windows/Fonts/tahoma.ttf",  # Tahoma - good Arabic support
                    "C:/Windows/Fonts/calibri.ttf",  # Calibri supports Arabic
                    "C:/Windows/Fonts/arialuni.ttf",  # Arial Unicode - full Unicode support
                ]
                title_font = None
                text_font = None
                for font_path in arabic_fonts:
                    try:
                        title_font = ImageFont.truetype(font_path, title_font_size)
                        text_font = ImageFont.truetype(font_path, text_font_size)
                        break
                    except:
                        continue
                if title_font is None:
                    raise Exception("No font found")
            else:
                # Linux/Mac - try common fonts with Arabic support
                arabic_fonts = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Good Unicode support
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/System/Library/Fonts/Helvetica.ttc",
                    "/System/Library/Fonts/Supplemental/Arial.ttf"
                ]
                title_font = None
                text_font = None
                for font_path in arabic_fonts:
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
        
        # Write story (split into lines) with proper text direction support
        story_lines = self._wrap_text(story_text, img_width - 100, text_font, draw, language)
        y_offset = text_y_start + 140
        
        for line in story_lines:
            if y_offset + 50 > final_height - 40:
                break
            # For Arabic, use right-to-left alignment
            if language.lower() == "arabic":
                # Calculate text width for right alignment
                try:
                    bbox = draw.textbbox((0, 0), line, font=text_font)
                    text_width = bbox[2] - bbox[0]
                    x_pos = img_width - 50 - text_width
                except:
                    x_pos = img_width - 50 - (len(line) * 15)
                draw.text((x_pos, y_offset), line, fill=(30, 30, 30), font=text_font)
            else:
                draw.text((50, y_offset), line, fill=(30, 30, 30), font=text_font)
            y_offset += 42
        
        return final_image
    
    def _wrap_text(self, text: str, max_width: int, font, draw: ImageDraw.Draw, language: str = "Arabic") -> list:
        """Split text into lines based on available width with language support"""
        # For Arabic, handle RTL text properly
        if language.lower() == "arabic":
            # Split by Arabic characters and spaces
            import re
            # Split by spaces and punctuation, keeping Arabic text together
            words = re.findall(r'[\u0600-\u06FF]+|[^\s]+', text)
        else:
            words = text.split()
        
        lines = []
        current_line = ""
        
        # Create temporary image for calculation
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        for word in words:
            # For Arabic, join words with space; for English, use space
            separator = " " if current_line else ""
            test_line = current_line + separator + word
            
            try:
                bbox = temp_draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
            except:
                # Estimation method if calculation fails
                # Arabic characters might be wider
                char_width = 18 if language.lower() == "arabic" else 15
                text_width = len(test_line) * char_width
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
