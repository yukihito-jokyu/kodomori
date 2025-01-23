import queue
import time
from collections import defaultdict
from typing import Any, Optional, Tuple

import numpy as np
from numpy.typing import NDArray


class FrameBuffer:
    """
    Buffer for managing camera frames and tracking results with motion prediction capabilities.

    This class provides a thread-safe queue for managing camera frames and tracking results,
    along with position history tracking and motion prediction functionality.

    Attributes:
        frame_queue (Queue): Thread-safe queue for storing camera frames
        latest_result: Most recent tracking result
        position_history (defaultdict): Track position history for motion prediction
        max_history (int): Maximum number of historical positions to keep per track
    """

    def __init__(self, maxsize: int = 2, max_history: int = 2):
        """
        Initialize frame buffer with specified capacity.

        Args:
            maxsize (int, optional): Maximum size of frame queue. Defaults to 32.
            max_history (int, optional): Maximum positions to keep per track. Defaults to 10.

        Example:
            >>> buffer = FrameBuffer(maxsize=64, max_history=15)
        """
        self.frame_queue = queue.Queue(maxsize=maxsize)
        self.latest_result = None
        self.position_history = defaultdict(list)
        self.max_history = max_history

        # 追加
        self.result_frame_queue = queue.Queue(maxsize=maxsize)

    def predict_next_position(
        self, track_id: int, current_pos: Tuple[float, float], current_time: float
    ) -> Tuple[float, float]:
        """
        Predict next position based on tracking history using velocity-based prediction.

        Args:
            track_id (int): Identifier for tracked object
            current_pos (Tuple[float, float]): Current position (x, y)
            current_time (float): Current timestamp

        Returns:
            Tuple[float, float]: Predicted (x, y) position

        Example:
            >>> buffer = FrameBuffer()
            >>> buffer.update_position_history(1, (100, 100), 0.0)
            >>> buffer.update_position_history(1, (110, 110), 0.1)
            >>> next_pos = buffer.predict_next_position(1, (120, 120), 0.2)
        """
        history = self.position_history[track_id]
        if len(history) < 2:
            return current_pos

        last_pos, last_time = history[-1]
        dt = current_time - last_time

        # Avoid division by very small numbers
        if dt < 0.0001:
            return current_pos

        # Calculate velocity vector
        velocity_x = (current_pos[0] - last_pos[0]) / dt
        velocity_y = (current_pos[1] - last_pos[1]) / dt

        # Adaptive look-ahead based on velocity magnitude
        magnitude = np.sqrt(velocity_x**2 + velocity_y**2)
        look_ahead = min(max(magnitude / 100, 0.1), 2.0)  # between 0.1 and 2 seconds

        # Predict future position
        next_x = current_pos[0] + velocity_x * look_ahead
        next_y = current_pos[1] + velocity_y * look_ahead

        return (next_x, next_y)

    def put_frame(self, frame: NDArray) -> None:
        """
        Add new frame to buffer, dropping oldest if full.

        Args:
            frame (NDArray): Camera frame to buffer

        Example:
            >>> import numpy as np
            >>> buffer = FrameBuffer()
            >>> frame = np.zeros((480, 640, 3), dtype=np.uint8)
            >>> buffer.put_frame(frame)
        """
        if self.frame_queue.full():
            try:
                self.frame_queue.get_nowait()
            except queue.Empty:
                pass
        self.frame_queue.put(frame)

    def get_frame(self) -> Optional[NDArray]:
        """
        Get next frame from buffer.

        Returns:
            Optional[NDArray]: Frame if available, None otherwise

        Example:
            >>> buffer = FrameBuffer()
            >>> frame = buffer.get_frame()
            >>> if frame is not None:
            ...     process_frame(frame)
        """
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

    def put_result_frame(self, frame: NDArray) -> None:
        """
        文字表示後のフレームをqueueに保存する

        Args:
            frame (NDArray): _description_
        """
        if self.result_frame_queue.full():
            try:
                self.result_frame_queue.get_nowait()
            except queue.Empty:
                pass
        self.result_frame_queue.put(frame)

    def get_result_frame(self) -> Optional[NDArray]:
        """
        文字表示後のフレームをqueueから取得する

        Returns:
            Optional[NDArray]: _description_
        """
        try:
            return self.result_frame_queue.get_nowait()
        except queue.Empty:
            return None

    def put_result(self, result: Any) -> None:
        """
        Update latest tracking result.

        Args:
            result (Any): YOLO tracking result

        Example:
            >>> buffer = FrameBuffer()
            >>> # Assuming 'results' is from YOLO model
            >>> buffer.put_result(results)
        """
        self.latest_result = result

    def get_result(self) -> Any:
        """
        Get latest tracking result.

        Returns:
            Any: Latest YOLO tracking result

        Example:
            >>> buffer = FrameBuffer()
            >>> results = buffer.get_result()
            >>> if results is not None:
            ...     process_results(results)
        """
        return self.latest_result

    def update_position_history(
        self, track_id: int, position: Tuple[float, float], timestamp: float
    ) -> None:
        """
        Update position history for a tracked object.

        Args:
            track_id (int): Identifier for tracked object
            position (Tuple[float, float]): (x, y) position
            timestamp (float): Current time

        Example:
            >>> buffer = FrameBuffer()
            >>> buffer.update_position_history(1, (100, 100), time.time())
        """
        history = self.position_history[track_id]
        history.append((position, timestamp))

        # Keep only recent history
        if len(history) > self.max_history:
            history.pop(0)

    def clean_old_tracks(self, current_time: float, max_age: float = 2.0) -> None:
        """
        Remove tracking history for objects not seen recently.

        Args:
            current_time (float): Current timestamp
            max_age (float, optional): Maximum age in seconds before dropping track.
                                     Defaults to 2.0.

        Example:
            >>> buffer = FrameBuffer()
            >>> # After some tracking...
            >>> buffer.clean_old_tracks(time.time())
        """
        for track_id in list(self.position_history.keys()):
            history = self.position_history[track_id]
            if history and (current_time - history[-1][1]) > max_age:
                del self.position_history[track_id]


# Usage example
if __name__ == "__main__":
    # Create a frame buffer
    buffer = FrameBuffer(maxsize=32, max_history=10)

    # Simulate frame processing
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    buffer.put_frame(frame)

    # Simulate tracking
    current_time = time.time()
    buffer.update_position_history(1, (100, 100), current_time)
    buffer.update_position_history(1, (110, 110), current_time + 0.1)

    # Test prediction
    next_pos = buffer.predict_next_position(1, (120, 120), current_time + 0.2)
    print(f"Predicted next position: {next_pos}")

    # Clean up old tracks
    buffer.clean_old_tracks(current_time + 3.0)
