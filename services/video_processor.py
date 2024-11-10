import cv2
import os
from datetime import datetime

class VideoProcessor:
    def __init__(self, app):
        self.app = app
        self.fish_count = 0
        self.output_video_path = None

    def process_video(self):
        selected_mask_name = self.app.selected_mask.get()
        if selected_mask_name:
            self.app.mask_creator.load_mask(selected_mask_name)
        else:
            selected_mask_name = "NoMask"

        # Generate timestamp for filename and logs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize video capture
        cap = cv2.VideoCapture(self.app.video_path)
        ret, prev_frame = cap.read()
        if not ret:
            print("Failed to read video")
            cap.release()
            return

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        # Temporary output video path
        output_dir = "processed_videos"
        os.makedirs(output_dir, exist_ok=True)
        video_name = os.path.basename(self.app.video_path).split('.')[0]
        temp_output_path = os.path.join(output_dir, f"{video_name}_{selected_mask_name}_{timestamp}_temp.mp4")

        # Initialize VideoWriter
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.app.mask_creator.mask is not None:
                gray = cv2.bitwise_and(gray, gray, mask=~self.app.mask_creator.mask)

            frame_diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            prev_gray = gray

            for contour in contours:
                if cv2.contourArea(contour) > self.app.min_contour_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.fish_count += 1

            # Write processed frame to output video
            out.write(frame)

            # Optional: Show the frame in real-time
            cv2.imshow('Fish Finder', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # Final output video path with mask name, fish count, and timestamp
        self.output_video_path = os.path.join(output_dir, f"{video_name}_{selected_mask_name}_{self.fish_count}_fish_{timestamp}.mp4")
        os.rename(temp_output_path, self.output_video_path)  # Rename temp file to final output name

        # Save results to CSV with the processed video path
        self.app.current_fish_count = self.fish_count
        self.app.save_results(self.output_video_path)
        self.app.show_fish_count(self.fish_count)
