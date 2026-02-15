"""
Real-time Speed Limit Detection from Video
This module processes video streams to detect speed limit signs in real-time.
"""

import cv2
import tempfile
import os
from speed_detector import SpeedSignDetector
from typing import Optional


class VideoSpeedDetector:
    """
    Real-time speed limit sign detector for video streams.
    """
    
    # Configuration constants
    FRAME_SKIP = 10  # Process every Nth frame for better performance
    
    def __init__(self):
        """Initialize the video speed detector."""
        self.detector = SpeedSignDetector()
        self.current_speed_limit = None
        
    def process_video(self, video_path: str, output_path: Optional[str] = None) -> None:
        """
        Process a video file and detect speed limit signs.
        
        Args:
            video_path: Path to the input video file (or 0 for webcam)
            output_path: Optional path to save the output video
        """
        # Open video
        if video_path == "0":
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer if output path provided
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        
        print("Processing video... Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_count += 1
            
            # Process every FRAME_SKIP frames to improve performance
            if frame_count % self.FRAME_SKIP == 0:
                # Save frame temporarily using cross-platform temp file
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                    temp_path = tmp_file.name
                
                try:
                    cv2.imwrite(temp_path, frame)
                    
                    # Detect speed signs
                    detections = self.detector.detect_speed_limit(temp_path)
                    
                    if detections:
                        for speed, (x, y, r) in detections:
                            self.current_speed_limit = speed
                            # Draw detection on frame
                            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
                            cv2.putText(frame, f"{speed} km/h", (x - r, y - r - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error processing frame {frame_count}: {e}")
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            
            # Display current speed limit on frame
            if self.current_speed_limit:
                cv2.putText(frame, f"Current Speed Limit: {self.current_speed_limit} km/h",
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Write frame if output is enabled
            if writer:
                writer.write(frame)
            
            # Display frame
            cv2.imshow('Speed Limit Detection', frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        
        print(f"\nProcessed {frame_count} frames")
        if output_path:
            print(f"Output saved to {output_path}")


def main():
    """Main function for video speed detection."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python video_speed_detector.py <video_path|0> [output_path]")
        print("  video_path: Path to video file or '0' for webcam")
        print("  output_path: Optional path to save output video")
        print("\nExample: python video_speed_detector.py traffic.mp4 output.mp4")
        print("Example: python video_speed_detector.py 0  # Use webcam")
        return
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    detector = VideoSpeedDetector()
    detector.process_video(video_path, output_path)


if __name__ == "__main__":
    main()
