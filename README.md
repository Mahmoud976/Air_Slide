# AirSlide ✋🎤

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0F172A,50:155E75,100:22D3EE&text=AirSlide&fontColor=FFFFFF&fontSize=70&fontAlignY=38&desc=Hands-free%20presentation%20control&descAlignY=60&descSize=17&animation=fadeIn" width="100%" alt="AirSlide animated header" />
</p>

<p align="center"><strong>Control your presentation with hand gestures using Python and computer vision.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-0097A7?style=for-the-badge" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/PyAutoGUI-Keyboard%20Control-16A34A?style=for-the-badge" alt="PyAutoGUI" />
</p>

<p align="center">
  <a href="#features">Features</a> · <a href="#how-it-works">How it works</a> · <a href="#getting-started">Get started</a> · <a href="#gesture-controls">Gestures</a>
</p>

---

## What is AirSlide?

AirSlide turns your webcam into a simple, hands-free presentation controller. It detects one hand, recognizes an open palm or a fist, and tracks horizontal hand movement to send the appropriate arrow-key press to the active presentation.

The goal is to make presenting more natural when a physical clicker is unavailable, using a lightweight Python application and a standard webcam.

> **Current scope:** AirSlide sends keyboard inputs. Keep your PowerPoint slide show focused when using it. Test navigation in your own setup before relying on it during a live presentation.

## Features

- **Hands-free slide navigation:** move an open hand left or right to navigate.
- **Gesture-based pause and resume:** make a fist to pause control; show an open palm to resume.
- **Real-time hand landmarks:** MediaPipe detects and tracks hand points.
- **Visual status overlay:** see whether the controller is ready, paused, or navigating.
- **Gesture stability check:** waits for a gesture to remain consistent before switching modes.
- **Movement threshold and cooldown:** helps reduce accidental repeated slide changes.
- **Safety stop:** press Q or Esc to exit; PyAutoGUI's fail-safe remains enabled.

## How it works

1. **Capture:** OpenCV reads a frame from the webcam and flips it for a mirror-like view.
2. **Track:** MediaPipe Hands detects landmarks for one hand.
3. **Recognize:** AirSlide estimates whether the hand is open, closed, or another gesture.
4. **Check stability:** the gesture must remain consistent before it changes the controller mode.
5. **Measure movement:** horizontal wrist movement is compared with a configurable threshold.
6. **Control slides:** PyAutoGUI sends the left or right arrow key to the focused presentation.

## Gesture controls

| Gesture / action | Result |
|---|---|
| Show an open palm | Enable controls / prepare to navigate |
| Move an open hand right | Next slide (Right Arrow) |
| Move an open hand left | Previous slide (Left Arrow) |
| Make a fist | Pause gesture control |
| Show another gesture | Wait for an open palm |
| Press Q or Esc | Quit AirSlide |

**Tip:** Face your palm toward the camera, keep your hand clearly visible, and use deliberate horizontal movements. Lighting and camera position can affect detection.

## Tech stack

| Tool | Purpose |
|---|---|
| Python | Application logic |
| OpenCV | Webcam capture, image processing, and status window |
| MediaPipe Hands | Hand landmark detection |
| PyAutoGUI | Sends left/right arrow-key presses |
| time, math, collections | Timing, landmark distance, and movement history |

## Getting started

### Requirements

- A compatible Python environment (tested with Python 3.11 on Windows).
- A working webcam.
- PowerPoint or another presentation app that supports left/right arrow-key navigation.

### 1. Clone the repository

    git clone https://github.com/Mahmoud976/Air_Slide.git
    cd Air_Slide

### 2. Create and activate a virtual environment

**Windows — Git Bash**

    python -m venv .venv
    source .venv/Scripts/activate

**Windows — PowerShell**

    py -3.11 -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1

### 3. Install dependencies

    python -m pip install --upgrade pip
    pip install -r requirements.txt

### 4. Run AirSlide

    python airslide.py

A webcam window named **AirSlide Controller** should appear. Use an open palm to enable control, move horizontally to navigate, and press Q or Esc to exit.

## Configuration

The main settings are near the top of airslide.py:

| Setting | Default | Purpose |
|---|---:|---|
| CAMERA_INDEX | 0 | Webcam device index |
| COOLDOWN | 1.2 seconds | Minimum time between slide actions |
| MOVEMENT_THRESHOLD | 0.12 | Horizontal movement needed to trigger navigation |
| CALIBRATION_FRAMES | 8 frames | Number of tracked positions used to evaluate movement |

If your webcam is not the default camera, try changing CAMERA_INDEX. Adjust movement sensitivity gradually: a smaller threshold is more sensitive, while a larger one requires a bigger movement.

## Development and test scripts

The repository includes separate scripts to test the main building blocks:

- **camera_test.py** — verify webcam access.
- **hand_tracking_test.py** — inspect hand landmark tracking.
- **gesture_test.py** — test open-hand, fist, and other-gesture classification.
- **airslide.py** — run the complete controller.

Run a test script from the project directory, for example:

    python camera_test.py
    python hand_tracking_test.py
    python gesture_test.py

## Safety notes

- Start with a test presentation, not an important live presentation.
- Keep the presentation window focused; AirSlide sends system keyboard input.
- Quit with Q or Esc if tracking behaves unexpectedly.
- PyAutoGUI's fail-safe is enabled. Moving the mouse to the upper-left corner can trigger its safety stop.
- Do not rely on this as a safety-critical control without additional testing.

## Roadmap

- [ ] Add a short demo GIF or video to the repository.
- [ ] Add an optional calibration mode for different camera positions.
- [ ] Improve gesture recognition across hand orientations and lighting conditions.
- [ ] Add configurable controls and sensitivity settings.
- [ ] Package the application for easier setup.

## Contributing

Suggestions, bug reports, and pull requests are welcome. For a useful bug report, include your operating system, Python version, webcam setup, and steps to reproduce the issue.

## License

No license file has been added yet. Add a license before explicitly permitting reuse or redistribution.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&height=90&color=0:22D3EE,50:155E75,100:0F172A&section=footer&animation=fadeIn" width="100%" alt="Animated footer" />
</p>
