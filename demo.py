#!/usr/bin/env python3
"""
Example usage script for Speed Sensing AI
Demonstrates various capabilities of the speed detection system.
"""

import cv2
import numpy as np
from speed_detector import SpeedSignDetector


def create_demo_images():
    """Create demonstration images with different speed limit signs."""
    signs = [
        ("demo_30.jpg", "30", 30),
        ("demo_50.jpg", "50", 50),
        ("demo_80.jpg", "80", 80),
        ("demo_100.jpg", "100", 100),
    ]
    
    print("Creating demonstration images...")
    
    for filename, text, speed in signs:
        # Create white background
        img = np.ones((500, 500, 3), dtype=np.uint8) * 255
        
        # Draw red circle (speed limit sign border)
        center = (250, 250)
        radius = 100
        cv2.circle(img, center, radius, (0, 0, 255), 12)
        
        # Add white circle inside
        cv2.circle(img, center, radius - 15, (255, 255, 255), -1)
        
        # Add red circle again for border
        cv2.circle(img, center, radius, (0, 0, 255), 12)
        
        # Add speed text
        font = cv2.FONT_HERSHEY_BOLD
        text_size = cv2.getTextSize(text, font, 2.5 if len(text) <= 2 else 2, 6)[0]
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] + text_size[1] // 2
        thickness = 6 if len(text) <= 2 else 5
        cv2.putText(img, text, (text_x, text_y), font, 2.5 if len(text) <= 2 else 2, 
                   (0, 0, 0), thickness)
        
        cv2.imwrite(filename, img)
        print(f"  ✓ Created {filename} - {speed} km/h sign")
    
    return [sign[0] for sign in signs]


def demo_image_detection():
    """Demonstrate speed detection on images."""
    print("\n" + "=" * 70)
    print("DEMO 1: Image-based Speed Limit Detection")
    print("=" * 70)
    
    # Create demo images
    image_files = create_demo_images()
    
    # Initialize detector
    detector = SpeedSignDetector()
    
    print("\nDetecting speed limits in demo images...")
    
    for image_file in image_files:
        print(f"\nProcessing: {image_file}")
        
        try:
            detections = detector.detect_speed_limit(image_file)
            
            if detections:
                for speed, (x, y, r) in detections:
                    print(f"  ✓ Detected: {speed} km/h at position ({x}, {y})")
                
                # Create annotated output
                output_file = f"output_{image_file}"
                detector.draw_detections(image_file, output_file)
                print(f"  ✓ Annotated image saved: {output_file}")
            else:
                print(f"  ✗ No speed limit detected")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")


def demo_multiple_signs():
    """Demonstrate detection of multiple speed signs in one image."""
    print("\n" + "=" * 70)
    print("DEMO 2: Multiple Speed Signs in One Image")
    print("=" * 70)
    
    # Create image with multiple signs
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    signs_data = [
        ((200, 300), 60, "50"),
        ((600, 300), 60, "80"),
    ]
    
    for center, radius, text in signs_data:
        # Draw red circle
        cv2.circle(img, center, radius, (0, 0, 255), 10)
        cv2.circle(img, center, radius - 12, (255, 255, 255), -1)
        cv2.circle(img, center, radius, (0, 0, 255), 10)
        
        # Add text
        font = cv2.FONT_HERSHEY_BOLD
        text_size = cv2.getTextSize(text, font, 2, 5)[0]
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] + text_size[1] // 2
        cv2.putText(img, text, (text_x, text_y), font, 2, (0, 0, 0), 5)
    
    filename = "demo_multiple.jpg"
    cv2.imwrite(filename, img)
    print(f"\nCreated image with multiple signs: {filename}")
    
    # Detect
    detector = SpeedSignDetector()
    detections = detector.detect_speed_limit(filename)
    
    print(f"\nDetected {len(detections)} speed sign(s):")
    for speed, (x, y, r) in detections:
        print(f"  - Speed: {speed} km/h at ({x}, {y})")
    
    output_file = "output_multiple.jpg"
    detector.draw_detections(filename, output_file)
    print(f"\nAnnotated image saved: {output_file}")


def print_system_info():
    """Print system information."""
    print("\n" + "=" * 70)
    print("System Information")
    print("=" * 70)
    
    import sys
    print(f"Python version: {sys.version}")
    
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError:
        print("OpenCV: Not installed")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
    except Exception:
        print("Tesseract: Not properly configured")
    
    try:
        import numpy as np
        print(f"NumPy version: {np.__version__}")
    except ImportError:
        print("NumPy: Not installed")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("SPEED SENSING AI - DEMONSTRATION SCRIPT")
    print("=" * 70)
    
    try:
        print_system_info()
        demo_image_detection()
        demo_multiple_signs()
        
        print("\n" + "=" * 70)
        print("✓ All demonstrations completed successfully!")
        print("=" * 70)
        print("\nGenerated files:")
        print("  - demo_30.jpg, demo_50.jpg, demo_80.jpg, demo_100.jpg")
        print("  - demo_multiple.jpg")
        print("  - output_*.jpg (annotated results)")
        print("\nYou can view these images to see the detection results.")
        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
