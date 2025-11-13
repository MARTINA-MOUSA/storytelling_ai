"""
Image generation service for stories using Google Gemini Imagen API
"""
import os
import google.generativeai as genai
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import json
from dotenv import load_dotenv

load_dotenv()

class ImageGenerationService:
    def __init__(self):
        # Use Gemini API key (same as story generation)
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Will use default images.")
        else:
            genai.configure(api_key=self.api_key)
        # Using custom model for image generation
        # Can use Gemini Imagen or custom API
        self.model_name = os.getenv("IMAGE_MODEL", "imagen-4.0-generate-001")
        self.custom_api_key = os.getenv("CUSTOM_IMAGE_API_KEY", "")
        self.custom_model = os.getenv("CUSTOM_IMAGE_MODEL", "")
        
        # Build API URL based on model
        if self.custom_model and self.custom_api_key:
            # Use custom model (e.g., Hugging Face format)
            # Format: https://api-inference.huggingface.co/models/{model}
            if "huggingface.co" in self.custom_model or "/" in self.custom_model:
                # If it's a full URL or Hugging Face model path
                if self.custom_model.startswith("http"):
                    self.api_url = self.custom_model
                else:
                    # Hugging Face model format: org/model-name
                    self.api_url = f"https://api-inference.huggingface.co/models/{self.custom_model}"
            else:
                # Default to Hugging Face if just model name
                self.api_url = f"https://api-inference.huggingface.co/models/{self.custom_model}"
        else:
            # Gemini Imagen API URL (if using Gemini)
            self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateImages"
    
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
        if self.custom_api_key and self.custom_model:
            # Use custom API (e.g., Hugging Face, custom endpoint)
            base_image = self._generate_with_custom_api(prompt)
        elif self.api_key:
            # Use Gemini Imagen
            base_image = self._generate_with_gemini(prompt)
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
    
    def _generate_with_gemini(self, prompt: str) -> Image.Image:
        """Generate image using Google Gemini Imagen API via REST API"""
        try:
            # Try using REST API first
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "prompt": prompt,
                "numberOfImages": 1,
                "aspectRatio": "1:1",
                "safetyFilterLevel": "block_some",
                "personGeneration": "allow_all"
            }
            
            # Make request to Imagen API
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for image in response
                if 'generatedImages' in result and len(result['generatedImages']) > 0:
                    # Get base64 encoded image
                    image_data_b64 = result['generatedImages'][0].get('base64String', '')
                    if image_data_b64:
                        import base64
                        image_bytes = base64.b64decode(image_data_b64)
                        image = Image.open(io.BytesIO(image_bytes))
                        # Resize if needed
                        if image.size[0] < 1024 or image.size[1] < 1024:
                            image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
                        return image
                
                # Try alternative response format
                if 'images' in result and len(result['images']) > 0:
                    image_data_b64 = result['images'][0].get('base64String', '')
                    if image_data_b64:
                        import base64
                        image_bytes = base64.b64decode(image_data_b64)
                        image = Image.open(io.BytesIO(image_bytes))
                        if image.size[0] < 1024 or image.size[1] < 1024:
                            image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
                        return image
                
                print(f"Unexpected response format: {list(result.keys())}")
                return self._create_default_image()
            else:
                print(f"Imagen API error (status {response.status_code}): {response.text[:500]}")
                # Try fallback method using SDK
                return self._generate_with_gemini_sdk(prompt)
                
        except requests.exceptions.Timeout:
            print("Image generation timeout. Trying SDK method...")
            return self._generate_with_gemini_sdk(prompt)
        except Exception as e:
            print(f"Error with REST API: {e}. Trying SDK method...")
            return self._generate_with_gemini_sdk(prompt)
    
    def _generate_with_custom_api(self, prompt: str) -> Image.Image:
        """Generate image using custom API (e.g., Hugging Face, custom endpoint, etc.)"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.custom_api_key}"
            }
            
            # Try Hugging Face format first (most common)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "width": 1024,
                    "height": 1024
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                # Check if response is an image (binary)
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type or response.content.startswith(b'\xff\xd8') or response.content.startswith(b'\x89PNG'):
                    image = Image.open(io.BytesIO(response.content))
                    if image.size[0] < 1024 or image.size[1] < 1024:
                        image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
                    return image
                
                # Try JSON response with base64 image
                try:
                    result = response.json()
                    # Check various possible response formats
                    if 'image' in result:
                        import base64
                        image_data = base64.b64decode(result['image'])
                        image = Image.open(io.BytesIO(image_data))
                        return image
                    elif 'generated_image' in result:
                        import base64
                        image_data = base64.b64decode(result['generated_image'])
                        image = Image.open(io.BytesIO(image_data))
                        return image
                    elif isinstance(result, list) and len(result) > 0:
                        # Some APIs return list with image data
                        first_item = result[0]
                        if 'image' in first_item:
                            import base64
                            image_data = base64.b64decode(first_item['image'])
                            image = Image.open(io.BytesIO(image_data))
                            return image
                except Exception as json_error:
                    print(f"Error parsing JSON response: {json_error}")
            
            elif response.status_code == 503:
                # Model is loading
                print("Model is loading. Please wait and try again.")
                return self._create_default_image()
            
            print(f"Custom API error (status {response.status_code}): {response.text[:500]}")
            return self._create_default_image()
            
        except Exception as e:
            print(f"Error with custom API: {e}")
            import traceback
            traceback.print_exc()
            return self._create_default_image()
    
    def _generate_with_gemini_sdk(self, prompt: str) -> Image.Image:
        """Fallback: Generate image using Google Generative AI SDK"""
        try:
            # Try using the SDK method
            imagen_model = genai.GenerativeModel(self.model_name)
            
            # Generate image with the prompt
            response = imagen_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "top_k": 40,
                }
            )
            
            # Try to extract image from various response formats
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        # Check for inline data (image)
                        if hasattr(part, 'inline_data'):
                            image_data = part.inline_data.data
                            image = Image.open(io.BytesIO(image_data))
                            if image.size[0] < 1024 or image.size[1] < 1024:
                                image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
                            return image
                        # Check for text that might be base64
                        if hasattr(part, 'text'):
                            import base64
                            try:
                                image_data = base64.b64decode(part.text)
                                image = Image.open(io.BytesIO(image_data))
                                return image
                            except:
                                pass
            
            print("No image found in SDK response. Using default image.")
            return self._create_default_image()
            
        except Exception as e:
            print(f"Error generating image with Gemini SDK: {e}")
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
