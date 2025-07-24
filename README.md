# 🎯 Real-Time Multi-object Tracking on Selection 

This project is a real-time multi-object tracking application using **OpenCV** and **Python**, where users can:
- Select and track multiple objects from a live webcam feed.
- Record tracking sessions as video, and save the recorded video.
- Analyze and save movement statistics such as distance and speed.
- Plot the motion path of each tracked object.

---

## 📦 Features

### ✅ Real-Time Object Tracking
- Press **`s`** to select one or more objects using your mouse.
- Each object is given a unique ID and tracked continuously.
- Tracking overlays include bounding boxes and labels.

### ✅ Tracker Management
- Press **`u`** to stop tracking all currently selected objects.
- Previously tracked objects are not lost; their history remains saved.

### ✅ Video Recording
- Press **`r`** to start recording the live stream.
- Press **`x`** to stop and save the video.

### ✅ Post-Tracking Statistics
- Press **`q`** to quit the app
After quitting the app:
- The application computes the **total distance traveled** and **average speed** for each tracked object.
- All stats are saved as `tracking_stats.csv`.
- Motion paths are visualized using `matplotlib`.
- Recorded video (if found) will be saved as 'tracked_output.mp4'

---
## 🛠 Implementation Details

### 📌 1. Initialization

- The system uses `cv2.VideoCapture(0)` to open the webcam stream.
- All active and archived tracked objects are managed using two lists:
  - `active_trackers`: stores objects currently being tracked.
  - `all_trackers`: stores all objects ever tracked for analysis, even if unselected.

```python
cap = cv2.VideoCapture(0)
active_trackers = []
all_trackers = []

```

### 🧠 2. TrackedObject Class
- Each object selected for tracking is wrapped in a custom class to store:
- The tracker object (cv2.legacy.TrackerCSRT_create())
- The ROI selected by the user
- A unique ID
- A list of its center positions during motio
- Start and end frame indices (used to calculate duration)
- A flag active indicating whether it's still being tracked

```python
class TrackedObject:
    def __init__(self, tracker, roi, object_id, start_frame):
        self.tracker = tracker
        self.roi = roi
        self.id = object_id
        self.positions = []
        self.start_frame = start_frame
        self.end_frame = start_frame
        self.active = True
```
### 🎥 3. Object Tracking Loop
- Each frame is processed in a loop.
- If an object is active, the system updates its tracker.
- If tracking is successful, the new bounding box is drawn and the object’s center is recorded.
- If tracking fails (e.g. object moves out of frame), it is marked as inactive but not deleted.
```python
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
```


### 🖱 4. User Controls
- s: User selects a new object using cv2.selectROI. A new tracker is initialized and added.
- u: Clears all active trackers but keeps the history in all_trackers.
- r: Starts recording the live feed into tracked_output.mp4.
- x: Stops and saves the video file.
- q: Quits the application and generates final analysis.


### 📈 5. Motion Analysis
- After quitting, statistics are computed for each tracked object:
- Total Distance: Sum of Euclidean distances between consecutive center points.
- Average Speed: Total distance divided by number of frames.

```python
distances = [
np.linalg.norm(np.array(obj.positions[i + 1]) - np.array(obj.positions[i]))
                     for i in range(len(obj.positions) - 1)
]
total_distance = sum(distances)
avg_speed = total_distance / lifetime if lifetime > 0 else 0
```


### 📊 6. Visualization and Export
- A trajectory plot is created using matplotlib, showing the path each object followed.
- A CSV file tracking_stats.csv is saved with summary metrics for each object:
  - Object ID
  - Total distance
  - Average speed


### 💾 Outputs
- tracked_output.mp4: Optional recording of the session.
- tracking_stats.csv: Table of object motion statistics.
- Matplotlib motion plot (displayed, can be saved if needed).


---
## 🚀 Instructions for Deployment

Follow the steps below to set up and run the application locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/object-tracking-opencv.git
cd object-tracking-opencv
```
### 2️⃣ Install Dependencies
```bash
pip install opencv
pip install imutils 
pip install matplotlib 
pip install pandas 
pip install numpy
```
### 3️⃣ Run the file

---

## 👩‍💻 Author
**Malak Nasser** | AI Engineer <br>
📧 [E-mail](mallaknasser812@gmail.com) <br>
🔗 [LinkedIn](https://www.linkedin.com/in/malak-nasser-752ab0214/) 

