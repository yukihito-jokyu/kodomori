import base64
import json
import os
import time
from contextlib import asynccontextmanager
from typing import Tuple

import cv2
import numpy as np
from fastapi import FastAPI
from lib.camera_thread import CameraThread
from lib.point import Point
from lib.vision_processor import VisionProcessor
from lib.zone_manager import ZoneManager
from numpy.typing import NDArray

from .types import Pin, PinAndDistance


class MainApplication:
    def __init__(self) -> None:
        self.vision_processor = VisionProcessor(scale_factor=100)
        self.camera_thread = CameraThread(
            frame_callback=self.update_frame,
            mapping_callback=self.handle_mapped_point,
            camera_id=0,
        )
        self.zone_manager = ZoneManager()
        self.camera_thread.daemon = True
        self.camera_thread.start()

        self.points = []
        self.distances = {}

        self.mapped_points = []

        self.json_path = "homography_data.json"

        self.load_data()

    def update_frame(self, frame, results):
        pass

    def stop(self) -> None:
        self.camera_thread.stop()
        self.camera_thread.join()

    def save(self, points, distances):
        data = {
            "points": [point.to_dict() for point in points],
            "distances": distances,
        }
        with open(self.json_path, "w") as f:
            json.dump(data, f)

    def load_data(self) -> None:
        """Load saved homography points from file."""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
                    self.points = [
                        Point.from_dict(point_data)
                        for point_data in data.get("points", [])
                    ]
                    self.distances = data.get("distances", {})
            except Exception as e:
                print(f"Error loading data: {e}")

    def next(self):
        is_hit = False
        is_hit_id = None
        is_pred_hit = False
        is_pred_hit_id = None
        try:
            warped = self.get_waped()
            if warped is not None:
                warped_with_zone = self._draw_zones(warped)
                warped_with_zone, is_hit, is_hit_id, is_pred_hit, is_pred_hit_id = (
                    self._draw_tracked_points(warped_with_zone)
                )

                ret, buffer = cv2.imencode(".jpg", warped_with_zone)
                # フレームをJPEG形式にエンコード
                _, buffer = cv2.imencode(".jpg", warped_with_zone)
                # Base64エンコードしてテキスト形式に変換
                warped_with_zone_base64 = base64.b64encode(buffer).decode("utf-8")

                return (
                    warped_with_zone_base64,
                    is_hit,
                    is_hit_id,
                    is_pred_hit,
                    is_pred_hit_id,
                )
            else:
                # warpedがNoneの場合の処理
                return "", is_hit, is_hit_id, is_pred_hit, is_pred_hit_id
        except cv2.error as e:
            print(f"OpenCV error occurred: {e}")
            # エラーが発生した場合、空の文字列を返す
            return "", is_hit, is_hit_id, is_pred_hit, is_pred_hit_id
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return "", is_hit, is_hit_id, is_pred_hit, is_pred_hit_id

    def get_frame(self) -> str:
        frame = self.camera_thread.frame_buffer.get_frame()
        height, width, _ = frame.shape
        print(height, width)
        if frame is not None:
            ret, buffer = cv2.imencode(".jpg", frame)
            # フレームをJPEG形式にエンコード
            _, buffer = cv2.imencode(".jpg", frame)
            # Base64エンコードしてテキスト形式に変換
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            return frame_base64

    def get_waped(self):
        frame = self.camera_thread.frame_buffer.get_frame()
        if len(self.points) == 4:
            # Calculate homography using vision processor
            self.vision_processor.calculate_homography(self.points, self.distances)
            dimensions = self.vision_processor.get_output_dimensions()

            if dimensions is None:
                return

            # Apply homography transform
            warped = cv2.warpPerspective(
                frame, self.vision_processor._matrix, dimensions
            )

            if warped is not None:
                return warped

    def get_wrap_code(self) -> Tuple[str, int, int]:
        frame = self.camera_thread.frame_buffer.get_frame()
        if len(self.points) == 4:
            # Calculate homography using vision processor
            self.vision_processor.calculate_homography(self.points, self.distances)
            dimensions = self.vision_processor.get_output_dimensions()

            if dimensions is None:
                return

            # Apply homography transform
            warped = cv2.warpPerspective(
                frame, self.vision_processor._matrix, dimensions
            )

            if warped is not None:
                height, width, _ = warped.shape
                ret, buffer = cv2.imencode(".jpg", warped)
                # フレームをJPEG形式にエンコード
                _, buffer = cv2.imencode(".jpg", warped)
                # Base64エンコードしてテキスト形式に変換
                warped_base64 = base64.b64encode(buffer).decode("utf-8")
                return warped_base64, height, width

    def set_floor(self, pin_and_distances: PinAndDistance) -> str:
        pin_1_x = int(pin_and_distances.pin_1_x * 16 / 11)
        pin_1_y = int(pin_and_distances.pin_1_y * 16 / 11)
        pin_2_x = int(pin_and_distances.pin_2_x * 16 / 11)
        pin_2_y = int(pin_and_distances.pin_2_y * 16 / 11)
        pin_3_x = int(pin_and_distances.pin_3_x * 16 / 11)
        pin_3_y = int(pin_and_distances.pin_3_y * 16 / 11)
        pin_4_x = int(pin_and_distances.pin_4_x * 16 / 11)
        pin_4_y = int(pin_and_distances.pin_4_y * 16 / 11)

        p1_p2 = pin_and_distances.p1_p2
        p1_p3 = pin_and_distances.p1_p3
        p1_p4 = pin_and_distances.p1_p4
        p2_p3 = pin_and_distances.p2_p3
        p2_p4 = pin_and_distances.p2_p4
        p3_p4 = pin_and_distances.p3_p4

        self.distances = {
            "1-2": p1_p2,
            "1-3": p1_p3,
            "1-4": p1_p4,
            "2-3": p2_p3,
            "2-4": p2_p4,
            "3-4": p3_p4,
        }

        self.points = [
            {
                "coord": (pin_1_x, pin_1_y),
                "id": 1,
                "color": (0, 0, 255),
                "real_coord": (0.0, 0.0),
            },
            {
                "coord": (pin_2_x, pin_2_y),
                "id": 2,
                "color": (0, 0, 255),
                "real_coord": (0.0, 0.0),
            },
            {
                "coord": (pin_3_x, pin_3_y),
                "id": 3,
                "color": (0, 0, 255),
                "real_coord": (0.0, 0.0),
            },
            {
                "coord": (pin_4_x, pin_4_y),
                "id": 4,
                "color": (0, 0, 255),
                "real_coord": (0.0, 0.0),
            },
        ]

        self.points = [Point.from_dict(p) for p in self.points]

        self.save(self.points, self.distances)

        self.camera_thread.points = self.points

        warped = self.get_waped()

        if warped is not None:
            ret, buffer = cv2.imencode(".jpg", warped)
            # フレームをJPEG形式にエンコード
            _, buffer = cv2.imencode(".jpg", warped)
            # Base64エンコードしてテキスト形式に変換
            warped_base64 = base64.b64encode(buffer).decode("utf-8")
            return warped_base64

    def set_zone(self, zones: Pin) -> NDArray:
        pin_1_x = int(zones.pin_1_x)
        pin_1_y = int(zones.pin_1_y)
        pin_2_x = int(zones.pin_2_x)
        pin_2_y = int(zones.pin_2_y)
        pin_3_x = int(zones.pin_3_x)
        pin_3_y = int(zones.pin_3_y)
        pin_4_x = int(zones.pin_4_x)
        pin_4_y = int(zones.pin_4_y)

        zones = [
            (pin_1_x, pin_1_y),
            (pin_2_x, pin_2_y),
            (pin_3_x, pin_3_y),
            (pin_4_x, pin_4_y),
        ]

        self.zone_manager.set_zone(zones)

        warped = self.get_waped()
        if warped is not None:
            warped_with_zone = self._draw_zones(warped)

            ret, buffer = cv2.imencode(".jpg", warped_with_zone)
            # フレームをJPEG形式にエンコード
            _, buffer = cv2.imencode(".jpg", warped_with_zone)
            # Base64エンコードしてテキスト形式に変換
            warped_with_zone_base64 = base64.b64encode(buffer).decode("utf-8")

            return warped_with_zone_base64

    def _draw_zones(self, warped: NDArray) -> NDArray:
        """Draw zones and current polygon"""
        for zone in self.zone_manager.zones:
            points = np.array(zone)
            cv2.fillPoly(
                warped,
                [points.astype(np.int32)],
                (50, 50, 150, 100),
                lineType=cv2.LINE_AA,
            )
            cv2.polylines(
                warped,
                [points.astype(np.int32)],
                True,
                (100, 100, 200),
                2,
                lineType=cv2.LINE_AA,
            )

        return warped

    def _draw_tracked_points(self, warped):
        """Draw tracked points with zone detection"""
        # print(self.mapped_points)
        is_hit = False
        is_hit_id = None
        is_pred_hit = False
        is_pred_hit_id = None
        for point in self.mapped_points:
            try:
                # Process tracking results using vision processor
                result = self.vision_processor.process_tracking_result(
                    point, self.zone_manager.zones
                )

                # Draw current position
                px, py = result.transformed_coord

                if not (0 <= px < warped.shape[1] and 0 <= py < warped.shape[0]):
                    continue

                # Check zone collisions
                zones_hit = self.zone_manager.check_point_in_zones((px, py))
                if zones_hit:
                    is_hit = True
                    is_hit_id = point.get("track_id", "unknown")

                # Color based on zone presence
                point_color = (0, 255, 255)  # default yellow
                if result.zones:  # if in any zones
                    point_color = (0, 255, 0)  # green

                cv2.circle(warped, (int(px), int(py)), 5, point_color, -1)

                # Draw prediction if available
                if result.prediction:
                    pred_x, pred_y = result.prediction
                    if 0 <= pred_x < warped.shape[1] and 0 <= pred_y < warped.shape[0]:
                        cv2.circle(
                            warped, (int(pred_x), int(pred_y)), 5, (0, 0, 255), -1
                        )
                        cv2.line(
                            warped,
                            (int(px), int(py)),
                            (int(pred_x), int(pred_y)),
                            (0, 0, 255),
                            2,
                        )

                    # Check predicted position zone collisions
                    pred_zones_hit = self.zone_manager.check_point_in_zones(
                        (pred_x, pred_y)
                    )
                    if pred_zones_hit:
                        is_pred_hit = True
                        is_pred_hit_id = point.get("track_id", "unknown")

            except Exception as e:
                print(f"Error processing tracking result: {e}")
                continue

        return warped, is_hit, is_hit_id, is_pred_hit, is_pred_hit_id

    def handle_mapped_point(self, point_data):
        """Process mapped points from tracking"""
        if point_data is None:
            self.clear_mapped_points()
            return

        try:
            # Update or add point tracking data
            existing_point = next(
                (
                    p
                    for p in self.mapped_points
                    if p.get("track_id") == point_data["track_id"]
                ),
                None,
            )

            current_time = time.time()

            if existing_point:
                existing_point.update(
                    {
                        "prev_coord": existing_point["coord"],
                        "coord": point_data["coord"],
                        "mapped": point_data["mapped"],
                        "last_update": current_time,
                    }
                )

                # Calculate prediction
                if "prev_coord" in existing_point:
                    dx = existing_point["coord"][0] - existing_point["prev_coord"][0]
                    dy = existing_point["coord"][1] - existing_point["prev_coord"][1]

                    speed = np.sqrt(dx * dx + dy * dy)
                    scale = min(max(speed / 10, 3.0), 15.0)

                    existing_point["predicted"] = (
                        existing_point["mapped"][0] + dx * scale,
                        existing_point["mapped"][1] + dy * scale,
                    )
            else:
                point_data["last_update"] = current_time
                self.mapped_points.append(point_data)

            # Clean up old points
            self.mapped_points = [
                p for p in self.mapped_points if current_time - p["last_update"] < 1.0
            ]

            # self.update_sim_frame()

        except Exception as e:
            print(f"Error mapping point: {e}")

    def clear_mapped_points(self):
        """Clear all mapped tracking points"""
        self.mapped_points = []


# camera_thread = Camera_Thread(buffer_all=False)

main_app = MainApplication()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event")
    yield
    print("Stopping the server...")
    main_app.stop()  # カメラスレッドの停止処理
    print("Server stopped gracefully.")
