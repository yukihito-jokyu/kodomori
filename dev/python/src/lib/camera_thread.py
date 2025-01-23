import json
import os
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import cv2
import numpy as np

from .frame_buffer import FrameBuffer
from .point import Point
from .yolo_thread import YOLOThread


class CameraThread(threading.Thread):
    """
    Thread-based camera capture and processing implementation with homography setup.

    This class manages camera capture, frame processing, object tracking,
    and homography point selection in a separate thread. It provides callbacks
    for frame updates and coordinate mapping.

    Attributes:
        frame_buffer (FrameBuffer): Buffer for frame processing
        frame_callback (Callable): Callback for processed frames
        mapping_callback (Optional[Callable]): Callback for coordinate mapping
        running (bool): Thread control flag
        points (List[Point]): Homography reference points

    Example:
        >>> def on_frame(frame, results):
        ...     process_frame(frame)
        >>> camera = CameraThread(
        ...     frame_callback=on_frame,
        ...     camera_id=0
        ... )
        >>> camera.start()
        >>> # Camera will process frames until stopped
        >>> camera.stop()
        >>> camera.join()
    """

    def __init__(
        self,
        frame_callback: Callable[[np.ndarray, Optional[Any]], None],
        mapping_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        camera_id: int = 0,
        model_path: str = "yolov8n.pt",
        save_file: str = "homography_data.json",
    ):
        """
        Initialize camera thread with callbacks and configuration.

        Args:
            frame_callback: Called with (frame, results) for each processed frame
            mapping_callback: Optional callback for coordinate mapping updates
            camera_id: Camera device ID (default: 0)
            model_path: Path to YOLO model weights (default: 'yolov8n.pt')
            save_file: Path to save homography data (default: 'homography_data.json')
        """
        super().__init__()
        self.frame_callback = frame_callback
        self.mapping_callback = mapping_callback
        self.camera_id = camera_id
        self.save_file = save_file
        self.running = True

        # Point management
        self.points = []
        self.selected_point = None
        self.point_counter = 0
        self.max_points = 4

        # Colors
        self.point_color = (0, 0, 255)  # Red
        self.selected_color = (0, 255, 0)  # Green

        # Initialize frame buffer and YOLO thread
        self.frame_buffer = FrameBuffer()
        self.yolo_thread = YOLOThread(
            frame_buffer=self.frame_buffer, model_path=model_path
        )
        self.yolo_thread.daemon = True

        # Performance monitoring
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.fps = 0

        # Load saved data
        self.load_data()

    def load_data(self) -> None:
        """Load saved homography points from file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.points = [
                        Point.from_dict(point_data)
                        for point_data in data.get("points", [])
                    ]
                    if self.points:
                        self.point_counter = max(point.id for point in self.points)
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self) -> None:
        """Save homography points to file."""
        data = {"points": [point.to_dict() for point in self.points]}
        with open(self.save_file, "w") as f:
            json.dump(data, f)

    def mouse_callback(
        self, event: int, x: int, y: int, flags: int, param: Any
    ) -> None:
        """
        Handle mouse events for point selection.

        Args:
            event: OpenCV mouse event type
            x: Mouse x coordinate
            y: Mouse y coordinate
            flags: Event flags
            param: Additional parameters
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < self.max_points:
                # Add new point
                self.point_counter += 1
                new_point = Point(
                    coord=(x, y), id=self.point_counter, color=self.point_color
                )
                self.points.append(new_point)
                self.save_data()
            else:
                # Select existing point
                for point in self.points:
                    if point.is_near(x, y):
                        if self.selected_point == point:
                            self.selected_point = None
                            point.selected = False
                        else:
                            if self.selected_point:
                                self.selected_point.selected = False
                            self.selected_point = point
                            point.selected = True
                        self.save_data()
                        break

    def calculate_fps(self) -> None:
        """Update FPS calculation every 30 frames."""
        self.fps_counter += 1
        if self.fps_counter % 30 == 0:
            current_time = time.time()
            self.fps = 30 / (current_time - self.fps_start_time)
            self.fps_start_time = current_time

    def process_tracking_results(
        self, frame: np.ndarray, results: Any
    ) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Process YOLO tracking results and update frame visualization.

        Args:
            frame: Input frame to process
            results: YOLO tracking results

        Returns:
            Tuple containing:
                - Processed frame with visualizations
                - List of tracking data dictionaries
        """
        draw_frame = frame.copy()
        tracking_data = []

        if results is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            current_time = time.time()

            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box

                # Calculate bottom center
                bottom_center_x = x
                bottom_center_y = y + h / 2
                current_pos = (float(bottom_center_x), float(bottom_center_y))

                # Update position history
                self.frame_buffer.update_position_history(
                    track_id, current_pos, current_time
                )

                # Get prediction
                next_pos = self.frame_buffer.predict_next_position(
                    track_id, current_pos, current_time
                )

                # Draw tracking visualization
                cv2.rectangle(
                    draw_frame,
                    (int(x - w / 2), int(y - h / 2)),
                    (int(x + w / 2), int(y + h / 2)),
                    (0, 255, 0),
                    2,
                )

                cv2.arrowedLine(
                    draw_frame,
                    (int(bottom_center_x), int(bottom_center_y)),
                    (int(next_pos[0]), int(next_pos[1])),
                    (0, 0, 255),
                    2,
                )

                cv2.putText(
                    draw_frame,
                    f"ID: {track_id}",
                    (int(x - w / 2), int(y - h / 2) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

                # Collect tracking data
                tracking_data.append(
                    {
                        "coord": (float(x), float(y)),
                        "mapped": (float(bottom_center_x), float(bottom_center_y)),
                        "track_id": track_id,
                        "size": (float(w), float(h)),
                    }
                )

        # Draw homography points
        for point in self.points:
            color = self.selected_color if point.selected else point.color
            cv2.circle(draw_frame, point.coord, 5, color, -1)
            cv2.putText(
                draw_frame,
                f"P{point.id}",
                (point.coord[0] + 10, point.coord[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

        # Draw points left instruction
        points_left = self.max_points - len(self.points)
        if points_left > 0:
            cv2.putText(
                draw_frame,
                f"Select {points_left} more points",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                self.point_color,
                2,
            )

        return draw_frame, tracking_data

    def set_point(self, points: List[Point]) -> None:
        """_summary_

        Args:
            points (List[Any]): _description_
        """

        # 初期化
        self.points = []

        for p in points:
            new_point = Point(
                coord=(p.coord[0], p.coord[1]),
                id=p.id,
                color=p.color,
            )
            self.points.append(new_point)
            self.save_data()

    def run(self) -> None:
        """Main camera capture and processing loop."""
        # Start YOLO thread
        self.yolo_thread.start()

        # Initialize camera
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print(f"Cannot access camera {self.camera_id}")
            return

        # Setup display window
        cv2.namedWindow("Homography Setup")
        cv2.setMouseCallback("Homography Setup", self.mouse_callback)

        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Update FPS
                self.calculate_fps()

                # Process frame
                self.frame_buffer.put_frame(frame.copy())
                results = self.frame_buffer.get_result()

                # Process tracking results
                processed_frame, tracking_data = self.process_tracking_results(
                    frame, results
                )

                # Draw FPS
                cv2.putText(
                    processed_frame,
                    f"FPS: {self.fps:.1f}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )

                # 文字を表示したframeを保存する
                self.frame_buffer.put_result_frame(processed_frame.copy())

                # Show frame
                cv2.imshow("Homography Setup", processed_frame)

                # Handle callbacks
                try:
                    self.frame_callback(frame, results)
                    if self.mapping_callback:
                        for data in tracking_data:
                            self.mapping_callback(data)
                except Exception as e:
                    print(f"Error in callbacks: {e}")

                # Handle key events
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("c"):
                    self.points = []
                    self.selected_point = None
                    self.point_counter = 0
                    self.save_data()
                elif key == ord("p") and self.selected_point:
                    self.points.remove(self.selected_point)
                    self.selected_point = None
                    self.save_data()

        finally:
            # Cleanup
            self.yolo_thread.stop()
            self.yolo_thread.join()
            cap.release()
            cv2.destroyAllWindows()

    def stop(self) -> None:
        """Stop camera capture thread gracefully."""
        self.running = False
        if self.yolo_thread.is_alive():
            self.yolo_thread.stop()


# Usage example
if __name__ == "__main__":

    def frame_handler(frame, results):
        pass  # Just for demonstration

    # Create and start camera thread
    camera = CameraThread(frame_handler)
    camera.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        camera.stop()
        camera.join()
