import json
from typing import List, Optional, Tuple


class ZoneManager:
    """
    Manages definition and interaction with polygon zones in a 2D space.

    This class handles the creation, storage, and querying of polygon zones,
    with support for point-in-polygon testing and zone persistence.

    Attributes:
        zones (List[List[Tuple[float, float]]]): List of polygon zones
        current_polygon (List[Tuple[float, float]]): Points of polygon being drawn
        zones_file (str): Path to JSON file for zone persistence

    Example:
        >>> manager = ZoneManager(zones_file='zones.json')
        >>> manager.add_point(100, 100)
        >>> manager.add_point(200, 100)
        >>> manager.add_point(150, 150)
        >>> if manager.complete_current():
        ...     print("Zone created")
    """

    def __init__(self, zones_file: str = "zones.json"):
        """
        Initialize zone manager with specified storage file.

        Args:
            zones_file (str): Path to JSON file for storing zones
        """
        self.zones: List[List[Tuple[float, float]]] = []
        self.current_polygon: List[Tuple[float, float]] = []
        self.zones_file = zones_file
        self.load_zones()

    def load_zones(self) -> None:
        """
        Load zones from storage file.

        Attempts to read zones from JSON file, creates empty zone list if file
        doesn't exist or is invalid.

        Example:
            >>> manager = ZoneManager()
            >>> manager.load_zones()
        """
        try:
            with open(self.zones_file, "r") as f:
                data = json.load(f)
                self.zones = data.get("zones", [])
        except FileNotFoundError:
            self.zones = []
        except Exception as e:
            print(f"Error loading zones: {e}")
            self.zones = []

    def save_zones(self) -> None:
        """
        Save current zones to storage file.

        Writes all zones to JSON file for persistence.

        Example:
            >>> manager.add_point(100, 100)
            >>> manager.add_point(200, 100)
            >>> manager.add_point(150, 150)
            >>> manager.complete_current()
            >>> manager.save_zones()
        """
        try:
            with open(self.zones_file, "w") as f:
                json.dump({"zones": self.zones}, f)
        except Exception as e:
            print(f"Error saving zones: {e}")

    def add_point(self, x: float, y: float) -> None:
        """
        Add point to current polygon being drawn.

        Args:
            x (float): X coordinate of point
            y (float): Y coordinate of point

        Example:
            >>> manager.add_point(100, 100)
        """
        self.current_polygon.append((x, y))

    def clear_current(self) -> None:
        """
        Clear points from current polygon being drawn.

        Example:
            >>> manager.clear_current()
        """
        self.current_polygon = []

    def complete_current(self) -> bool:
        """
        Complete current polygon if it has at least 3 points.

        Returns:
            bool: True if polygon was completed, False if not enough points

        Example:
            >>> manager.add_point(100, 100)
            >>> manager.add_point(200, 100)
            >>> manager.add_point(150, 150)
            >>> success = manager.complete_current()
            >>> print(success)
            True
        """
        if len(self.current_polygon) >= 3:
            # Close the polygon
            self.current_polygon.append(self.current_polygon[0])
            # Add to zones
            self.zones.append(self.current_polygon.copy())
            # Clear current
            self.current_polygon = []
            # Save
            self.save_zones()
            return True
        return False

    def set_zone(self, zones: List[Tuple[float, float]]) -> None:
        self.zones = []
        zones.append(zones[0])
        self.zones.append(zones)
        self.save_zones()

    def delete_zone(self, index: int) -> bool:
        """
        Delete zone at specified index.

        Args:
            index (int): Index of zone to delete

        Returns:
            bool: True if zone was deleted, False if index invalid

        Example:
            >>> success = manager.delete_zone(0)
            >>> print(success)
            True
        """
        if 0 <= index < len(self.zones):
            del self.zones[index]
            self.save_zones()
            return True
        return False

    def point_in_polygon(
        self, point: Tuple[float, float], polygon: List[Tuple[float, float]]
    ) -> bool:
        """
        Check if point lies inside polygon using ray casting algorithm.

        Args:
            point (Tuple[float, float]): Point to test (x, y)
            polygon (List[Tuple[float, float]]): List of polygon vertices

        Returns:
            bool: True if point is inside polygon

        Example:
            >>> polygon = [(0,0), (100,0), (100,100), (0,100)]
            >>> manager.point_in_polygon((50, 50), polygon)
            True
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

    def check_point_in_zones(self, point: Tuple[float, float]) -> List[int]:
        """
        Check which zones contain the given point.

        Args:
            point (Tuple[float, float]): Point to test (x, y)

        Returns:
            List[int]: Indices of zones containing the point

        Example:
            >>> zones_containing_point = manager.check_point_in_zones((150, 150))
        """
        return [
            i
            for i, zone in enumerate(self.zones)
            if self.point_in_polygon(point, zone[:-1])
        ]  # [:-1] to exclude closing point

    def get_zone_points(self, index: int) -> Optional[List[Tuple[float, float]]]:
        """
        Get points defining a specific zone.

        Args:
            index (int): Index of zone to retrieve

        Returns:
            Optional[List[Tuple[float, float]]]: Zone points if index valid, None otherwise

        Example:
            >>> points = manager.get_zone_points(0)
            >>> if points:
            ...     print(f"Zone has {len(points)} vertices")
        """
        if 0 <= index < len(self.zones):
            return self.zones[index]
        return None

    def get_zone_count(self) -> int:
        """
        Get number of defined zones.

        Returns:
            int: Number of zones

        Example:
            >>> count = manager.get_zone_count()
            >>> print(f"There are {count} zones defined")
        """
        return len(self.zones)


# Usage example
if __name__ == "__main__":
    # Create zone manager
    manager = ZoneManager()

    # Create a simple square zone
    manager.add_point(0, 0)
    manager.add_point(100, 0)
    manager.add_point(100, 100)
    manager.add_point(0, 100)

    if manager.complete_current():
        print("Created square zone")

    # Test point in zone
    point = (50, 50)
    zones = manager.check_point_in_zones(point)
    print(f"Point {point} is in zones: {zones}")
