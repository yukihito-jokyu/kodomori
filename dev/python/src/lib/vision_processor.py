from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from scipy.optimize import minimize


@dataclass
class ProcessedTrackingResult:
    """
    Contains processed tracking results after homography transformation

    Attributes:
        original_coord: Original coordinates in image space
        transformed_coord: Coordinates after homography transform
        track_id: Tracking identifier
        prediction: Predicted future position
        zones: List of zone indices the point is currently in
    """

    original_coord: Tuple[float, float]
    transformed_coord: Tuple[float, float]
    track_id: int
    prediction: Optional[Tuple[float, float]] = None
    zones: List[int] = None


class VisionProcessor:
    """
    Handles computer vision processing including homography, tracking, and zone detection.

    This class provides a complete processing pipeline for:
    - Computing homography transforms from point correspondences
    - Transforming tracked points into real-world coordinates
    - Predicting future positions
    - Detecting zone intersections

    Attributes:
        scale_factor (float): Scale factor for real-world coordinates (pixels per meter)
    """

    def __init__(self, scale_factor: float = 100):
        """
        Initialize vision processor with specified scale.

        Args:
            scale_factor (float): Pixels per meter scale. Defaults to 100.

        Example:
            >>> processor = VisionProcessor(scale_factor=150)
        """
        self.scale_factor = scale_factor
        self._matrix = None
        self._inverse_matrix = None
        self._output_dimensions = None

    def calculate_homography(
        self, points: List["Point"], distances: Dict[str, float]
    ) -> None:
        """
        Compute homography matrix from point correspondences and real-world distances.

        Args:
            points (List[Point]): Four points defining the homography
            distances (Dict[str, float]): Real-world distances between points

        Raises:
            ValueError: If not exactly 4 points provided or missing distances

        Example:
            >>> processor.calculate_homography(corner_points, measured_distances)
        """
        if len(points) != 4:
            raise ValueError("Exactly 4 points required for homography calculation")

        sorted_points = sorted(points, key=lambda x: x.id)
        src_points = np.float32([p.coord for p in sorted_points])
        dst_points = self._calculate_real_points(sorted_points, distances)

        # Scale to reasonable pixel dimensions
        scale = min(800 / np.max(dst_points[:, 0]), 800 / np.max(dst_points[:, 1]))
        dst_points = dst_points * scale

        # Center the points
        min_coords = [np.min(dst_points[:, 0]), np.min(dst_points[:, 1])]
        dst_points = dst_points - min_coords

        self._matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        self._inverse_matrix = cv2.getPerspectiveTransform(dst_points, src_points)
        self._output_dimensions = (
            int(np.max(dst_points[:, 0]) - np.min(dst_points[:, 0])),
            int(np.max(dst_points[:, 1]) - np.min(dst_points[:, 1])),
        )

    def process_tracking_result(
        self, track_data: Dict[str, Any], zones: List[List[Tuple[float, float]]]
    ) -> ProcessedTrackingResult:
        """
        Process a single tracking result with homography and zone detection.

        Args:
            track_data (Dict[str, Any]): Tracking data including coordinates and ID
            zones (List[List[Tuple[float, float]]]): List of polygon zones

        Returns:
            ProcessedTrackingResult: Processed tracking information

        Raises:
            ValueError: If homography matrix not computed

        Example:
            >>> result = processor.process_tracking_result(track_data, defined_zones)
        """
        if self._matrix is None:
            raise ValueError("Homography matrix not computed")

        # Transform coordinates
        src_pts = np.float32([[track_data["mapped"][0], track_data["mapped"][1]]])
        dst_pts = cv2.perspectiveTransform(src_pts.reshape(-1, 1, 2), self._matrix)
        transformed = tuple(dst_pts[0][0])

        # Process prediction if available
        prediction = None
        if "predicted" in track_data:
            pred_pts = np.float32(
                [[track_data["predicted"][0], track_data["predicted"][1]]]
            )
            pred_dst = cv2.perspectiveTransform(
                pred_pts.reshape(-1, 1, 2), self._matrix
            )
            prediction = tuple(pred_dst[0][0])

        # Check zone intersections
        active_zones = []
        for i, zone in enumerate(zones):
            if self._point_in_polygon(transformed, zone):
                active_zones.append(i)

        return ProcessedTrackingResult(
            original_coord=track_data["mapped"],
            transformed_coord=transformed,
            track_id=track_data["track_id"],
            prediction=prediction,
            zones=active_zones,
        )

    def transform_point(
        self, point: Tuple[float, float], inverse: bool = False
    ) -> Tuple[float, float]:
        """
        Transform a single point using homography matrix.

        Args:
            point (Tuple[float, float]): Point to transform
            inverse (bool): If True, use inverse transform. Defaults to False.

        Returns:
            Tuple[float, float]: Transformed point

        Raises:
            ValueError: If homography matrix not computed

        Example:
            >>> real_world_pos = processor.transform_point((100, 200))
        """
        if self._matrix is None:
            raise ValueError("Homography matrix not computed")

        matrix = self._inverse_matrix if inverse else self._matrix
        pts = np.float32([[point[0], point[1]]])
        transformed = cv2.perspectiveTransform(pts.reshape(-1, 1, 2), matrix)
        return tuple(transformed[0][0])

    def get_output_dimensions(self) -> Optional[Tuple[int, int]]:
        """
        Get dimensions of output space after homography.

        Returns:
            Optional[Tuple[int, int]]: (width, height) or None if not computed

        Example:
            >>> width, height = processor.get_output_dimensions()
        """
        return self._output_dimensions

    def _calculate_real_points(
        self, sorted_points: List["Point"], distances: Dict[str, float]
    ) -> np.ndarray:
        """
        Calculate real-world coordinates from distances using geometric optimization.

        Args:
            sorted_points (List[Point]): Ordered points
            distances (Dict[str, float]): Distance measurements

        Returns:
            np.ndarray: Real-world coordinates

        Raises:
            ValueError: If missing required distances
        """
        # Place first point at origin
        real_coords = [(0, 0)]

        # Second point on x-axis
        d01 = distances.get(f"{sorted_points[0].id}-{sorted_points[1].id}")

        if d01 is None:
            raise ValueError("Missing distance between points 0 and 1")
        real_coords.append((d01, 0))

        # Calculate third point using triangulation
        d12 = distances.get(f"{sorted_points[1].id}-{sorted_points[2].id}")
        d02 = distances.get(f"{sorted_points[0].id}-{sorted_points[2].id}")
        if None in (d12, d02):
            raise ValueError("Missing distances for point 3")

        x = (d02 * d02 - d12 * d12 + d01 * d01) / (2 * d01)
        y = np.sqrt(d02 * d02 - x * x)
        real_coords.append((x, y))

        # Optimize fourth point position
        d23 = distances.get(f"{sorted_points[2].id}-{sorted_points[3].id}")
        d03 = distances.get(f"{sorted_points[0].id}-{sorted_points[3].id}")
        d13 = distances.get(f"{sorted_points[1].id}-{sorted_points[3].id}")

        if None in (d23, d03, d13):
            raise ValueError("Missing distances for point 4")

        def error_func(point):
            px, py = point
            error = 0
            error += (np.sqrt(px * px + py * py) - d03) ** 2
            error += (np.sqrt((px - d01) ** 2 + py**2) - d13) ** 2
            error += (
                np.sqrt((px - real_coords[2][0]) ** 2 + (py - real_coords[2][1]) ** 2)
                - d23
            ) ** 2
            return error

        result = minimize(error_func, (d03 / 2, d03 / 2))
        real_coords.append((result.x[0], result.x[1]))

        return np.float32(real_coords)

    def _point_in_polygon(
        self, point: Tuple[float, float], polygon: List[Tuple[float, float]]
    ) -> bool:
        """
        Check if point lies within polygon using ray casting algorithm.

        Args:
            point (Tuple[float, float]): Point to check
            polygon (List[Tuple[float, float]]): Vertices of polygon

        Returns:
            bool: True if point is inside polygon

        Example:
            >>> inside = processor._point_in_polygon((10, 20), zone_vertices)
        """
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside


# Usage example
if __name__ == "__main__":
    # Create processor
    processor = VisionProcessor(scale_factor=100)

    # Example points and distances
    from point import Point

    points = [
        Point((0, 0), 0),
        Point((100, 0), 1),
        Point((100, 100), 2),
        Point((0, 100), 3),
    ]

    distances = {
        "0-1": 1.0,
        "1-2": 1.0,
        "2-3": 1.0,
        "3-0": 1.0,
        "0-2": 1.414,
        "1-3": 1.414,
        "0-3": 1.414,
    }

    # Calculate homography
    processor.calculate_homography(points, distances)

    # Example tracking result
    track_data = {"mapped": (50, 50), "track_id": 1, "predicted": (60, 60)}

    # Example zones
    zones = [[(0, 0), (50, 0), (50, 50), (0, 50)]]

    # Process tracking
    result = processor.process_tracking_result(track_data, zones)
    print(f"Processed result: {result}")
