# String Art Generator 🎨

Transform your images into beautiful string art patterns! This application uses a sophisticated algorithm to create continuous string paths that recreate your image using only black thread on a circular board with pins.

![String Art Example](https://via.placeholder.com/600x300/000000/FFFFFF?text=String+Art+Generator)

## Features

- **Smart Algorithm**: Uses a greedy approach to find the optimal string placement
- **Continuous Path**: Generates one continuous string path for easy physical construction
- **Customizable Parameters**: Adjust number of pins, connections, and string opacity
- **Multiple Download Formats**: Get your pattern as image, JSON, or text file
- **Real-time Preview**: See your string art generate in real-time

## Quick Start

### Online Version (Streamlit Cloud)

The easiest way to use this application is through Streamlit Cloud:

1. Visit the deployed app: [String Art Generator](your-app-url-here)
2. Upload an image
3. Adjust parameters
4. Generate and download your string art pattern

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/string-art-generator.git
cd string-art-generator

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## How to Use

1. **Upload an Image**: Choose a high-contrast image for best results
2. **Set Parameters**:
   - **Number of pins**: 50-400 (more pins = finer detail)
   - **Number of connections**: 500-10000 (more connections = darker result)
   - **Canvas size**: Choose output resolution
   - **String opacity**: Adjust darkness per string
3. **Generate**: Click "Generate String Art" and wait for processing
4. **Download**: Get your pattern as image, JSON, or text file

## Algorithm Details

The string art generator uses a **greedy algorithm** that:

1. Converts the image to grayscale and applies a circular mask
2. Places pins evenly around the circle's perimeter  
3. Iteratively selects string connections that best match the target image
4. Creates a continuous path by choosing the next best pin from the current position
5. Optimizes for maximum darkness where the original image is dark

## File Formats

### Connection Sequence (JSON/Text)
Contains the complete pin sequence for physical construction:
```
Start at pin 0, connect to pin 45, then to pin 123, etc.
```

### Visualization (PNG)
Shows the complete string art with pins and strings for reference.

## Tips for Best Results

### Image Selection
- **High contrast** images work best
- **Simple subjects** with clear edges
- **Black and white** or monochrome images
- **Portraits** and **simple shapes** are ideal

### Parameter Tuning
- Start with **200 pins** and **3000 connections**
- Increase pins for more detail, increase connections for darker results
- Lower string opacity if using thin thread physically

### Physical Construction
- Use a circular wooden board or large embroidery hoop
- Mark pin positions evenly around the perimeter
- Use thin black thread or embroidery floss
- Number your pins and follow the sequence exactly
- Keep string tension consistent

## Project Structure

```
string-art-generator/
├── app.py                 # Main Streamlit application
├── string_art_generator.py # Core algorithm implementation
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/           # Streamlit configuration (optional)
    └── config.toml
```

## Technical Requirements

- Python 3.7+
- Streamlit
- OpenCV
- NumPy
- Pillow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Improvement
- Alternative algorithms (genetic algorithm, simulated annealing)
- Color string art support
- Batch processing
- Mobile-optimized interface
- Advanced image preprocessing options

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the mathematical art of string art and circle art
- Algorithm based on research in computational art generation
- Thanks to the Streamlit community for the amazing framework

## Examples

### Portrait
![Portrait Example](https://via.placeholder.com/300x300/000000/FFFFFF?text=Portrait+Example)

### Landscape  
![Landscape Example](https://via.placeholder.com/300x300/000000/FFFFFF?text=Landscape+Example)

### Abstract
![Abstract Example](https://via.placeholder.com/300x300/000000/FFFFFF?text=Abstract+Example)

---

**Made with ❤️ using Streamlit**

For questions or support, please open an issue on GitHub.
