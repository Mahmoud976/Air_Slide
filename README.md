# AirSlide ✋🎤

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0F172A,50:155E75,100:22D3EE&text=AirSlide&fontColor=FFFFFF&fontSize=70&fontAlignY=38&desc=Hands-free%20presentation%20control&descAlignY=60&descSize=17&animation=fadeIn" width="100%" alt="AirSlide animated header" />
</p>

<p align="center">
  <a href="https://readme-typing-svg.demolab.com">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=19&pause=900&color=22D3EE&center=true&vCenter=true&width=1200&lines=Control+your+presentation+with+hand+gestures+using+Python+and+computer+vision." alt="Control your presentation with hand gestures using Python and computer vision." />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-0097A7?style=for-the-badge" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/PyAutoGUI-Keyboard%20Control-16A34A?style=for-the-badge" alt="PyAutoGUI" />
</p>

<p align="center">
  <a href="#features">Features</a> · <a href="#how-it-works">How it works</a> · <a href="#getting-started">Get started</a> · <a href="#windows-exe">Windows EXE</a> · <a href="#gesture-controls">Gestures</a> · <a href="#configuration">Configuration</a>
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
- **Responsive movement detection:** uses a short median-smoothed wrist position instead of waiting for a long movement window.
- **One movement, one key press:** resets the movement anchor after each slide action to reduce missed gestures and repeated triggers.
- **Gesture stability check and cooldown:** filters noisy gesture changes while keeping slide navigation responsive.
- **Safety stop:** press Q or Esc to exit; PyAutoGUI's fail-safe remains enabled.

## How it works

1. **Capture:** OpenCV reads a frame from the webcam and flips it for a mirror-like view.
2. **Track:** MediaPipe Hands detects landmarks for one hand.
3. **Recognize:** AirSlide estimates whether the hand is open, closed, or another gesture.
4. **Check stability:** the gesture must remain consistent before it changes the controller mode.
5. **Smooth movement:** a short rolling median reduces wrist-tracking jitter.
6. **Detect a slide gesture:** movement is measured from the current anchor; after a key press, the anchor resets so a held position does not repeatedly trigger.
7. **Control slides:** PyAutoGUI sends the left or right arrow key to the focused presentation.

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

## Windows EXE

**AirSlide can be packaged as a standalone Windows application** so you can run it without installing Python or the project dependencies separately.

### Download

- **[GitHub Releases — permanent downloads](https://github.com/Mahmoud976/Air_Slide/releases/latest)** — use this page for versioned releases when one is published.
- [GitHub Actions — latest build runs](https://github.com/Mahmoud976/Air_Slide/actions/workflows/build-windows-exe.yml) — the CI build artifact is temporary and expires after 14 days.

To download a successful Actions build:
1. Open the workflow runs page above and select the latest successful **Build Windows EXE** run.
2. Under **Artifacts**, download `AirSlide-Windows`.
3. Extract the ZIP and run `AirSlide.exe`.

> **Artifact vs. Release:** Actions artifacts are temporary CI outputs. A GitHub Release is the permanent, versioned download page. The release workflow is available under **Actions → Publish Windows Release**; run it with a version such as `v1.0.0` to build the EXE and attach it to a release.

### Build it yourself on Windows

1. Install Python 3.11 and Git.
2. Clone the repository and open its folder.
3. Double-click `build_exe.bat`.
4. After the build completes, run `dist\\AirSlide.exe`.

The single-file executable is approximately **237 MiB** because it bundles Python, OpenCV, and MediaPipe. First launch can take longer while bundled files are unpacked. Windows Defender or other security software may inspect a newly built executable.

**Before presenting:** Test the EXE with your webcam and a test slide deck. Keep the presentation window focused because AirSlide sends keyboard input to the active window. CI confirms dependency/import checks and packaging; it does not replace a real webcam test on the target PC.

## Configuration

The main settings are near the top of airslide.py:

| Setting | Default | Purpose |
|---|---:|---|
| CAMERA_INDEX | 0 | Webcam device index |
| COOLDOWN | 0.60 seconds | Minimum time between slide actions |
| MOVEMENT_THRESHOLD | 0.065 | Normalized horizontal movement needed to trigger navigation |
| SMOOTHING_FRAMES | 3 frames | Short median window used to reduce tracking jitter |

If your webcam is not the default camera, try changing CAMERA_INDEX. If slides still do not change reliably, lower MOVEMENT_THRESHOLD slightly for more sensitivity; if accidental changes occur, raise it. The current defaults use a 3-frame median and a 0.065 movement threshold for quicker response, with a short keyboard-action pause. Use deliberate horizontal movements and keep your open palm visible to the camera.

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
- [x] Package a single-file Windows EXE with GitHub Actions.
- [x] Add a workflow to publish versioned Windows releases with the EXE attached.

## Contributing

Suggestions, bug reports, and pull requests are welcome. For a useful bug report, include your operating system, Python version, webcam setup, and steps to reproduce the issue.

## Author

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=170&color=0:0F172A,50:155E75,100:22D3EE&section=header&text=AUTHOR&fontColor=FFFFFF&fontSize=42&fontAlignY=38&animation=fadeIn" width="100%" alt="Author banner" />
</p>

<p align="center">
  <a href="https://readme-typing-svg.demolab.com">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&pause=1000&color=22D3EE&center=true&vCenter=true&width=900&lines=Mahmoud+Mohammed+El+Sayed+Saleh" alt="Mahmoud Mohammed El Sayed Saleh" />
  </a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/mahmoud-m-saleh/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect%20with%20Mahmoud-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Connect with Mahmoud on LinkedIn" />
  </a>
</p>

## License

This project is licensed under the [MIT License](LICENSE).

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=140&color=0:0F172A,50:155E75,100:22D3EE&section=footer&animation=twinkling&reversal=true" width="100%" alt="Animated footer banner" />
</p>
