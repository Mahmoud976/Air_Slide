
import cv2
import mediapipe as mp

def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    print("AirSlide Hand Tracking started.")
    print("Show your hand to the camera.")
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

                rgb_frame = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                results = hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS
                        )

                    status = "Hand detected"
                else:
                    status = "Show your hand"

                cv2.putText(
                    frame,
                    status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("AirSlide - Hand Tracking", frame)

                key = cv2.waitKey(10)

                if key != -1 and (key & 0xFF) in (ord("q"), 27):
                    break

                if cv2.getWindowProperty(
                    "AirSlide - Hand Tracking",
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
