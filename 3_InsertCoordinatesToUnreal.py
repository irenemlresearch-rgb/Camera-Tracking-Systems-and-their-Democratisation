# output_file_path_coordinates = 'camera_coordinates.txt'
# output_file_path_running_avg = 'running_avg_coordinates.txt'

# Specify the path to the .txt file containing 3D vectors
location_txt_file_path = "" #HERE YOUR PATH TO SAVE THE FILE
sequence_asset_path = "" #HERE THE NAME OF YOUR UNREAL SEQUENCE (Same as defined in UnrealSequenceAndCamara.py)

import unreal

def add_keyframes_from_txt(camera_actor):

    # add an infinite transform track
    track = camera_actor.add_track(unreal.MovieScene3DTransformTrack)    
    section = track.add_section()
    section.set_start_frame_bounded(0)
    section.set_end_frame_bounded(0)

    # Read 3D vectors from the .txt file
    with open(location_txt_file_path, 'r') as file:
        lines = file.readlines()

    # Assuming each line contains a 3D vector in the format "x\ty\tz"
    frame = 0
    for line in lines:
        frame = frame + 1
        components = line.strip().split('\t')
        if len(components) == 3:
            x, y, z = float(components[0]), float(components[1]), float(components[2])

            section.get_all_channels()[0].add_key(time=unreal.FrameNumber(frame), new_value=5310.3+(x*37))
            section.get_all_channels()[1].add_key(time=unreal.FrameNumber(frame), new_value=5590.6+(y*37))
            section.get_all_channels()[2].add_key(time=unreal.FrameNumber(frame), new_value=50+(-z*37))

def main():
	sequence_asset = unreal.LevelSequence.cast(unreal.EditorAssetLibrary.load_asset(sequence_asset_path))
	
	# Create a spawnable from an actor class
	spawnable_camera_binding = sequence_asset.add_spawnable_from_class(unreal.CineCameraActor)

    # Add keyframes to the camera actor from the .txt file
	add_keyframes_from_txt(spawnable_camera_binding)

if __name__ == "__main__":
    main()

