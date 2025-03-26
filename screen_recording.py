import cv2
import numpy as np
import mss

# Functie om het scherm vast te leggen
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Pak het eerste scherm (of pas aan als je een ander scherm gebruikt)
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Converteer naar normaal BGR-formaat voor OpenCV

# Live beeld tonen in een venster
while True:
    frame = capture_screen()
    cv2.imshow("Live Scherm", frame)

    # Stoppen als je op 'q' drukt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
