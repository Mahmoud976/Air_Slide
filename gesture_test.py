
import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def distance(point1, point2):
    return math.hypot(
        point1.x - point2.x,
        point1.y - point2.y
    )


def recognize_gesture(hand_landmarks):
    points = hand_landmarks.landmark

    # Finger tips and their middle joints
    fingers = [
        (8, 6),    # Index
        (12, 10),  # Middle
        (16, 14),  # Ring
        (20, 18)   # Pinky
    ]

    extended_fingers = 0

    for tip, joint in fingers:
        if distance(points[tip], points[0]) > distance(points[joint], points[0]):
            extended_fingers += 1

    # Thumb check
    if distance(points[4], points[0]) > distance(points[3], points[0]):
        extended_fingers += 1

    if extended_fingers >= 4:
        return "OPEN HAND"

    if extended_fingers <= 1:
        return "FIST"

    return "OTHER GESTURE"


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    print("AirSlide Gesture Recognition started.")
    print("Show an open hand, then make a fist.")
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
                success, frame = camera.read()

                if not success:
                    print("ERROR: Could not read webcam.")
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                status = "SHOW YOUR HAND"

                if results.multi_hand_landmarks:
                    for hand in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            frame,
                            hand,
                            mp_hands.HAND_CONNECTIONS
                        )
                        status = recognize_gesture(hand)

                cv2.putText(
                    frame,
                    status,
                    (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("AirSlide - Gesture Test", frame)

                key = cv2.waitKey(10)
                if key != -1 and (key & 0xFF) in (ord("q"), 27):
                    break

                if cv2.getWindowProperty(
                    "AirSlide - Gesture Test",
                    cv2.WND_PROP_VISIBLE
                ) < 1:
                    break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("AirSlide stopped.")


if __name__ == "__main__":
    main()
