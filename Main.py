import cv2
import imutils
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

# ========== Setup ==========
cap = cv2.VideoCapture(0)
output_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracked_output.mp4")
recording = False
writer = None
object_id = 0
frame_count = 0


# Define a custom tracked object class
class TrackedObject:
    def __init__(self, tracker, roi, object_id, start_frame):
        self.tracker = tracker
        self.roi = roi
        self.id = object_id
        self.positions = []
        self.start_frame = start_frame
        self.end_frame = start_frame
        self.active = True

# List of all tracked objects
active_trackers = [] # holds the active trackers
all_trackers = []    # holds all tracked objects for statistical analysis

# ========== Main Loop ==========
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, 900)
    frame = cv2.flip(frame, 1)
    frame_count += 1

    # Update all trackers
    for obj in active_trackers:
        if obj.active:
            success, box = obj.tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                center = (x + w // 2, y + h // 2)
                obj.positions.append(center) 
                obj.end_frame = frame_count

                # Draw rectangle and ID
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {obj.id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                cv2.putText(frame, 'TRACKING', (x, y - 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
            else:
                obj.active = False
                active_trackers.remove(obj)

    # Write video if recording
    if recording:
        writer.write(frame)
        cv2.putText(frame, "REC", (820, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Instructions
    cv2.putText(frame, "Press 's'=select, 'u'=clear, 'r'=record, 'x'=stop, 'q'=quit", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("Object Tracking - Malak Nasser", frame)
    k = cv2.waitKey(30)

    # === Select object ===
    if k == ord("s"):
        cv2.putText(frame, "Select ROI and press ENTER", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        roi = cv2.selectROI("Object Tracking - Malak Nasser", frame, fromCenter=False, showCrosshair=False)
        if roi != (0, 0, 0, 0):
            object_id += 1
            tracker = cv2.legacy.TrackerCSRT_create()
            tracker.init(frame, roi)
            tracked = TrackedObject(tracker, roi, object_id, frame_count)
            active_trackers.append(tracked)
            all_trackers.append(tracked)

    # === Unselect all ===
    if k == ord("u"):
        active_trackers = []

    # === Start recording ===
    if k == ord("r") and not recording:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        recording = True
        print("Recording started...")

    # === Stop recording ===
    if k == ord("x") and recording:
        recording = False
        writer.release()
        print("Recording stopped and saved as", output_filename)

    # === Quit ===
    if k == ord("q"):
        if recording:
            recording = False
            writer.release()
            print("Recording stopped and saved as", output_filename)
        break

# ========== Post-Tracking Statistics ==========
cap.release()
cv2.destroyAllWindows()

# Analyze and save stats
stats = []
for obj in all_trackers:
    lifetime = obj.end_frame - obj.start_frame
    if len(obj.positions) > 1:
        distances = [np.linalg.norm(np.array(obj.positions[i + 1]) - np.array(obj.positions[i]))
                     for i in range(len(obj.positions) - 1)]
        total_distance = sum(distances)

        # Plot the trajectory of the object
        positions = np.array(obj.positions)
        plt.plot(positions[:, 0], positions[:, 1], marker='o', label=f'Object ID {obj.id}')
        plt.text(positions[0, 0], positions[0, 1], f'Start {obj.id}', fontsize=8)
        plt.text(positions[-1, 0], positions[-1, 1], f'End {obj.id}', fontsize=8)

    else:
        total_distance = 0
    avg_speed = total_distance / lifetime if lifetime > 0 else 0

    stats.append({
        "Object ID": obj.id,
        "Total Distance (px)": round(total_distance, 2),
        "Average Speed (px/frame)": round(avg_speed, 2)
    })

# Plotting the motion paths
plt.title("Motion Paths of Tracked Objects")
plt.xlabel("X Position (pixels)")
plt.ylabel("Y Position (pixels)")
plt.legend()
plt.grid(True)
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()

# Create and export DataFrame
df = pd.DataFrame(stats)
print("\n Tracking Statistics:\n", df)
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracking_stats.csv")
df.to_csv(csv_path, index=False)
print(f"\n Stats saved to: {csv_path}")
