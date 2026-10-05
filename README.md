# QUT Rover OCR

This project contains a ROS 2 package that uses EasyOCR to find text in images from a camera. When text is found, the program shows the camera image, the image with a box around the text, and the OCR result in a window.

## Project location

The ROS 2 workspace is the `Rover_OCR_Node` folder. The main program is here:

```text
QUT_ROVER_OCR-main/Rover_OCR_Node/src/rover_ocr_node/rover_ocr_node/rover_ocr.py
```

The package files are in `Rover_OCR_Node/src/rover_ocr_node/`.

```text
QUT_ROVER_OCR-main/
├── README.md
└── Rover_OCR_Node/
    └── src/
        └── rover_ocr_node/
            ├── package.xml
            ├── setup.py
            └── rover_ocr_node/
                └── rover_ocr.py
```

The `build`, `install` and `log` folders are created by `colcon build`. They are not the source code for the package.

## Requirements

The project was set up for Ubuntu 22.04 and ROS 2 Humble. It uses EasyOCR, OpenCV, NumPy, Pillow, Tkinter and `rclpy`.

Install the ROS build tools and Tkinter if they are not already installed:

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-tk
```

Install the package dependencies with `rosdep` from the workspace folder:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## Build and run

Open a terminal and move into the ROS 2 workspace. If the project was extracted into its original folder, run:

```bash
cd QUT_ROVER_OCR-main/Rover_OCR_Node
```

Source ROS 2 Humble, build the package, and source the workspace:

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

Run the OCR node:

```bash
ros2 run rover_ocr_node rover_ocr
```

The program opens a window for the slideshow and starts reading from the camera. The first run of EasyOCR may take longer while its English model is loaded.

## Using the program

The program checks every 120th camera frame for text. When it finds text, it stores the image, an image with a box around the detected text, and the OCR result. Use the `<` and `>` buttons to move between stored results.

The camera is set to device `0` in `rover_ocr.py`:

```python
cap = cv.VideoCapture(0)
```

This normally selects the computer's default camera. If the rover camera uses a different camera number, change `0` to the correct number. The computer must also be able to access the camera.

## Troubleshooting

- **The camera does not open:** Check that it is connected, that another program is not using it, and that the camera number in `rover_ocr.py` is correct.
- **`ros2 run` cannot find the package:** Make sure the build completed and that `source install/setup.bash` was run from `Rover_OCR_Node` in the current terminal.
- **The window does not open:** Run the program from a desktop session with a display. If Tkinter is missing, install `python3-tk`.
- **EasyOCR takes a long time to start:** It may be loading its model for the first time. Allow the first startup to finish before trying again.

Press `Ctrl+C` in the terminal to stop the ROS 2 node.
