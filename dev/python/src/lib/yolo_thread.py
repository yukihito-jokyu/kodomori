import threading
import time

from ultralytics import YOLO

from .frame_buffer import FrameBuffer


class YOLOThread(threading.Thread):
    """
    Thread-based YOLO object detection and tracking implementation.

    This class manages a separate thread for running YOLO object detection
    and tracking on frames from a FrameBuffer. It is designed to run
    continuously while minimizing CPU usage.

    Attributes:
        frame_buffer (FrameBuffer): Buffer containing frames to process
        running (bool): Thread control flag
        model (YOLO): YOLO model instance for detection/tracking

    Example:
        >>> buffer = FrameBuffer()
        >>> yolo_thread = YOLOThread(buffer)
        >>> yolo_thread.start()
        >>> # Thread will process frames as they become available
        >>> yolo_thread.running = False  # Stop thread
        >>> yolo_thread.join()
    """

    def __init__(self, frame_buffer: FrameBuffer, model_path: str = "yolov8n.pt"):
        """
        Initialize YOLO detection thread.

        Args:
            frame_buffer (FrameBuffer): Buffer to get frames from
            model_path (str, optional): Path to YOLO model weights.
                                      Defaults to 'yolov8n.pt'.

        Example:
            >>> buffer = FrameBuffer()
            >>> thread = YOLOThread(buffer, model_path='yolov8s.pt')
        """
        super().__init__()
        self.frame_buffer = frame_buffer
        self.running = True
        self.model = YOLO(model_path, verbose=False)

    def run(self) -> None:
        """
        Main thread execution loop.

        Continuously processes frames from the frame buffer using YOLO
        detection and tracking. Results are stored back in the frame buffer.

        The thread will sleep briefly between iterations to prevent
        excessive CPU usage.

        Example:
            >>> thread.start()  # Starts the run loop
        """
        while self.running:
            frame = self.frame_buffer.get_frame()
            if frame is not None:
                # Run detection and tracking on people only (class 0)
                results = self.model.track(
                    frame,
                    persist=True,  # Enable tracking
                    classes=[0],  # Track people only
                    verbose=False,  # Suppress progress output
                )
                self.frame_buffer.put_result(results)
            time.sleep(0.001)  # Prevent thread from hogging CPU

    def stop(self) -> None:
        """
        Stop the detection thread gracefully.

        Sets the running flag to False, allowing the thread to complete
        its current iteration and exit.

        Example:
            >>> thread.stop()
            >>> thread.join()
        """
        self.running = False


# Usage example
if __name__ == "__main__":
    # Create frame buffer and YOLO thread
    buffer = FrameBuffer()
    detector = YOLOThread(buffer, model_path="yolov8n.pt")

    # Start detection
    detector.start()

    try:
        while True:
            # Simulate frame processing
            results = buffer.get_result()
            if results is not None:
                # Process detection results
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()

                for box, track_id in zip(boxes, track_ids):
                    print(f"Detected person {track_id} at position {box[:2]}")

            time.sleep(0.1)  # Simulate frame rate

    except KeyboardInterrupt:
        # Clean shutdown
        detector.stop()
        detector.join()
