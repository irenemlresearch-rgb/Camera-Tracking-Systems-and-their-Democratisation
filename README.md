# Camera Tracking Systems and their Democratisation
This project, which won the SMPTE 2024 Student Paper of the Year, evaluates free, publicly available camera-tracking tools and compares them with a custom OpenCV-based tracker. It also analyses how noise and resolution influence tracking performance.\

The motivation, methodology and outputs of this project are discussed in the paper [Camera Tracking Systems and their Democratisation](https://drive.google.com/file/d/1x1OWxxz59aBONJdz1HWx0qFFFp7Ncs5y/view?usp=share_link).\
Reading the paper is recomended before experimenting with the scripts below.\
For example videos of the tracking output follow [this Link](https://drive.google.com/drive/folders/1cseqY5Spty1Kzi8FG00lxmJGFAsL__Nf?usp=share_link)

## 1_OpenCV_Smooth_Tracker
The first script:
- Reads a video
- Tracks ORB features using optical flow
- Estimates camera rotation and translation between frames
- Computes the yaw angle from the rotation
- Integrates translations to estimate a camera path
- Computes:
  - a running average of the camera coordinates to smooth the motion
  - a decaying/exponential moving average of the rotation matrices
- Displays tracked points on the video
- Saves:
  - Camera_coordinates.txt (raw camera trajectory)
  - running_avg_coordinates.txt (smoothed trajectory)

## 2.UnrealSequenceAndCamera
The second script is meant to be run from Unreal Engine.

After opening an Unreal Engine project:
- Tools
  - Execute Python Script

This script creates a camera and a sequence in your Unreal Project.\
The sequence is vital for further steps.

## 3.InsertCoordinatesToUnreal

The third script is meant to be run from Unreal Engine.

Again, after opening an Unreal Engine project:
- Tools
  - Execute Python Script

This script will populate the Sequence created with __2.UnrealSequenceAndCamera.py__ with the coordinates files from the video recorded with __1_OpenCV_Smooth_Tracker__


## 4.ExtractingCoordinatesFromUnrealAndNormalise

The third script is meant to be run from Unreal Engine.

Again, after opening an Unreal Engine project:
- Tools
  - Execute Python Script

This script will extract the coordinates from the Unreal Engine Sequence created with __2.UnrealSequenceAndCamera.py__ and __1_OpenCV_Smooth_Tracker__ and normalises them.\
This is good to plot anc compare the coordinates from different tracking systems.
