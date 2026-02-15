#!/usr/bin/env python3
"""
Test script for Speed Sign Detection AI
"""

import numpy as np
import cv2
from speed_detector import SpeedSignDetector
import os


def create_test_image():
    """Create a simple test image with a speed limit sign."""
    # Create a white background
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw a red circle (speed limit sign border)
    center = (200, 200)
    radius = 80
    cv2.circle(img, center, radius, (0, 0, 255), 8)
    
    # Add white circle inside
    cv2.circle(img, center, radius - 10, (255, 255, 255), -1)
    
    # Add red circle again for border
    cv2.circle(img, center, radius, (0, 0, 255), 8)
    
    # Add speed text "50"
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "50"
    text_size = cv2.getTextSize(text, font, 3, 8)[0]
    text_x = center[0] - text_size[0] // 2
    text_y = center[1] + text_size[1] // 2
    cv2.putText(img, text, (text_x, text_y), font, 3, (0, 0, 0), 8)
    
    return img


def test_basic_detection():
    """Test basic speed sign detection."""
    print("=" * 60)
    print("Test 1: Basic Speed Sign Detection")
    print("=" * 60)
    
    # Create test image
    test_img = create_test_image()
    test_path = "/tmp/test_speed_sign.jpg"
    cv2.imwrite(test_path, test_img)
    print(f"Created test image at {test_path}")
    
    # Test detection
    detector = SpeedSignDetector()
    detections = detector.detect_speed_limit(test_path)
    
    print(f"\nDetections: {len(detections)}")
    for speed, (x, y, r) in detections:
        print(f"  - Speed: {speed} km/h at position ({x}, {y}) with radius {r}")
    
    # Draw detections
    output_path = "/tmp/test_output.jpg"
    detector.draw_detections(test_path, output_path)
    print(f"\nAnnotated output saved to {output_path}")
    
    if detections:
        print("✓ Test PASSED: Speed sign detected")
        return True
    else:
        print("✗ Test FAILED: No speed sign detected")
        return False


def test_preprocessing():
    """Test image preprocessing."""
    print("\n" + "=" * 60)
    print("Test 2: Image Preprocessing")
    print("=" * 60)
    
    test_img = create_test_image()
    detector = SpeedSignDetector()
    
    preprocessed = detector.preprocess_image(test_img)
    
    print(f"Original image shape: {test_img.shape}")
    print(f"Preprocessed image shape: {preprocessed.shape}")
    print(f"Preprocessed image dtype: {preprocessed.dtype}")
    
    if preprocessed.shape[0] == test_img.shape[0] and preprocessed.shape[1] == test_img.shape[1]:
        print("✓ Test PASSED: Preprocessing maintains image dimensions")
        return True
    else:
        print("✗ Test FAILED: Preprocessing changed image dimensions")
        return False


def test_circular_detection():
    """Test circular shape detection."""
    print("\n" + "=" * 60)
    print("Test 3: Circular Shape Detection")
    print("=" * 60)
    
    test_img = create_test_image()
    detector = SpeedSignDetector()
    
    circles = detector.detect_circular_signs(test_img)
    
    print(f"Detected {len(circles)} circular shape(s)")
    for x, y, r in circles:
        print(f"  - Circle at ({x}, {y}) with radius {r}")
    
    if len(circles) > 0:
        print("✓ Test PASSED: Circular shape detected")
        return True
    else:
        print("✗ Test FAILED: No circular shape detected")
        return False


def test_red_detection():
    """Test red region detection."""
    print("\n" + "=" * 60)
    print("Test 4: Red Region Detection")
    print("=" * 60)
    
    test_img = create_test_image()
    detector = SpeedSignDetector()
    
    red_mask = detector.detect_red_regions(test_img)
    red_pixels = np.sum(red_mask > 0)
    
    print(f"Detected {red_pixels} red pixels")
    
    if red_pixels > 1000:  # Should detect the red circle
        print("✓ Test PASSED: Red regions detected")
        return True
    else:
        print("✗ Test FAILED: No red regions detected")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SPEED SIGN DETECTION AI - TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_preprocessing,
        test_circular_detection,
        test_red_detection,
        test_basic_detection,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test FAILED with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All tests PASSED!")
    else:
        print("\n⚠️  Some tests FAILED")
    
    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
