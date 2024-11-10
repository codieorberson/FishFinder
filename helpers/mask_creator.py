import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class MaskCreator:
    def __init__(self, app):
        self.app = app
        self.mask = None
        self.x_start = -1
        self.y_start = -1
        self.temp_img = None
        self.first_frame = None  # Store the first frame for the preview
        self.annotated_frame = None  # Frame with shapes drawn
        self.saved_masks_dir = "saved_masks/"
        os.makedirs(self.saved_masks_dir, exist_ok=True)  # Ensure directory exists

    def create_mask(self):
        # Capture the first frame from the video for preview purposes
        cap = cv2.VideoCapture(self.app.video_path)
        ret, self.first_frame = cap.read()
        if not ret:
            print("Failed to read video")
            cap.release()
            return

        # Initialize the mask, temp image, and annotated frame for drawing
        self.mask = np.zeros(self.first_frame.shape[:2], dtype="uint8")
        self.temp_img = self.first_frame.copy()
        self.annotated_frame = self.first_frame.copy()  # Copy for annotated frame

        # Mouse callback function to draw shapes
        def draw_shape(event, x, y, flags, param):
            if self.app.drawing_mode == "Freeform":
                self.draw_freeform(event, x, y, flags)
            elif self.app.drawing_mode == "Rectangle":
                self.draw_rectangle(event, x, y, flags)

        cv2.imshow("Draw Mask", self.temp_img)
        cv2.setMouseCallback("Draw Mask", draw_shape)

        while True:
            if cv2.waitKey(1) & 0xFF == 13:  # Enter key
                break

        cv2.destroyWindow("Draw Mask")
        cap.release()

        # Schedule save_mask_prompt to run on the main thread
        self.app.root.after(0, self.save_mask_prompt)

    def draw_freeform(self, event, x, y, flags):
        current_brush_size = self.app.brush_size
        if event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON):
            # Draw on the mask and temp_img as well as the annotated_frame for outlines
            cv2.circle(self.mask, (x, y), current_brush_size, 255, -1)
            cv2.circle(self.temp_img, (x, y), current_brush_size, (0, 255, 0), -1)
            cv2.circle(self.annotated_frame, (x, y), current_brush_size, (0, 255, 0), 2)  # Outline in green
            cv2.imshow("Draw Mask", self.temp_img)
        elif event == cv2.EVENT_MOUSEMOVE:
            hover_img = self.temp_img.copy()
            cv2.circle(hover_img, (x, y), current_brush_size, (0, 255, 0), 1)
            cv2.imshow("Draw Mask", hover_img)

    def draw_rectangle(self, event, x, y, flags):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_start, self.y_start = x, y
        elif event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON:
            hover_img = self.temp_img.copy()
            cv2.rectangle(hover_img, (self.x_start, self.y_start), (x, y), (0, 255, 0), 2)
            cv2.imshow("Draw Mask", hover_img)
        elif event == cv2.EVENT_LBUTTONUP:
            # Draw on mask and temp_img, and also save the outline on annotated_frame
            cv2.rectangle(self.mask, (self.x_start, self.y_start), (x, y), 255, -1)
            cv2.rectangle(self.temp_img, (self.x_start, self.y_start), (x, y), (0, 255, 0), -1)
            cv2.rectangle(self.annotated_frame, (self.x_start, self.y_start), (x, y), (0, 255, 0), 2)  # Outline in green
            cv2.imshow("Draw Mask", self.temp_img)

    def save_mask_prompt(self):
        # Prompt user if they want to save the mask
        if messagebox.askyesno("Save Mask", "Do you want to save this mask?"):
            # Open a dialog to enter the mask name
            mask_name = simpledialog.askstring("Save Mask", "Enter a name for this mask:")
            if mask_name:
                self.save_mask(mask_name)
            else:
                messagebox.showwarning("Save Mask", "Mask not saved. Please enter a valid name.")
    
    def save_mask(self, mask_name):
        # Save the mask as a .npy file
        mask_path = os.path.join(self.saved_masks_dir, f"{mask_name}.npy")
        np.save(mask_path, self.mask)
        print(f"Mask saved as {mask_name}")

        # Save the annotated frame with outlines
        preview_path = os.path.join(self.saved_masks_dir, f"{mask_name}_annotated.jpg")
        cv2.imwrite(preview_path, self.annotated_frame)
        print(f"Annotated preview image saved as {mask_name}_annotated.jpg")

        # Refresh saved masks in GUI
        self.app.load_saved_masks()

    def load_mask(self, mask_name):
        # Load a mask from the saved file
        mask_path = os.path.join(self.saved_masks_dir, f"{mask_name}.npy")
        if os.path.exists(mask_path):
            self.mask = np.load(mask_path)
            print(f"Loaded mask: {mask_name}")
        else:
            print(f"Mask {mask_name} does not exist.")

    


