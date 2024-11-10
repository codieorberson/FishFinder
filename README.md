
# Fish Finder Application

The Fish Finder Application allows users to process videos with a sonar-like fish finder, apply custom masks, and count fish detections. It saves processed videos with bounding boxes on detected fish and logs results (mask name, video file, fish count, processed video path, and timestamp) in a CSV file for easy tracking.

## Features
- **Mask Creation**: Users can create custom masks (Freeform or Rectangle) to exclude specific regions from analysis.
- **Video Processing**: Detects and counts fish based on video frames, applying selected masks.
- **Dynamic Filename Generation**: Processed video files include mask names, fish counts, and timestamps.
- **CSV Logging**: Saves each session's details, including mask name, video filename, fish count, processed video path, and timestamp.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating a Mask](#creating-a-mask)
  - [Processing a Video](#processing-a-video)
  - [Viewing Results](#viewing-results)
- [Directory Structure](#directory-structure)
- [Required Pip Packages](#required-pip-packages)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Installation

### Prerequisites
- **Python 3.7 or later** is required.

### Cloning the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/fish-finder-app.git
cd fish-finder-app
```

### Installing Dependencies
Use the following command to install all required packages:

```bash
pip install -r requirements.txt
```

#### `requirements.txt`:
```plaintext
opencv-python-headless
numpy
tkinter
```

#### Manual Installation of Required Packages
If the above method doesn't work, you can install each package manually:
```bash
pip install opencv-python-headless
pip install numpy
pip install pillow  # For Tkinter support with images
```

---

## Usage

### Starting the Application
1. **Run the main application**:
   ```bash
   python main.py
   ```
2. **Select or create a mask**, choose a video file, and start processing.

### Interface Overview
- **Mask Options**:
  - `Create Mask`: Start creating a mask. Select Freeform or Rectangle and adjust brush size for Freeform.
  - `Select Mask`: Choose an existing mask from the dropdown.
  - `Preview Mask`: View the mask applied to the first frame of the selected video.

- **Drawing Options**:
  - `Brush Size`: Adjust brush size when using Freeform mode.
  - `Drawing Mode`: Toggle between Freeform and Rectangle modes.

- **Contour Settings**:
  - `Minimum Contour Area`: Adjust the minimum contour area for detecting fish.

- **Video Processing**:
  - `Start Video`: Processes the selected video, applying the mask, and saves the processed video file with a unique filename.

---

### Detailed Steps

#### 1. Creating a Mask
   - Click **Create Mask** to start.
   - Choose a drawing mode (Freeform or Rectangle).
   - Draw the mask over the regions to exclude fish detection.
   - Press `Enter` to finish, then name and save the mask.

#### 2. Processing a Video
   - Select a video file by clicking **Select Video** or use the default `BW.mp4`.
   - Choose an existing mask or skip to process without a mask.
   - Click **Start Video** to begin processing.
   - The processed video will be saved with the format:
     ```
     <video_name>_<mask_name>_<fish_count>_fish_<timestamp>.mp4
     ```
   - Results are logged in `Results/results.csv`.

#### 3. Viewing Results
   - Open `Results/results.csv` to view all saved records, including:
     - Mask Name
     - Video File
     - Fish Count
     - Processed Video Path
     - Timestamp

---

## Directory Structure
Here's a breakdown of the main directories and files in the project:

```
fish-finder-app/
├── helpers/
│   └── mask_creator.py            # Handles mask creation and saving
├── services/
│   ├── video_processor.py         # Handles video processing and fish counting
│   ├── result_saver.py            # Handles saving results to CSV
│   └── fish_finder_app.py         # Main app with GUI setup
├── Videos/
│   └── BW.mp4                     # Default example video
├── processed_videos/              # Directory for saving processed videos
├── Results/
│   └── results.csv                # CSV file with processed video logs
├── main.py                        # Main script to run the application
└── README.md                      # Project documentation
```

---

## Required Pip Packages

Here’s a list of the required pip packages:

- **opencv-python-headless**: For video processing without GUI.
- **numpy**: For handling numerical operations.
- **pillow**: Adds image support for Tkinter in Windows (optional but recommended).

---

## Troubleshooting

1. **Video not found**:
   - Ensure the video file exists in the `Videos/` directory or update the path in the application.

2. **Mask or video not loading**:
   - Ensure that mask files are saved in `saved_masks/` and have valid `.npy` format.
   - Confirm the default video path or select a video manually.

3. **Dependencies not installed**:
   - Ensure all required pip packages are installed. Use `pip list` to verify installations.

---

## License
This project is licensed under the MIT License.
