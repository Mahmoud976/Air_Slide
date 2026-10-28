
import cv2
import mediapipe as mp
import pyautogui
import time
import math
from collections import deque

# ---------- Settings ----------
CAMERA_INDEX = 0
COOLDOWN = 0.60
MOVEMENT_THRESHOLD = 0.065
SMOOTHING_FRAMES = 3

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

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

    # Smooth noisy wrist landmarks with a short median window. Unlike the
    # previous long frame-history check, this can detect quick hand movements.
    wrist_history = deque(maxlen=SMOOTHING_FRAMES)
    anchor_x = None
    last_action_time = 0
    armed = True
    previous_gesture = None
    gesture_frames = 0
    status = "SHOW YOUR HAND"

    print("AirSlide started.")
    print("Open palm: enable movement control.")
    print("Fist: pause control.")
    print("Move your open hand LEFT or RIGHT to change slides.")
    print("Keep PowerPoint Slide Show active when testing.")
    print("Press Q or ESC to quit.")

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
                    status = "CAMERA FRAME UNAVAILABLE"
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                now = time.monotonic()
                movement_delta = 0.0

                if result.multi_hand_landmarks:
                    hand = result.multi_hand_landmarks[0]
                    mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                    gesture = recognize_gesture(hand)
                    wrist_x = hand.landmark[0].x

                    if gesture == previous_gesture:
                        gesture_frames += 1
                    else:
                        previous_gesture = gesture
                        gesture_frames = 1

                    if gesture_frames >= 4:
                        if gesture == "FIST":
                            armed = False
                            anchor_x = None
                            wrist_history.clear()
                            status = "PAUSED - OPEN PALM TO ENABLE"

                        elif gesture == "OPEN HAND":
                            if not armed:
                                armed = True
                                anchor_x = None
                                wrist_history.clear()
                                status = "CONTROL ENABLED - HOLD STILL"
                            else:
                                wrist_history.append(wrist_x)
                                smoothed_x = sorted(wrist_history)[len(wrist_history) // 2]

                                if anchor_x is None and len(wrist_history) >= 3:
                                    anchor_x = smoothed_x
                                    status = "READY - MOVE LEFT OR RIGHT"
                                elif anchor_x is not None:
                                    movement_delta = smoothed_x - anchor_x

                                    if abs(movement_delta) >= MOVEMENT_THRESHOLD:
                                        if now - last_action_time >= COOLDOWN:
                                            direction = "right" if movement_delta > 0 else "left"
                                            pyautogui.press(direction)
                                            status = "NEXT SLIDE" if direction == "right" else "PREVIOUS SLIDE"
                                            last_action_time = now
                                            # One deliberate movement = one key press.
                                            # Re-anchor so holding the hand in place
                                            # does not repeatedly change slides.
                                            anchor_x = smoothed_x
                                        else:
                                            status = "WAIT - COOLDOWN"
                                    else:
                                        status = "READY - MOVE LEFT OR RIGHT"
                        else:
                            anchor_x = None
                            wrist_history.clear()
                            status = "OTHER GESTURE - SHOW OPEN PALM"
                else:
                    previous_gesture = None
                    gesture_frames = 0
                    anchor_x = None
                    wrist_history.clear()
                    status = "SHOW YOUR HAND"

                cv2.putText(
                    frame, status, (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                    (0, 255, 0), 2
                )
                mode = "ENABLED" if armed else "PAUSED"
                cv2.putText(
                    frame, f"Control: {mode}", (15, 68),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                    (255, 200, 0), 2
                )
                cv2.putText(
                    frame, f"Movement: {movement_delta:+.3f}", (15, 101),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 255, 255), 1
                )

                cv2.imshow("AirSlide Controller", frame)
                key = cv2.waitKey(1)
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
