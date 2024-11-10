import csv
import os

class ResultSaver:
    def __init__(self, file_path="results/results.csv"):
        self.file_path = file_path

        # Check if the file exists, if not, create it with headers
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Mask Name", "Video File", "Fish Count", "Processed Video Path", "Timestamp"])

    def save_result(self, mask_name, video_file, fish_count, processed_video_path, timestamp):
        # Write the result row to the CSV file
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([mask_name if mask_name else "None", video_file, fish_count, processed_video_path, timestamp])
        print(f"Results saved to {self.file_path}")
