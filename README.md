# 🎯 Real-Time Object Tracking and Statistical Analysis with OpenCV

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

## 📁 Output Files

- `tracked_output.mp4` – Optional video file of the tracking session.
- `tracking_stats.csv` – CSV file with object tracking stats.
- *(Optional)* `motion_paths.png` – Save the motion path visualization if desired.

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

##👩‍💻 Author
**Malak Nasser** <br>
📧 [E-mail](mallaknasser812@gmail.com) <br>
🔗 [LinkedIn](https://www.linkedin.com/in/malak-nasser-752ab0214/) 

