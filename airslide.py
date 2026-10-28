
import cv2
import mediapipe as mp
import pyautogui
import time
import math
from collections import deque

# ---------- Settings ----------
CAMERA_INDEX = 0
COOLDOWN = 1.2
MOVEMENT_THRESHOLD = 0.12
CALIBRATION_FRAMES = 8

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def recognize_gesture(hand):
    p = hand.landmark
    wrist = p[0]

    fingers = [(8, 6), (12, 10), (16, 14), (20, 18)]
    extended = sum(
        distance(p[tip], wrist) > distance(p[joint], wrist)
        for tip, joint in fingers
    )

    # Thumb estimate; works best with palm facing camera
    if distance(p[4], wrist) > distance(p[3], wrist):
        extended += 1

    if extended >= 4:
        return "OPEN HAND"
    if extended <= 1:
        return "FIST"
    return "OTHER"


def main():
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    last_x_positions = deque(maxlen=CALIBRATION_FRAMES)
    last_action_time = 0
    armed = True
    previous_gesture = None
    gesture_frames = 0

    print("AirSlide started.")
    print("Open palm: enable movement control.")
    print("Fist: pause control.")
    print("Move your open hand LEFT or RIGHT to change slides.")
    print("Keep PowerPoint Slide Show active when testing.")
    print("Press Q or ESC to quit.")
    print("Safety: no slide keys are sent until a movement is detected.")

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        ) as hands:

            while True:
                ok, frame = camera.read()
                if not ok:
                    print("ERROR: Could not read webcam.")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)

                status = "SHOW YOUR HAND"
                now = time.time()

                if result.multi_hand_landmarks:
                    hand = result.multi_hand_landmarks[0]
                    mp_draw.draw_landmarks(
                        frame, hand, mp_hands.HAND_CONNECTIONS
                    )

                    gesture = recognize_gesture(hand)
                    wrist_x = hand.landmark[0].x

                    if gesture == previous_gesture:
                        gesture_frames += 1
                    else:
                        previous_gesture = gesture
                        gesture_frames = 1

                    # Require a stable gesture before changing mode
                    if gesture_frames >= 5:
                        if gesture == "FIST":
                            armed = False
                            last_x_positions.clear()
                            status = "PAUSED - OPEN PALM TO ENABLE"

                        elif gesture == "OPEN HAND":
                            if not armed:
                                armed = True
                                last_x_positions.clear()
                                status = "CONTROL ENABLED - HOLD STILL"
                            else:
                                status = "READY - MOVE LEFT OR RIGHT"
                                last_x_positions.append(wrist_x)

                                if len(last_x_positions) == CALIBRATION_FRAMES:
                                    delta = last_x_positions[-1] - last_x_positions[0]

                                    if now - last_action_time >= COOLDOWN:
                                        if delta > MOVEMENT_THRESHOLD:
                                            pyautogui.press("right")
                                            status = "NEXT SLIDE"
                                            last_action_time = now
                                            last_x_positions.clear()

                                        elif delta < -MOVEMENT_THRESHOLD:
                                            pyautogui.press("left")
                                            status = "PREVIOUS SLIDE"
                                            last_action_time = now
                                            last_x_positions.clear()
                        else:
                            status = "OTHER GESTURE - HOLD OPEN PALM"

                else:
                    previous_gesture = None
                    gesture_frames = 0
                    last_x_positions.clear()

                cv2.putText(
                    frame, status, (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (0, 255, 0), 2
                )

                mode = "ENABLED" if armed else "PAUSED"
                cv2.putText(
                    frame, f"Control: {mode}", (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 200, 0), 2
                )

                cv2.imshow("AirSlide Controller", frame)

                key = cv2.waitKey(10)
                if key != -1 and (key & 0xFF) in (ord("q"), 27):
                    break

                if cv2.getWindowProperty(
                    "AirSlide Controller", cv2.WND_PROP_VISIBLE
                ) < 1:
                    break

    except pyautogui.FailSafeException:
        print("PyAutoGUI safety stop triggered.")

    finally:
        camera.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("AirSlide stopped.")


if __name__ == "__main__":
    main()
