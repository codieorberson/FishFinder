import tkinter as tk
from tkinter import Scale, Label, OptionMenu, StringVar, messagebox, LabelFrame, Button, filedialog
from threading import Thread
from helpers.mask_creator import MaskCreator
from services.video_processor import VideoProcessor
import os
import cv2
import numpy as np
from services.result_saver import ResultSaver
from datetime import datetime

class FishFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fish Finder")

        # Application settings and defaults
        self.min_contour_area = 500
        self.brush_size = 10
        self.drawing_mode = "Freeform"
        self.saved_masks_dir = "saved_masks/"
        self.selected_mask = StringVar(value="")  # Initialize with an empty value
        
        self.current_fish_count = 0

        # Default video path
        self.video_path = 'Videos/BW.mp4'

        # Video path label
        self.video_path_label = Label(root, text=f"Video: {self.video_path}", font=("Helvetica", 10))
        self.video_path_label.pack(pady=5)

        self.select_video_button = Button(root, text="Select Video", command=self.select_video_path)
        self.select_video_button.pack(pady=5)

        # Create MaskCreator and VideoProcessor instances
        self.mask_creator = MaskCreator(self)
        self.video_processor = VideoProcessor(self)
        
        # Result saver instance
        self.result_saver = ResultSaver()

        # GUI elements
        self.setup_gui()
        self.load_saved_masks()

    def reset_results(self):
        self.current_fish_count = 0

    def select_video_path(self):
        # Open file dialog to select a video file
        selected_file = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
        )
        if selected_file:  # If a file was selected
            self.video_path = selected_file
        else:  # If no file was selected, use the default path
            self.video_path = "BW.mp4"
        
        # Update the video path label
        self.video_path_label.config(text=f"Video: {self.video_path}")

    def setup_gui(self):
        # Mask Section
        mask_frame = LabelFrame(self.root, text="Mask Options", padx=10, pady=10)
        mask_frame.pack(pady=10, fill="both", expand="yes")

        # Create Mask button
        create_mask_button = tk.Button(mask_frame, text="Create Mask", command=self.start_mask_thread)
        create_mask_button.grid(row=0, column=0, padx=5, pady=5)
        self.add_hover_effect(create_mask_button, "lightblue")

        # Select Mask dropdown
        self.mask_menu = OptionMenu(mask_frame, self.selected_mask, "", command=self.on_mask_selected)
        self.mask_menu.grid(row=0, column=1, padx=5, pady=5)

        # Preview Mask button
        preview_mask_button = tk.Button(mask_frame, text="Preview Mask", command=self.preview_mask)
        preview_mask_button.grid(row=0, column=2, padx=5, pady=5)
        self.add_hover_effect(preview_mask_button, "lightblue")

        # Label to show the currently selected mask
        self.selected_mask_label = Label(mask_frame, text="No mask selected")
        self.selected_mask_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Drawing Options Section
        drawing_frame = LabelFrame(self.root, text="Drawing Options", padx=10, pady=10)
        drawing_frame.pack(pady=10, fill="both", expand="yes")

        # Drawing mode dropdown
        drawing_modes = ["Freeform", "Rectangle"]
        drawing_mode_var = StringVar(value=drawing_modes[0])
        drawing_mode_menu = OptionMenu(drawing_frame, drawing_mode_var, *drawing_modes, command=self.update_drawing_mode)
        drawing_mode_menu.grid(row=0, column=0, padx=5, pady=5)

        # Brush size slider
        brush_label = Label(drawing_frame, text="Brush Size for Mask (Freeform only)")
        brush_label.grid(row=1, column=0, padx=5, pady=5)
        brush_slider = Scale(drawing_frame, from_=5, to=50, orient='horizontal', command=self.update_brush_size)
        brush_slider.set(self.brush_size)
        brush_slider.grid(row=2, column=0, padx=5, pady=5)

        # Contour Settings Section
        contour_frame = LabelFrame(self.root, text="Contour Settings", padx=10, pady=10)
        contour_frame.pack(pady=10, fill="both", expand="yes")

        # Minimum contour area slider
        label = Label(contour_frame, text="Minimum Contour Area")
        label.grid(row=0, column=0, padx=5, pady=5)
        contour_slider = Scale(contour_frame, from_=100, to=2000, orient='horizontal', command=self.update_min_contour_area)
        contour_slider.set(self.min_contour_area)
        contour_slider.grid(row=1, column=0, padx=5, pady=5)

        # Video Processing Section
        video_frame = LabelFrame(self.root, text="Video Processing", padx=10, pady=10)
        video_frame.pack(pady=10, fill="both", expand="yes")

        # Start video processing button
        start_button = tk.Button(video_frame, text="Start Video", command=self.start_video_thread)
        start_button.grid(row=0, column=0, padx=5, pady=5)
        self.add_hover_effect(start_button, "lightgreen")

    def load_saved_masks(self):
        # Load available masks into the dropdown
        masks = [f[:-4] for f in os.listdir(self.saved_masks_dir) if f.endswith(".npy")]
        menu = self.mask_menu["menu"]
        menu.delete(0, "end")
        for mask_name in masks:
            menu.add_command(label=mask_name, command=lambda value=mask_name: self.on_mask_selected(value))

        # Set initial selection if masks are available
        if masks:
            self.selected_mask.set(masks[0])
            self.update_selected_mask_label()

    def on_mask_selected(self, mask_name):
        # Set the selected mask and update the label
        self.selected_mask.set(mask_name)
        self.update_selected_mask_label()

    def start_mask_thread(self):
        # Show instructions to the user before starting the mask creation process
        messagebox.showinfo(
            "Mask Creation Instructions",
            "Use Freeform or Rectangle mode to create a mask. \n"
            "Press 'Enter' to complete the mask creation."
        )
        # Start the mask creation process in a new thread
        mask_thread = Thread(target=self.mask_creator.create_mask)
        mask_thread.start()

    def start_video_thread(self):
        if self.video_path:
            self.reset_results()
            self.video_processor.fish_count = 0
            
            # Start the video processing in a new thread and save results after processing
            def process_and_save():
                self.video_processor.process_video()  # Process the video
                self.current_fish_count = self.video_processor.fish_count  # Get the final fish count
                # Pass the processed video path to save_results
            
            video_thread = Thread(target=process_and_save)
            video_thread.start()
        else:
            print("Please select a video file first.")



    def preview_mask(self):
    # Preview the selected mask with the original frame and outline the masked areas
        selected_mask_name = self.selected_mask.get()
        if selected_mask_name:
            mask_path = os.path.join(self.saved_masks_dir, f"{selected_mask_name}.npy")
            preview_path = os.path.join(self.saved_masks_dir, f"{selected_mask_name}_annotated.jpg")

            # Load the mask and first frame (original frame)
            if os.path.exists(mask_path):
                mask = np.load(mask_path)
            else:
                messagebox.showerror("Error", "Selected mask file does not exist.")
                return

            # Load the preview image or first frame of the video
            if os.path.exists(preview_path):
                original_frame = cv2.imread(preview_path)
            else:
                messagebox.showinfo("Info", "No preview image available for the selected mask.")
                return

            # Find contours in the mask and draw them on the original frame
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                # Draw the outline of each contour on the original frame
                cv2.drawContours(original_frame, [contour], -1, (0, 255, 0), 2)  # Green outline

            # Display the original frame with mask outlines
            cv2.imshow("Mask Preview with Original Frame", original_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showinfo("Info", "No mask selected to preview.")



    def update_selected_mask_label(self):
        # Update the label to show the current selected mask
        selected_mask_name = self.selected_mask.get()
        if selected_mask_name:
            self.selected_mask_label.config(text=f"Selected Mask: {selected_mask_name}")
        else:
            self.selected_mask_label.config(text="No mask selected")

    def update_min_contour_area(self, value):
        self.min_contour_area = int(value)

    def update_brush_size(self, value):
        self.brush_size = int(value)

    def update_drawing_mode(self, value):
        self.drawing_mode = value

    def show_fish_count(self, fish_count):
        messagebox.showinfo("Fish Finder", f"Total fish counted: {fish_count}")

    def add_hover_effect(self, button, color_on_hover):
        # Helper function to add hover effect to buttons
        original_color = button.cget("background")
        button.bind("<Enter>", lambda e: button.config(background=color_on_hover))
        button.bind("<Leave>", lambda e: button.config(background=original_color))
    
    def save_results(self, processed_video_path):
        # Generate timestamp for logging
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the results using ResultSaver
        mask_name = self.selected_mask.get() if self.selected_mask.get() else "None"
        video_file = os.path.basename(self.video_path)
        fish_count = self.current_fish_count
        self.result_saver.save_result(mask_name, video_file, fish_count, processed_video_path, timestamp)




