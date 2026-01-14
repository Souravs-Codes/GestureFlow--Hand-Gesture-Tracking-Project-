# GestureFlow ✋  
Real-Time Hand Gesture Interaction System

GestureFlow is a real-time hand gesture recognition and interaction system built using Python and computer vision. It enables intuitive human–computer interaction by detecting both hands, counting fingers from **1 to 10**, and mapping natural gestures to system controls such as volume adjustment.

---

## 🚀 Features

- 🖐️ Real-time **two-hand detection** using a webcam  
- 🔢 Finger counting from **1–10**
  - Left hand → **1–5**
  - Right hand → **6–10**
- 📍 Numbers displayed **above each hand**, stable and jitter-free  
- 🔊 Gesture-based **system volume control**
- 🔁 Toggle-based gesture modes to avoid accidental triggers  
- 🧠 Distance-based thumb detection (robust against camera mirroring)
- 🎯 Clean and minimal user interface

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- Pycaw (Windows system audio control)

---

## 🧩 How It Works

GestureFlow uses MediaPipe Hands to detect hand landmarks in real time.  
Custom gesture logic determines which fingers are open, with special handling for the thumb using distance-based detection rather than fragile directional checks.

Each hand is processed independently:
- The **left hand** represents numbers from **1 to 5**
- The **right hand** represents numbers from **6 to 10**


## 2️⃣ Install dependencies

```bash    
pip install -r requirements.txt
```
## 3️⃣ Run the application
``` bash
python VolumeHandControl.py
```


## 📂 Project Structure
├── VolumeHandControl.py # Main application

├── HandTrackingModule.py # Hand tracking utilities

├── requirements.txt # Dependencies

└── README.md # Documentation

## ⚠️ Notes:

Works best in good lighting

Uses your default webcam

Volume control is supported on Windows

## 🎮 Gesture Overview

| Gesture               | Action                |
| --------------------- | --------------------- |
| Open left hand        | Display numbers 1–5   |
| Open right hand       | Display numbers 6–10  |
| Thumb + ring finger   | Toggle volume control |
| Thumb + middle finger | Toggle skeleton view  |
| Finger distance       | Adjust system volume  |

## 💡 Key Learnings

1: Gesture systems depend heavily on logic design and UX

2: Thumbs require special handling due to biomechanics see

3: Stable UI anchors improve perceived accuracy

4: Preventing accidental triggers is critical for usability

## 📌 Future Improvements

1: Gesture stabilization (anti-flicker)

2: Smooth UI animations


Numbers are rendered **above the hand** using the top-most landmark, ensuring the display remains stable even when fingers bend or move. Gesture cooldowns are applied to prevent false triggers.

---
