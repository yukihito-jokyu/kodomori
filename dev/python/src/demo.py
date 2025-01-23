import json
import os
import time
import tkinter as tk
from tkinter import ttk

import cv2
import numpy as np
from lib.camera_thread import CameraThread
from lib.point import Point
from lib.vision_processor import VisionProcessor
from lib.zone_manager import ZoneManager
from PIL import Image, ImageTk


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Homography Tool")

        # Core application state
        self.save_file = "homography_data.json"
        self.last_modified = 0
        self.scale_factor = 100
        self.last_frame = None
        self.last_results = None
        self.mapped_points = []

        # Initialize vision processor
        self.vision_processor = VisionProcessor(scale_factor=self.scale_factor)

        # Setup UI frames
        self._setup_frames()

        # Initialize managers and components
        self.zone_manager = ZoneManager()
        self.init_sim_frame()
        self.init_edit_frame()
        self.update_zone_list()

        # Initialize camera thread
        self.camera_thread = CameraThread(
            frame_callback=self.update_frame,
            mapping_callback=self.handle_mapped_point,
            camera_id=0,
            model_path="yolov8n.pt",
            save_file=self.save_file,
        )
        self.camera_thread.daemon = True
        self.camera_thread.start()

        # Set up periodic update
        self.root.after(100, self.periodic_update)

        # Bind cleanup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_frames(self):
        """Initialize main UI frames"""
        self.edit_frame = ttk.LabelFrame(self.root, text="Point Editor")
        self.edit_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.sim_frame = ttk.LabelFrame(self.root, text="Simulation View")
        self.sim_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

    def update_sim_frame(self):
        """Update simulation display using vision processor"""
        try:
            if self.last_frame is None:
                return

            with open(self.save_file, "r") as f:
                data = json.load(f)
                points = [Point.from_dict(p) for p in data["points"]]

            if len(points) == 4:
                # Calculate homography using vision processor
                self.vision_processor.calculate_homography(
                    points, data.get("distances", {})
                )
                dimensions = self.vision_processor.get_output_dimensions()

                if dimensions is None:
                    return

                # Apply homography transform
                warped = cv2.warpPerspective(
                    self.last_frame, self.vision_processor._matrix, dimensions
                )

                self._draw_grid(warped)
                self._draw_zones(warped)
                self._draw_tracked_points(warped)
                self._update_display(warped)

        except Exception as e:
            print(f"Error in sim update: {e}")

    def _draw_grid(self, warped):
        """Draw measurement grid"""
        dimensions = self.vision_processor.get_output_dimensions()
        if not dimensions:
            return

        width, height = dimensions
        grid_spacing = int(self.scale_factor)

        for x in range(0, width, grid_spacing):
            cv2.line(warped, (x, 0), (x, height), (128, 128, 128), 1)
        for y in range(0, height, grid_spacing):
            cv2.line(warped, (0, y), (width, y), (128, 128, 128), 1)

    def _draw_zones(self, warped):
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

        if self.drawing_mode.get() and self.zone_manager.current_polygon:
            points = np.array(self.zone_manager.current_polygon)
            if len(points) > 1:
                cv2.polylines(
                    warped, [points.astype(np.int32)], False, (200, 50, 50), 2
                )
            for point in self.zone_manager.current_polygon:
                cv2.circle(warped, (int(point[0]), int(point[1])), 3, (200, 50, 50), -1)

    def _draw_tracked_points(self, warped):
        """Draw tracked points with zone detection"""
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

            except Exception as e:
                print(f"Error processing tracking result: {e}")
                continue

    def _update_display(self, frame):
        """Update tkinter display with new frame"""
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(display_frame)
        img_tk = ImageTk.PhotoImage(image=img)
        self.sim_label.configure(image=img_tk)
        self.sim_label.image = img_tk

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

            self.update_sim_frame()

        except Exception as e:
            print(f"Error mapping point: {e}")

    def init_sim_frame(self):
        """Initialize simulation view frame"""
        self.sim_label = ttk.Label(self.sim_frame)
        self.sim_label.pack(fill="both", expand=True)

        # Drawing mode setup
        self.drawing_mode = tk.BooleanVar(value=False)
        self.drawing_mode.trace("w", lambda *args: self._on_drawing_mode_change())
        self.sim_label.bind("<Button-1>", self.on_sim_click)

        self._setup_sim_controls()
        self._setup_zone_list()

    def _setup_sim_controls(self):
        """Setup simulation control buttons"""
        control_frame = ttk.Frame(self.sim_frame)
        control_frame.pack(fill="x", padx=5, pady=5)

        ttk.Checkbutton(
            control_frame, text="Draw Zone Mode", variable=self.drawing_mode
        ).pack(side="left", padx=5)
        ttk.Button(
            control_frame, text="Complete Zone", command=self.complete_current_zone
        ).pack(side="left", padx=5)
        ttk.Button(
            control_frame, text="Clear Current", command=self.clear_current_zone
        ).pack(side="left", padx=5)

    def _setup_zone_list(self):
        """Setup zone list display"""
        self.zone_list_frame = ttk.LabelFrame(self.sim_frame, text="Saved Zones")
        self.zone_list_frame.pack(fill="x", padx=5, pady=5)

        self.zone_listbox = tk.Listbox(self.zone_list_frame, height=5)
        self.zone_listbox.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        ttk.Button(
            self.zone_list_frame, text="Delete Zone", command=self.delete_selected_zone
        ).pack(side="right", padx=5, pady=5)

    def init_edit_frame(self):
        """Initialize point editor frame"""
        self.points_frame = ttk.Frame(self.edit_frame)
        self.points_frame.pack(fill="both", expand=True)

        # Scale factor control
        scale_frame = ttk.Frame(self.edit_frame)
        scale_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(scale_frame, text="Scale (pixels/meter):").pack(side="left", padx=5)
        scale_entry = ttk.Entry(scale_frame, width=10)
        scale_entry.insert(0, str(self.scale_factor))
        scale_entry.pack(side="left", padx=5)

        ttk.Button(
            scale_frame,
            text="Update Scale",
            command=lambda: self._update_scale(scale_entry),
        ).pack(side="left", padx=5)
        ttk.Button(
            scale_frame, text="Clear Mapped Points", command=self.clear_mapped_points
        ).pack(side="left", padx=5)

    def _update_scale(self, entry):
        """Update scale factor from entry widget"""
        try:
            new_scale = float(entry.get())
            if new_scale > 0:
                self.scale_factor = new_scale
                self.vision_processor.scale_factor = (
                    new_scale  # Update vision processor scale
                )
                self.update_sim_frame()
        except ValueError:
            pass

    def update_frame(self, frame, results):
        """Handle frame updates from camera thread"""
        self.last_frame = frame.copy()
        self.last_results = results
        self.update_sim_frame()

    def on_sim_click(self, event):
        """Handle simulation view clicks"""
        if not self.drawing_mode.get():
            return
        try:
            self.zone_manager.add_point(event.x, event.y)
            self.update_sim_frame()
        except Exception as e:
            print(f"Error in click handler: {e}")

    def complete_current_zone(self):
        """Complete current zone drawing"""
        if self.zone_manager.complete_current():
            self.drawing_mode.set(False)
            self.update_zone_list()
            self.update_sim_frame()

    def clear_current_zone(self):
        """Clear current zone in progress"""
        self.zone_manager.clear_current()
        self.update_sim_frame()

    def delete_selected_zone(self):
        """Delete selected zone from list"""
        selection = self.zone_listbox.curselection()
        if selection:
            if self.zone_manager.delete_zone(selection[0]):
                self.update_zone_list()
                self.update_sim_frame()

    def update_zone_list(self):
        """Update zone list display"""
        self.zone_listbox.delete(0, tk.END)
        for i, _ in enumerate(self.zone_manager.zones):
            self.zone_listbox.insert(tk.END, f"Zone {i+1}")

    def clear_mapped_points(self):
        """Clear all mapped tracking points"""
        self.mapped_points = []
        self.update_sim_frame()

    def periodic_update(self):
        """Periodic UI update check"""
        try:
            current_modified = os.path.getmtime(self.save_file)
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                self.update_edit_frame()
        except FileNotFoundError:
            pass

        self.root.after(100, self.periodic_update)

    def _on_drawing_mode_change(self):
        """Handle drawing mode changes"""
        if not self.drawing_mode.get():
            self.zone_manager.clear_current()
        self.update_sim_frame()

    def update_edit_frame(self):
        """Update point editor frame"""
        for widget in self.points_frame.winfo_children():
            widget.destroy()

        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)
                points = [Point.from_dict(p) for p in data["points"]]

            if len(points) >= 2:
                self._setup_distance_editor(points, data)

        except Exception as e:
            print(f"Error updating edit frame: {e}")

    def _setup_distance_editor(self, points, data):
        """Setup distance measurement editor"""
        frame = ttk.LabelFrame(self.points_frame, text="Point Distances")
        frame.pack(fill="x", padx=5, pady=5)

        distances = {}
        row = 0

        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points[i + 1 :], i + 1):
                dist_key = f"{p1.id}-{p2.id}"

                ttk.Label(frame, text=f"Distance P{p1.id} to P{p2.id}:").grid(
                    row=row, column=0, padx=5, pady=2
                )

                entry = ttk.Entry(frame, width=10)
                if "distances" in data and dist_key in data["distances"]:
                    entry.insert(0, str(data["distances"][dist_key]))
                entry.grid(row=row, column=1, padx=5, pady=2)
                distances[dist_key] = entry

                cam_dist = np.sqrt(
                    (p1.coord[0] - p2.coord[0]) ** 2 + (p1.coord[1] - p2.coord[1]) ** 2
                )
                ttk.Label(frame, text=f"Camera: {cam_dist:.1f}px").grid(
                    row=row, column=2, padx=5, pady=2
                )

                row += 1

        save_btn = ttk.Button(
            frame,
            text="Save All Distances",
            command=lambda: self._save_distances(distances),
        )
        save_btn.grid(row=row, column=0, columnspan=3, pady=10)

    def _save_distances(self, distance_entries):
        """Save distance measurements"""
        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)

            data["distances"] = {}
            for key, entry in distance_entries.items():
                try:
                    distance = float(entry.get())
                    if distance > 0:
                        data["distances"][key] = distance
                except ValueError:
                    continue

            with open(self.save_file, "w") as f:
                json.dump(data, f)

            # Refresh display after saving
            self.update_sim_frame()

        except Exception as e:
            print(f"Error saving distances: {e}")

    def on_closing(self):
        """Clean up on window close"""
        if hasattr(self, "camera_thread"):
            self.camera_thread.stop()
            self.camera_thread.join()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
