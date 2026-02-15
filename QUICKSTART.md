# Quick Start Guide - Speed Sensing AI

## Installation

1. Install Tesseract OCR (required):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

### 1. Detect Speed from Image
```bash
python speed_detector.py image.jpg output.jpg
```

### 2. Real-time Video Detection
```bash
# From video file
python video_speed_detector.py video.mp4 output.mp4

# From webcam (press 'q' to quit)
python video_speed_detector.py 0
```

### 3. Run Demo
```bash
python demo.py
```

### 4. Run Tests
```bash
python test_speed_detector.py
```

## Python API

```python
from speed_detector import SpeedSignDetector

# Initialize detector
detector = SpeedSignDetector()

# Detect speed limits in an image
detections = detector.detect_speed_limit("image.jpg")

for speed, (x, y, radius) in detections:
    print(f"Speed limit: {speed} km/h at position ({x}, {y})")

# Save annotated image
detector.draw_detections("image.jpg", "output.jpg")
```

## Features

✅ Circular speed sign detection using computer vision  
✅ OCR-based speed limit recognition  
✅ Real-time video processing  
✅ Webcam support  
✅ Multi-method preprocessing for robust detection  
✅ Cross-platform support (Windows, macOS, Linux)  

## System Requirements

- Python 3.7+
- OpenCV 4.8.1.78+
- Tesseract OCR 5.0+
- NumPy 1.24.0+
- Pillow 12.1.1+
- pytesseract 0.3.10+

## Troubleshooting

**Issue**: "tesseract: command not found"  
**Solution**: Install Tesseract OCR for your operating system

**Issue**: No speed signs detected  
**Solution**: Ensure images are clear and speed signs are visible and not obscured

**Issue**: Wrong speed detected  
**Solution**: The OCR may misread numbers in low-quality images. Try with higher resolution images

## Support

For issues or feature requests, please check the README.md for more details.
