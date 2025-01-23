from dataclasses import dataclass
from typing import Any, Dict, Tuple

import numpy as np


@dataclass
class Point:
    """
    Represents a 2D point with additional metadata for tracking and visualization.

    This class is designed for computer vision applications, particularly for
    homography calculations and point tracking.

    Attributes:
        coord (Tuple[int, int]): The pixel coordinates (x, y) in the image space
        id (int): Unique identifier for the point
        real_coord (Tuple[float, float]): Real-world coordinates (x, y) in meters
        color (Tuple[int, int, int]): RGB color tuple for visualization
        selected (bool): Selection state for UI interaction
    """

    coord: Tuple[int, int]
    id: int
    real_coord: Tuple[float, float] = (0.0, 0.0)
    color: Tuple[int, int, int] = (0, 0, 255)  # Default to red in BGR
    selected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the point to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary containing point data
        """
        return {
            "coord": self.coord,
            "id": self.id,
            "real_coord": self.real_coord,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Point":
        """
        Create a Point instance from a dictionary.

        Args:
            data (Dict[str, Any]): Dictionary containing point data

        Returns:
            Point: New Point instance

        Example:
            >>> data = {'coord': (100, 100), 'id': 1, 'color': (0, 0, 255)}
            >>> point = Point.from_dict(data)
        """
        point = cls(
            coord=(data["coord"][0], data["coord"][1]),
            id=data["id"],
            color=tuple(data["color"]),
        )
        if "real_coord" in data:
            point.real_coord = tuple(data["real_coord"])
        return point

    def is_near(self, x: int, y: int, threshold: int = 10) -> bool:
        """
        Check if a given point is within a threshold distance.

        Args:
            x (int): X coordinate to check
            y (int): Y coordinate to check
            threshold (int, optional): Maximum distance in pixels. Defaults to 10.

        Returns:
            bool: True if point is within threshold distance

        Example:
            >>> point = Point((100, 100), 1)
            >>> point.is_near(105, 103)
            True
        """
        return np.sqrt((self.coord[0] - x) ** 2 + (self.coord[1] - y) ** 2) < threshold

    def distance_to(self, other: "Point") -> float:
        """
        Calculate Euclidean distance to another point.

        Args:
            other (Point): Another Point instance

        Returns:
            float: Distance in pixels

        Example:
            >>> p1 = Point((0, 0), 1)
            >>> p2 = Point((3, 4), 2)
            >>> p1.distance_to(p2)
            5.0
        """
        return np.sqrt(
            (self.coord[0] - other.coord[0]) ** 2
            + (self.coord[1] - other.coord[1]) ** 2
        )

    def set_real_coordinates(self, x: float, y: float) -> None:
        """
        Set the real-world coordinates for this point.

        Args:
            x (float): Real-world X coordinate in meters
            y (float): Real-world Y coordinate in meters

        Example:
            >>> point = Point((100, 100), 1)
            >>> point.set_real_coordinates(1.5, 2.3)
        """
        self.real_coord = (x, y)


# Usage example
if __name__ == "__main__":
    # Create a point
    p1 = Point((100, 100), 1)
    p2 = Point((150, 150), 2, color=(0, 255, 0))

    # Test distance calculation
    dist = p1.distance_to(p2)
    print(f"Distance between points: {dist:.2f} pixels")

    # Test serialization
    data = p1.to_dict()
    p3 = Point.from_dict(data)
    assert p3.coord == p1.coord

    # Test proximity check
    is_near = p1.is_near(105, 103)
    print(f"Point is near (105, 103): {is_near}")
