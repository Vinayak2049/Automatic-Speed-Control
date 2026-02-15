"""
Speed Limit Sign Detection AI
This module detects and recognizes speed limit signs from images or video streams.
"""

import cv2
import numpy as np
import pytesseract
from typing import List, Tuple, Optional
import re


class SpeedSignDetector:
    """
    AI-based speed limit sign detector that can identify and read speed limit values
    from images using computer vision and OCR techniques.
    """
    
    # Configuration constants
    MIN_SPEED_LIMIT = 10  # Minimum valid speed limit (km/h)
    MAX_SPEED_LIMIT = 150  # Maximum valid speed limit (km/h)
    
    def __init__(self):
        """Initialize the speed sign detector with default parameters."""
        self.speed_pattern = re.compile(r'\b(\d{2,3})\b')
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the image for better detection.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Preprocessed grayscale image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def detect_circular_signs(self, image: np.ndarray) -> List[Tuple[int, int, int]]:
        """
        Detect circular shapes that could be speed limit signs.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            List of circles as (x, y, radius) tuples
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Use HoughCircles to detect circular shapes
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=100,
            param2=30,
            minRadius=20,
            maxRadius=200
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            return [(x, y, r) for x, y, r in circles[0, :]]
        
        return []
    
    def detect_red_regions(self, image: np.ndarray) -> np.ndarray:
        """
        Detect red regions in the image (speed signs often have red borders).
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Binary mask of red regions
        """
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for red color (red appears in two ranges in HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        # Create masks for both red ranges
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        
        # Combine both masks
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        return red_mask
    
    def extract_speed_from_roi(self, roi: np.ndarray) -> Optional[int]:
        """
        Extract speed limit value from a region of interest using OCR.
        
        Args:
            roi: Region of interest containing potential speed limit number
            
        Returns:
            Detected speed limit value or None if not found
        """
        # Preprocess ROI for better OCR
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) if len(roi.shape) == 3 else roi
        
        # Try multiple preprocessing approaches
        speed_candidates = []
        
        # Method 1: Simple thresholding
        _, thresh_roi1 = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        enlarged1 = cv2.resize(thresh_roi1, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        # Method 2: Inverted thresholding
        _, thresh_roi2 = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        enlarged2 = cv2.resize(thresh_roi2, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        # Method 3: Adaptive thresholding
        thresh_roi3 = cv2.adaptiveThreshold(gray_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
        enlarged3 = cv2.resize(thresh_roi3, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        # Try OCR on all methods
        for enlarged in [enlarged1, enlarged2, enlarged3]:
            try:
                # Try different PSM modes
                for psm in [7, 8, 10, 13]:
                    text = pytesseract.image_to_string(
                        enlarged, 
                        config=f'--psm {psm} -c tesseract_char_whitelist=0123456789'
                    )
                    
                    # Find speed limit values (typically 20-150)
                    matches = self.speed_pattern.findall(text)
                    
                    for match in matches:
                        speed = int(match)
                        if self.MIN_SPEED_LIMIT <= speed <= self.MAX_SPEED_LIMIT:
                            speed_candidates.append(speed)
                            
            except Exception:
                continue
        
        # Return most common speed if found
        if speed_candidates:
            from collections import Counter
            most_common = Counter(speed_candidates).most_common(1)[0][0]
            return most_common
            
        return None
    
    def detect_speed_limit(self, image_path: str) -> List[Tuple[int, Tuple[int, int, int]]]:
        """
        Detect speed limit signs in an image and return the detected speeds.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            List of (speed_limit, (x, y, radius)) tuples for each detected sign
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        results = []
        
        # Detect circular signs
        circles = self.detect_circular_signs(image)
        
        # Process each detected circle
        for x, y, r in circles:
            # Extract ROI around the circle
            margin = int(r * 0.3)
            y1 = max(0, y - r - margin)
            y2 = min(image.shape[0], y + r + margin)
            x1 = max(0, x - r - margin)
            x2 = min(image.shape[1], x + r + margin)
            
            roi = image[y1:y2, x1:x2]
            
            # Extract speed from ROI
            speed = self.extract_speed_from_roi(roi)
            
            if speed is not None:
                results.append((speed, (x, y, r)))
        
        return results
    
    def draw_detections(self, image_path: str, output_path: str) -> None:
        """
        Draw detected speed signs on the image and save the result.
        
        Args:
            image_path: Path to the input image
            output_path: Path to save the annotated image
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        detections = self.detect_speed_limit(image_path)
        
        for speed, (x, y, r) in detections:
            # Draw circle
            cv2.circle(image, (x, y), r, (0, 255, 0), 3)
            
            # Draw speed text
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{speed} km/h"
            cv2.putText(image, text, (x - r, y - r - 10), 
                       font, 1, (0, 255, 0), 2)
        
        cv2.imwrite(output_path, image)
        print(f"Annotated image saved to {output_path}")


def main():
    """Main function to demonstrate speed limit detection."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python speed_detector.py <image_path> [output_path]")
        print("Example: python speed_detector.py test_image.jpg output.jpg")
        return
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output_detected.jpg"
    
    detector = SpeedSignDetector()
    
    print(f"Processing image: {image_path}")
    detections = detector.detect_speed_limit(image_path)
    
    if detections:
        print(f"\nDetected {len(detections)} speed limit sign(s):")
        for speed, (x, y, r) in detections:
            print(f"  - Speed Limit: {speed} km/h at position ({x}, {y})")
        
        # Draw and save results
        detector.draw_detections(image_path, output_path)
    else:
        print("No speed limit signs detected in the image.")


if __name__ == "__main__":
    main()
