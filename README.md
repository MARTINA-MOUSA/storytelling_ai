# 📚 Interactive Story Generator with AI

An interactive application for generating custom short stories using Google Gemini AI with automatic image generation.

> 🌐 **Want to deploy online?** Check out [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md) for easy deployment guides!

## ✨ Features

- 🎯 **Interactive Story Generation**: Create custom stories based on your choices
- 👤 **Character Customization**: Use your name as the story hero
- 📖 **Multiple Genres**: Adventure, Sci-Fi, Romance, Horror, Comedy, Historical, Fantasy, Realistic, Mystery, Thriller
- 🌐 **Multi-language Support**: Generate stories in Arabic or English
- 🎨 **Automatic Image Generation**: Beautiful image containing your name and story
- 💾 **Download Stories**: Save your stories as images
- 🎨 **Beautiful UI**: Modern and easy-to-use Streamlit interface

## 🛠️ Technologies Used

- **Streamlit**: Interactive user interface
- **Google Gemini AI**: Text and story generation
- **Clipdrop API**: High-quality image generation
- **Pillow**: Image processing

## 📋 Requirements

- Python 3.8 or higher
- Google Gemini API key (required for story generation)
- Clipdrop API key (required for image generation)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd storytelling_ai
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup API Keys

1. Copy `env_template.txt` to `.env`:
   ```bash
   copy env_template.txt .env  # Windows
   # or
   cp env_template.txt .env    # Linux/Mac
   ```

2. Get Gemini API Key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an account or sign in
   - Create a new API key
   - Copy the key

3. (Optional) Get Hugging Face API Key:
   - Go to [Hugging Face](https://huggingface.co/settings/tokens)
   - Create an account or sign in
   - Create a new token
   - Copy the key

4. Edit `.env` file and add your keys:
   ```env
   GEMINI_API_KEY=your_actual_gemini_key_here
   HUGGINGFACE_API_KEY=your_actual_hf_key_here
   ```

## 🎮 Usage

### Run the Application

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
streamlit run frontend/app.py
```

The app will automatically open in your browser at: `http://localhost:8501`

### Using the Application

1. **Enter your name**: It will become the hero's name in the story
2. **Choose language**: Select Arabic or English
3. **Select story type**: Choose from the dropdown menu
4. **Add characters**: Mention other characters in the story
5. **Describe events**: Mention the main events you want
6. **Add theme** (optional): Any additional ideas
7. **Click "Generate Story"**: Wait a moment and you'll get your story with an image!

## 📁 Project Structure

```
storytelling_ai/
├── frontend/
│   └── app.py              # Main Streamlit application
├── services/
│   ├── __init__.py
│   ├── gemini_service.py   # Story generation service
│   └── image_service.py    # Image generation service
├── outputs/                # Folder for generated stories
├── .env.template           # Environment variables template
├── requirements.txt        # Required libraries
├── setup.bat               # Setup script (Windows)
├── run.bat                 # Run script (Windows)
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
└── TROUBLESHOOTING.md      # Troubleshooting guide
```

## 🔧 Customization

### Adding New Story Types

You can add new story types in `frontend/app.py` in the `story_type` list:

```python
story_type = st.selectbox(
    "📖 Story Type/Genre",
    ["Adventure", "Sci-Fi", "Romance", "Horror", "Comedy", "Historical", "Fantasy", "Realistic", "Mystery", "Thriller", "New Type"]
)
```

### Improving Image Quality

To improve generated image quality:
1. Get a Hugging Face API key
2. Add it to `.env` file
3. You can also change the image model in `services/image_service.py`

## 🐛 Troubleshooting

### Error "GEMINI_API_KEY not found"
- Make sure `.env` file exists in the project folder
- Make sure the key is added correctly: `GEMINI_API_KEY=your_key`

### Images not generating
- If you don't have a Hugging Face key, a default beautiful image will be used
- Make sure you have internet connection

### Story not generating
- Check if your Gemini API key is valid
- Check your internet connection
- There might be a daily usage limit for Gemini API

## 📝 License

This project is open source and available for free use.

## 🤝 Contributing

Contributions are welcome! You can:
- Add new story types
- Improve the user interface
- Add new features

## 📧 Support

If you encounter any issues or have suggestions, please open an issue in the project.

## 🌟 Features in Detail

### Story Generation
- Uses Google Gemini Pro model for high-quality story generation
- Supports multiple languages (Arabic and English)
- Customizable story length (400-600 words)
- Interactive and engaging narratives

### Image Generation
- Automatic image generation with story text overlay
- Supports both Arabic and English text rendering
- Beautiful default images if API is unavailable
- Customizable image dimensions

### User Interface
- Modern Streamlit interface
- Real-time progress indicators
- Download generated stories as images
- Session state management for last generated story

---

**Enjoy creating your own stories! 📚✨**
