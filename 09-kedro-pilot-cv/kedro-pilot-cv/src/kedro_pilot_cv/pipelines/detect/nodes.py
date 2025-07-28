import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO


def vertical_scroll_hand(
    model_path: str,
    scroll_threshold: float,
    scroll_sensitivity: float,
) -> None:
    """
    1) Run YOLOv8-seg to get the person mask.
    2) Crop out the lower half so only the hand remains.
    3) Find the hand contour and compute its centroid.
    4) Map vertical movement of that centroid to scroll events.
    """
    model = YOLO(model_path, task="segment")
    cap = cv2.VideoCapture(0)
    prev_cy = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mirror image
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # 1) Inference
        seg = model.predict(frame)[0]
        if seg.masks is None:
            cv2.imshow("Hand Scroll", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # 2) Extract only the “person” mask (COCO class 0)
        person_mask = None
        for cls, m in zip(seg.boxes.cls.cpu().numpy(), seg.masks.data.cpu().numpy()):
            if int(cls) == 0:
                person_mask = (m * 255).astype(np.uint8)
                break
        if person_mask is None:
            cv2.imshow("Hand Scroll", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # 3) Crop out lower half (body)
        person_mask[h // 2 :, :] = 0

        # 4) Clean up noise
        kernel = np.ones((5, 5), np.uint8)
        mask_clean = cv2.erode(person_mask, kernel, iterations=1)
        mask_clean = cv2.dilate(mask_clean, kernel, iterations=1)

        # 5) Find the largest contour (your hand)
        contours, _ = cv2.findContours(
            mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            cv2.imshow("Hand Scroll", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue
        cnt = max(contours, key=cv2.contourArea)

        # 6) Compute centroid of the hand contour
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cy = int(M["m01"] / M["m00"])
        cx = int(M["m10"] / M["m00"])

        # 7) Draw centroid for debug
        cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)

        # 8) Vertical motion → scroll
        if prev_cy is not None:
            delta_y = cy - prev_cy
            if abs(delta_y) > scroll_threshold:
                amt = int((delta_y / scroll_threshold) * scroll_sensitivity)
                pyautogui.scroll(-amt)
        prev_cy = cy

        # 9) Debug display: side-by-side frame & resized mask
        debug_mask = cv2.cvtColor(mask_clean, cv2.COLOR_GRAY2BGR)
        debug_mask = cv2.resize(debug_mask, (w, h))
        combined = np.hstack([frame, debug_mask])
        cv2.imshow("Hand Scroll", combined)

        # 10) Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
