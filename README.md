# Speed Sensing AI

An intelligent AI system for detecting and recognizing speed limit signs from images and video streams using computer vision and OCR techniques.

## Features

- 🚦 **Speed Limit Sign Detection**: Automatically detects circular speed limit signs
- 🔍 **OCR-based Recognition**: Reads speed limit values using OCR technology
- 📷 **Image Processing**: Processes static images to find speed limit signs
- 🎥 **Video Support**: Real-time detection from video files and webcam streams
- 🎨 **Visual Output**: Annotates detected signs with bounding circles and speed values
- 🔴 **Color-based Detection**: Uses red color detection to improve accuracy

## Installation

### Prerequisites

- Python 3.7 or higher
- Tesseract OCR engine

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Detect Speed Limits in Images

```bash
python speed_detector.py <image_path> [output_path]
```

**Example:**
```bash
python speed_detector.py traffic_sign.jpg detected_output.jpg
```

### 2. Real-time Video Detection

```bash
python video_speed_detector.py <video_path|0> [output_path]
```

**Examples:**
```bash
# Process a video file
python video_speed_detector.py traffic_video.mp4 output_video.mp4

# Use webcam (press 'q' to quit)
python video_speed_detector.py 0
```

### 3. Run Tests

```bash
python test_speed_detector.py
```

## How It Works

### Detection Pipeline

1. **Image Preprocessing**
   - Convert to grayscale
   - Apply Gaussian blur for noise reduction
   - Adaptive thresholding for better contrast

2. **Sign Detection**
   - Circular shape detection using Hough Circle Transform
   - Red color detection (speed signs typically have red borders)
   - Region of Interest (ROI) extraction

3. **Speed Recognition**
   - OCR processing on detected ROIs
   - Pattern matching for speed values (10-150 km/h range)
   - Validation of reasonable speed limit values

4. **Visualization**
   - Draw bounding circles around detected signs
   - Annotate with detected speed values
   - Save or display results

## Architecture

```
speed_detector.py         # Core detection module for images
video_speed_detector.py   # Real-time video processing module
test_speed_detector.py    # Comprehensive test suite
requirements.txt          # Python dependencies
```

## API Reference

### SpeedSignDetector Class

Main class for speed limit sign detection.

#### Methods

- `detect_speed_limit(image_path: str)`: Detect speed signs in an image
- `draw_detections(image_path: str, output_path: str)`: Visualize detections
- `preprocess_image(image: np.ndarray)`: Preprocess image for detection
- `detect_circular_signs(image: np.ndarray)`: Find circular shapes
- `detect_red_regions(image: np.ndarray)`: Detect red-colored areas
- `extract_speed_from_roi(roi: np.ndarray)`: Extract speed value using OCR

### VideoSpeedDetector Class

Class for processing video streams.

#### Methods

- `process_video(video_path: str, output_path: str)`: Process video and detect signs

## Configuration

The detector can be customized by modifying parameters in the code:

- **Hough Circle Parameters**: Adjust sensitivity for circle detection
- **OCR Config**: Customize Tesseract settings for better recognition
- **Color Ranges**: Modify HSV ranges for red color detection
- **Speed Range**: Change valid speed limit range (default: 10-150 km/h)

## Limitations

- Works best with clear, front-facing images of speed limit signs
- Performance depends on image quality and lighting conditions
- Requires Tesseract OCR to be properly installed
- May have difficulty with partially obscured or damaged signs
- Designed primarily for circular speed limit signs

## Future Enhancements

- Support for different sign shapes (rectangular, diamond, etc.)
- Multi-language support for different countries
- Deep learning-based detection for improved accuracy
- Speed limit change tracking over time
- Integration with GPS for location-aware detection

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available for educational and research purposes.

## Author

Created as part of the Speed Sensing AI project.