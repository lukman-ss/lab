# Kedro Pilot CV

A Kedro-based project that uses Ultralytics YOLOv8 segmentation to detect a raised hand via webcam and map vertical hand movement to scroll events (e.g., scrolling a browser window). The pipeline runs as a Kedro pipeline named `detect`.

## Features

* YOLOv8 segmentation (using `task="segment"`) for person detection
* Hand region extraction by cropping upper half of the person mask
* Contour-based hand centroid computation
* Mapping vertical hand motion to OS scroll events via PyAutoGUI
* Side-by-side debug view (webcam frame + cleaned mask)
* Configurable parameters: model path, scroll threshold, sensitivity
* Modular structure using Kedro pipelines for easy extension

## Prerequisites

* Python 3.7+ (recommended 3.10 or 3.11 for compatibility)
* pip
* Git
* (Optional) Conda or pyenv for managing multiple Python versions

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/lukman-ss/lab.git
   cd 09-kedro-pilot-cv/kedro-pilot-cv
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure parameters**
   Edit `conf/base/parameters.yml` as needed:

   ```yaml
   model_path: "yolov8n-seg.pt"
   scroll_threshold: 20.0
   scroll_sensitivity: 5.0
   ```

   Ensure you have the `yolov8n-seg.pt` model downloaded or update to a different YOLOv8 segmentation model.

## Project Structure

```
kedro-pilot-cv/
├── conf/
│   └── base/
│       └── parameters.yml
├── data/
├── logs/
├── src/
│   ├── kedro_pilot_cv/
│   │   ├── pipelines/
│   │   │   └── detect/
│   │   │       ├── nodes.py
│   │   │       └── pipeline.py
│   │   └── pipeline_registry.py
│   └── requirements.txt
├── README.md
└── …
```

## Usage

Run the `detect` pipeline:

```bash
kedro run --pipeline detect
```

A window will open showing your mirrored webcam feed side-by-side with the cleaned mask. Raise your hand into the frame and move it **up** to scroll up, **down** to scroll down in your active application. Press `ESC` to exit.

## Customization

* **Model**: Update `model_path` in `parameters.yml` to use a different YOLOv8 segmentation weight.
* **Threshold**: Adjust `scroll_threshold` for how much hand movement is required to trigger a scroll.
* **Sensitivity**: Modify `scroll_sensitivity` to control scroll speed per threshold unit.

## Troubleshooting

* **Dependency Issues**: Ensure you're using a compatible Python version (3.10/3.11) and have installed all requirements.
* **Kedro Warnings**: If pipelines aren’t detected, verify that `pipeline_registry.py` and the `detect` pipeline folder exist under `src/kedro_pilot_cv/pipelines/`.

## License

This project is released under the MIT License.
