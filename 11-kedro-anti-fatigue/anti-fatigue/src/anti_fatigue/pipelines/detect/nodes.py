import os
import time
from collections import deque

import cv2
import matplotlib.pyplot as plt
import numpy as np


def detect_and_record(
    video_source: int,
    eye_closed_frames: int,
    yawn_frames: int,
    scale_factor_eye: float,
    min_neighbors_eye: int,
    scale_factor_smile: float,
    min_neighbors_smile: int,
    record_dir: str,
    pre_buffer_secs: int,
    post_record_secs: int
) -> None:
    """
    Live webcam detection of blinks & yawns. On each yawn, record
    pre_buffer_secs before the event and post_record_secs after into a video.
    """
    # --- Setup Haar cascades ---
    eye_cascade   = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml"
    )
    smile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_smile.xml"
    )

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {video_source}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    pre_buffer_n = int(fps * pre_buffer_secs)
    post_buffer_n = int(fps * post_record_secs)

    # rolling buffer for last N frames
    frame_buffer = deque(maxlen=pre_buffer_n)

    os.makedirs(record_dir, exist_ok=True)

    # Matplotlib setup for timeline
    plt.ion()
    fig, ax = plt.subplots()
    xs, ys = [], []
    evt_map = {"blink": 1, "yawn": 2}
    ax.set_yticks([1,2]); ax.set_yticklabels(["Blink","Yawn"])
    ax.set_xlabel("Time (s)"); ax.set_title("Event Timeline")

    start_t = time.time()
    blink_ctr = yawn_ctr = 0
    recording = False
    writer = None
    post_count = 0

    print("▶️  Press [q] in the video window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_buffer.append(frame.copy())

        # detect eyes
        eyes = eye_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor_eye,
            minNeighbors=min_neighbors_eye,
            minSize=(30,30)
        )
        # detect smiles
        smiles = smile_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor_smile,
            minNeighbors=min_neighbors_smile,
            minSize=(60,60)
        )

        event = ""
        # blink logic
        if len(eyes) == 0:
            blink_ctr += 1
            if blink_ctr >= eye_closed_frames:
                event = "Blink"
                blink_ctr = 0
                ts = time.time() - start_t
                xs.append(ts); ys.append(evt_map["blink"])
        else:
            blink_ctr = 0

        # yawn logic
        if len(smiles) > 0:
            yawn_ctr += 1 if 'yawn_ctr' in locals() else 1
            if yawn_ctr >= yawn_frames and not recording:
                event = "Yawn"
                yawn_ctr = 0
                ts = time.time() - start_t
                xs.append(ts); ys.append(evt_map["yawn"])
                # start recording
                fname = f"yawn_{int(time.time())}.avi"
                path = os.path.join(record_dir, fname)
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                h, w = frame.shape[:2]
                writer = cv2.VideoWriter(path, fourcc, fps, (w, h))
                # dump buffered frames
                for buf in frame_buffer:
                    writer.write(buf)
                recording = True
                post_count = 0
        else:
            # reset if no smile
            if 'yawn_ctr' in locals():
                yawn_ctr = 0

        # if recording after yawn, write current frame and count down
        if recording:
            writer.write(frame)
            post_count += 1
            if post_count >= post_buffer_n:
                writer.release()
                recording = False
                print(f"✅ Saved yawn clip to {path}")

        # overlay
        if event:
            cv2.putText(
                frame, event, (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2
            )

        cv2.imshow("Fatigue Detector", frame)

        # update plot
        ax.clear()
        ax.set_yticks([1,2]); ax.set_yticklabels(["Blink","Yawn"])
        ax.set_xlabel("Time (s)"); ax.set_title("Event Timeline")
        if xs:
            ax.plot(xs, ys, marker="o", linestyle="-")
        fig.canvas.draw(); plt.pause(0.001)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.ioff(); plt.show()
