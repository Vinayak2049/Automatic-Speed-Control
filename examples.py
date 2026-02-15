#!/usr/bin/env python3
"""
Simple Usage Examples for Speed Sensing AI

This file demonstrates the most common use cases for the Speed Sensing AI system.
Copy and modify these examples for your own projects.
"""

# Example 1: Basic Image Detection
# ==================================
def example_detect_from_image():
    """Detect speed limit from a single image."""
    from speed_detector import SpeedSignDetector
    
    # Create detector
    detector = SpeedSignDetector()
    
    # Detect speed limits
    detections = detector.detect_speed_limit("traffic_sign.jpg")
    
    # Print results
    if detections:
        print("✓ Speed signs detected:")
        for speed, (x, y, radius) in detections:
            print(f"  - {speed} km/h at position ({x}, {y})")
    else:
        print("✗ No speed signs found")
    
    # Save annotated image
    detector.draw_detections("traffic_sign.jpg", "output.jpg")
    print("Annotated image saved to output.jpg")


# Example 2: Process Multiple Images
# ===================================
def example_batch_processing():
    """Process multiple images in a folder."""
    from speed_detector import SpeedSignDetector
    import glob
    
    detector = SpeedSignDetector()
    
    # Find all images
    image_files = glob.glob("images/*.jpg")
    
    results = {}
    for image_path in image_files:
        detections = detector.detect_speed_limit(image_path)
        results[image_path] = detections
        
        # Save annotated version
        output_path = image_path.replace(".jpg", "_detected.jpg")
        detector.draw_detections(image_path, output_path)
    
    # Print summary
    print(f"Processed {len(image_files)} images")
    total_detections = sum(len(d) for d in results.values())
    print(f"Found {total_detections} speed signs total")


# Example 3: Video Processing
# ============================
def example_video_processing():
    """Process a video file and detect speed signs."""
    from video_speed_detector import VideoSpeedDetector
    
    detector = VideoSpeedDetector()
    
    # Process video (press 'q' to quit early)
    detector.process_video("traffic_video.mp4", "output_video.mp4")
    
    print("Video processing complete!")


# Example 4: Webcam Detection
# ============================
def example_webcam():
    """Use webcam for real-time speed sign detection."""
    from video_speed_detector import VideoSpeedDetector
    
    detector = VideoSpeedDetector()
    
    print("Starting webcam detection...")
    print("Press 'q' to quit")
    
    # Use webcam (device 0)
    detector.process_video("0")


# Example 5: Custom Speed Range
# ==============================
def example_custom_speed_range():
    """Detect speed signs with custom speed range."""
    from speed_detector import SpeedSignDetector
    
    detector = SpeedSignDetector()
    
    # Customize speed range for your region
    detector.MIN_SPEED_LIMIT = 20   # e.g., for urban areas only
    detector.MAX_SPEED_LIMIT = 100  # e.g., for country roads
    
    detections = detector.detect_speed_limit("sign.jpg")
    print(f"Detected {len(detections)} signs in range 20-100 km/h")


# Example 6: Get Detection Confidence
# ====================================
def example_with_details():
    """Get detailed information about each detection."""
    from speed_detector import SpeedSignDetector
    import cv2
    
    detector = SpeedSignDetector()
    
    # Load image to get dimensions
    image = cv2.imread("sign.jpg")
    height, width = image.shape[:2]
    
    detections = detector.detect_speed_limit("sign.jpg")
    
    for speed, (x, y, radius) in detections:
        print(f"Speed: {speed} km/h")
        print(f"  Center: ({x}, {y})")
        print(f"  Radius: {radius} pixels")
        print(f"  Position: {x/width:.1%} across, {y/height:.1%} down")
        print()


# Example 7: Error Handling
# ==========================
def example_with_error_handling():
    """Robust detection with proper error handling."""
    from speed_detector import SpeedSignDetector
    import os
    
    detector = SpeedSignDetector()
    
    image_path = "my_image.jpg"
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return
    
    try:
        detections = detector.detect_speed_limit(image_path)
        
        if detections:
            print(f"Success! Found {len(detections)} speed sign(s)")
            for speed, (x, y, r) in detections:
                print(f"  - {speed} km/h")
        else:
            print("No speed signs detected in image")
            
    except Exception as e:
        print(f"Error during detection: {e}")


# Example 8: Integration with Other Systems
# ==========================================
def example_api_integration():
    """Example of how to integrate with a web API or database."""
    from speed_detector import SpeedSignDetector
    import json
    from datetime import datetime
    
    detector = SpeedSignDetector()
    
    # Detect from image
    detections = detector.detect_speed_limit("sign.jpg")
    
    # Format results for API/database
    results = {
        "timestamp": datetime.now().isoformat(),
        "image_path": "sign.jpg",
        "detections_count": len(detections),
        "speed_limits": []
    }
    
    for speed, (x, y, radius) in detections:
        results["speed_limits"].append({
            "speed_kmh": speed,
            "position_x": int(x),
            "position_y": int(y),
            "radius_px": int(radius)
        })
    
    # Save as JSON
    with open("detection_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to detection_results.json")
    print(json.dumps(results, indent=2))


# Example 9: Performance Tuning
# ==============================
def example_performance_tuning():
    """Adjust frame skip rate for video processing performance."""
    from video_speed_detector import VideoSpeedDetector
    
    detector = VideoSpeedDetector()
    
    # Process more frames for better accuracy (slower)
    detector.FRAME_SKIP = 5
    
    # Or skip more frames for better performance (faster)
    # detector.FRAME_SKIP = 20
    
    detector.process_video("video.mp4", "output.mp4")


# Example 10: Testing Your Setup
# ===============================
def example_test_installation():
    """Test if everything is installed correctly."""
    print("Testing Speed Sensing AI installation...")
    print()
    
    # Test imports
    try:
        import cv2
        print("✓ OpenCV installed:", cv2.__version__)
    except ImportError:
        print("✗ OpenCV not installed")
        return False
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print("✓ Tesseract installed:", version)
    except Exception:
        print("✗ Tesseract not installed or not configured")
        return False
    
    try:
        from speed_detector import SpeedSignDetector
        print("✓ SpeedSignDetector available")
    except ImportError:
        print("✗ speed_detector.py not found")
        return False
    
    try:
        from video_speed_detector import VideoSpeedDetector
        print("✓ VideoSpeedDetector available")
    except ImportError:
        print("✗ video_speed_detector.py not found")
        return False
    
    print()
    print("🎉 All components installed successfully!")
    return True


# Main: Run examples
# ===================
if __name__ == "__main__":
    print("=" * 70)
    print("SPEED SENSING AI - USAGE EXAMPLES")
    print("=" * 70)
    print()
    print("Available examples:")
    print("  1. example_detect_from_image() - Basic image detection")
    print("  2. example_batch_processing() - Process multiple images")
    print("  3. example_video_processing() - Process video file")
    print("  4. example_webcam() - Real-time webcam detection")
    print("  5. example_custom_speed_range() - Custom speed limits")
    print("  6. example_with_details() - Detailed detection info")
    print("  7. example_with_error_handling() - Robust detection")
    print("  8. example_api_integration() - API/database integration")
    print("  9. example_performance_tuning() - Performance optimization")
    print(" 10. example_test_installation() - Test your setup")
    print()
    print("Running installation test...")
    print()
    
    # Test installation by default
    example_test_installation()
    
    print()
    print("To run other examples, edit this file and call them directly.")
    print("For example: example_detect_from_image()")
