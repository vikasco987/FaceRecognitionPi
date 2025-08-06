import threading
import time
import cv2
import config

CAPTURE_HZ = 30.0  # Target FPS

class OpenCVCapture:
    def __init__(self, device_id=0):
        self._camera = cv2.VideoCapture(device_id)
        if not self._camera.isOpened():
            raise Exception("Webcam not found or can't be opened.")

        self._capture_frame = None
        self._running = True
        self._capture_lock = threading.Lock()

        # Start capture thread
        self._capture_thread = threading.Thread(target=self._grab_frames, daemon=True)
        self._capture_thread.start()

    def _grab_frames(self):
        while self._running:
            ret, frame = self._camera.read()
            with self._capture_lock:
                self._capture_frame = frame if ret else None
            time.sleep(1.0 / CAPTURE_HZ)

    def read(self):
        with self._capture_lock:
            return self._capture_frame.copy() if self._capture_frame is not None else None

    def stop(self):
        self._running = False
        self._capture_thread.join()
        self._camera.release()


if __name__ == "__main__":
    cam = None
    last_save_time = 0
    SAVE_INTERVAL = 5  # seconds

    try:
        cam = OpenCVCapture()
        print("Press 'q' or ESC to quit.")

        while True:
            frame = cam.read()
            if frame is not None:
                # Optionally save every 5s
                # current_time = time.time()
                # if current_time - last_save_time > SAVE_INTERVAL:
                #     cv2.imwrite(config.Recent_Image, frame)
                #     last_save_time = current_time

                cv2.imshow("Live Webcam Preview", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                print("Exiting webcam preview...")
                break

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        if cam:
            cam.stop()
        cv2.destroyAllWindows()
