
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy
from scipy.spatial.transform import Rotation


# Function to detect and track features, and estimate camera pose
def detect_and_track(frame, prev_frame, prev_points, K, reset_interval=30):
    # Convert frames to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    if prev_points is None or len(prev_points) < reset_interval:
        # Use a feature detector, e.g., ORB
        orb = cv2.ORB_create()
        keypoints, _ = orb.detectAndCompute(gray, None)
        prev_points = np.array([kp.pt for kp in keypoints], dtype=np.float32).reshape(-1, 1, 2)

    # Calculate optical flow
    next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None)

    # Filter out points that were not successfully tracked
    good_new = next_points[status == 1]
    good_old = prev_points[status == 1]

    # Draw red crosses on the frame
    marked_frame = frame.copy()
    for point in good_new:
        x, y = point.ravel()
        marked_frame = cv2.drawMarker(marked_frame, (int(x), int(y)), (0, 0, 255),
                                      markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)

    # Calculate essential matrix using the camera matrix
    E, _ = cv2.findEssentialMat(good_old, good_new, K)

    # Recover pose (rotation and translation) from essential matrix
    _, R, t, _ = cv2.recoverPose(E, good_old, good_new, K)

    # Convert rotation matrix to quaternion
    rotation_matrix = R
    rotation_quaternion = Rotation.from_matrix(rotation_matrix).as_quat()

    # Calculate yaw angle from quaternion
    yaw_angle = np.degrees(2 * np.arctan2(rotation_quaternion[3], rotation_quaternion[0]))
    print("Yaw Angle:", yaw_angle)

    return R, t, marked_frame, good_old, good_new, yaw_angle


# Input video file path
input_video_path = '' # HERE YOUR VIDEO

# Open the video file
cap = cv2.VideoCapture(input_video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Camera intrinsic parameters (replace with your camera parameters)
fx = 500.0  # focal length in x direction
fy = 500.0  # focal length in y direction
cx = width / 2.0  # principal point in x direction
cy = height / 2.0  # principal point in y direction

K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])

# Initialize variables for optical flow tracking
prev_frame = None
prev_points = None
rotations = []  # Array to store rotation matrices
translations = []  # Array to store translation vectors
camera_coordinates = []  # Array to store camera coordinates (x, y, z)
running_avg_coordinates = []  # Array to store running average coordinates
num_frames_for_avg = 10  # Number of frames to consider for running average
decaying_avg_rotations = []  # Array to store decaying average rotations
decay_factor = 0.1  # Decay factor for the exponential moving average


# Process each frame in the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect and track features, and estimate camera pose
    if prev_frame is not None and prev_points is not None:
        R, t, marked_frame, _, good_new = detect_and_track(frame, prev_frame, prev_points, K)
    else:
        R, t, marked_frame, _, good_new = detect_and_track(frame, frame, None, K)

    # Append the rotation and translation to the arrays
    rotations.append(R)
    translations.append(t)

    # Calculate camera coordinates
    if len(translations) > 1:
        # Integrate translation vectors over time to get camera trajectory
        cumulative_translation = np.sum(translations, axis=0)
        camera_coordinates.append(cumulative_translation.flatten())  # Flatten to make it 1D

        # Calculate running average coordinates
        if len(camera_coordinates) >= num_frames_for_avg:
            avg_coordinates = np.mean(camera_coordinates[-num_frames_for_avg:], axis=0)
            running_avg_coordinates.append(avg_coordinates)

   # Calculate decaying average rotations
        if len(rotations) > 1:
            last_avg_rotation = decaying_avg_rotations[-1] if decaying_avg_rotations else rotations[0]
            avg_rotations = last_avg_rotation * (1 - decay_factor) + R * decay_factor
            decaying_avg_rotations.append(avg_rotations)

    # Display the current frame with marked features
    cv2.imshow('Frame with Marked Features', marked_frame)

    # Set the current frame as the previous frame for the next iteration
    prev_frame = frame.copy()
    prev_points = good_new.reshape(-1, 1, 2)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Convert the lists to NumPy arrays
rotations = np.array(rotations)
translations = np.array(translations)
camera_coordinates = np.array(camera_coordinates)
running_avg_coordinates = np.array(running_avg_coordinates)
decaying_avg_rotations = np.array(decaying_avg_rotations)


# Print or save camera coordinates, rotation angles, running average coordinates, and running average rotations to external documents
output_file_path_coordinates = 'Camera_coordinates.txt'
output_file_path_running_avg = 'running_avg_coordinates.txt' #A RUNNING AVERAGE GIVES SMOOTHER MOTION

np.savetxt(output_file_path_coordinates, camera_coordinates[:, :3], fmt='%.2f', delimiter='\t')
np.savetxt(output_file_path_running_avg, running_avg_coordinates, fmt='%.2f', delimiter='\t')

