
import cv2

def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Webcam could not be opened.")
        return

    print("AirSlide webcam test started.")
    print("Click the camera window, then press Q or ESC to quit.")
    print("You can also close the camera window using X.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Failed to read webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            cv2.imshow("AirSlide", frame)

            key = cv2.waitKey(10)

            if key != -1 and (key & 0xFF) in (ord("q"), 27):
                print("Exit key detected.")
                break

            if cv2.getWindowProperty(
                "AirSlide", cv2.WND_PROP_VISIBLE
            ) < 1:
                print("Camera window closed.")
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("Camera released. Program stopped.")

if __name__ == "__main__":
    main()
