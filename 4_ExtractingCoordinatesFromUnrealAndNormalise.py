# Specify the path to the .txt file containing 3D vectors
location_txt_file_path = "/Users/iml3/Desktop/Desktop - Irene’s MacBook Pro/TechProject/1_PythonTracker/PYTHON_Straight_SMPTE_coordinates.txt"
rotation_txt_file_path = "/Users/iml3/Desktop/Desktop - Irene’s MacBook Pro/TechProject/1_PythonTracker/PYTHON_Straight_SMPTE_rotation.txt"
sequence_asset_path = "/Game/Sequences/Straight_1_SMPTE"

import unreal

def main():
    sequence_asset = unreal.LevelSequence.cast(unreal.EditorAssetLibrary.load_asset(sequence_asset_path))

    if sequence_asset:

        bindings = sequence_asset.get_bindings()
        
        # Get the master tracks
        master_tracks = sequence_asset.get_master_tracks()
        
        # Iterate through each track in the sequence
        for spawnable in sequence_asset.get_spawnables():
            print("spawnable name:", spawnable.get_display_name())
            
            if isinstance(spawnable, unreal.MovieSceneBindingProxy):

                tracks = spawnable.get_tracks()
                for track in tracks:
                    print(track.get_display_name())
                    if isinstance(track, unreal.MovieScene3DTransformTrack):
                        print("track found")
                        for section in track.get_sections():
                            location_x =section.get_all_channels()[0].get_keys()
                            location_y =section.get_all_channels()[1].get_keys()
                            location_z =section.get_all_channels()[2].get_keys()         
                            # Write coordinates to a text file
                            with open(location_txt_file_path, "w") as file:
                                for frame in range(0,len(location_x)):
                                    file.write(f"{location_x[frame].get_value()-location_x[0].get_value()}\t{location_y[frame].get_value()-location_y[0].get_value()}\t{location_z[frame].get_value()-location_z[0].get_value()}\n")
                            
                            rotation_x =section.get_all_channels()[3].get_keys()
                            rotation_y =section.get_all_channels()[4].get_keys()
                            rotation_z =section.get_all_channels()[5].get_keys() 
                            
                            with open(rotation_txt_file_path, "w") as file:
                                for frame in range(0,len(location_x)):
                                    file.write(f"{rotation_x[frame].get_value()-rotation_x[0].get_value()}\t{rotation_y[frame].get_value()-rotation_y[0].get_value()}\t{rotation_z[frame].get_value()-rotation_z[0].get_value()}\n")


            else:
                print("not found", spawnable.get_virtual_path())
            



if __name__ == "__main__":
    main()



# import unreal

# def get_txt_from_keyframes(camera_actor):

#     # add an infinite transform track
#     track = camera_actor.add_track(unreal.MovieScene3DTransformTrack)    
#     section = track.add_section()
#     section.set_start_frame_bounded(0)
#     section.set_end_frame_bounded(0)

#     # Read 3D vectors from the .txt file
#     with open(location_txt_file_path, 'r') as file:
#         lines = file.readlines()

#     # Assuming each line contains a 3D vector in the format "x\ty\tz"
#     frame = 0
#     for line in lines:
#         frame = frame + 1
#         components = line.strip().split('\t')
#         if len(components) == 3:
#             x, y, z = float(components[0]), float(components[1]), float(components[2])

#             section.get_all_channels()[0].add_key(time=unreal.FrameNumber(frame), new_value=5310.3+(-z*37))
#             section.get_all_channels()[1].add_key(time=unreal.FrameNumber(frame), new_value=5590.6+(x*37))
#             section.get_all_channels()[2].add_key(time=unreal.FrameNumber(frame), new_value=50+(y*37))

#     # Read 3D vectors from the .txt file
#     with open(rotation_txt_file_path, 'r') as file:
#         lines = file.readlines()

#     # Assuming each line contains a 3D vector in the format "x\ty\tz"
#     frame = 0
#     for line in lines:
#         frame = frame + 1
#         components = line.strip().split('\t')
#         if len(components) == 3:
#             x, y, z = float(components[0]), float(components[1]), float(components[2])

#             section.get_all_channels()[3].add_key(time=unreal.FrameNumber(frame), new_value=(-z))
#             section.get_all_channels()[4].add_key(time=unreal.FrameNumber(frame), new_value=x)
#             section.get_all_channels()[5].add_key(time=unreal.FrameNumber(frame), new_value=y)


# def main():
# 	sequence_asset = unreal.LevelSequence.cast(unreal.EditorAssetLibrary.load_asset(sequence_asset_path))
	
# 	# Create a spawnable from an actor class
# 	spawnable_camera_binding = sequence_asset.add_spawnable_from_class(unreal.CineCameraActor)

#     # Add keyframes to the camera actor from the .txt file
# 	add_keyframes_from_txt(spawnable_camera_binding)

# if __name__ == "__main__":
#     main()

# import unreal

# # Assuming the frame rate of your video is 50fps
# video_frame_rate = 50.0

# def add_keyframes_from_txt(camera_actor, video_frame_rate):

#     # add an infinite transform track
#     track = camera_actor.add_track(unreal.MovieScene3DTransformTrack)    
#     section = track.add_section()
#     section.set_start_frame_bounded(0)
#     section.set_end_frame_bounded(0)
       
#     # Read 3D vectors from the .txt file
#     with open(location_txt_file_path, 'r') as file:
#         lines = file.readlines()

#     # Assuming each line contains a 3D vector in the format "x\ty\tz"
#     frame = 0
#     for line in lines:
#         frame += 1
#         components = line.strip().split('\t')
#         if len(components) == 3:
#             x, y, z = float(components[0]), float(components[1]), float(components[2])

#             # Adjust the frame calculation based on the video frame rate
#             section.get_all_channels()[0].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=x)
#             section.get_all_channels()[1].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=y)
#             section.get_all_channels()[2].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=z)

#     # Read 3D vectors from the .txt file
#     with open(rotation_txt_file_path, 'r') as file:
#         lines = file.readlines()

#     # Assuming each line contains a 3D vector in the format "x\ty\tz"
#     frame = 0
#     for line in lines:
#         frame += 1
#         components = line.strip().split('\t')
#         if len(components) == 3:
#             x, y, z = float(components[0]), float(components[1]), float(components[2])

#             # Adjust the frame calculation based on the video frame rate
#             section.get_all_channels()[3].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=x)
#             section.get_all_channels()[4].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=y)
#             section.get_all_channels()[5].add_key(time=unreal.FrameNumber(int(frame * video_frame_rate)), new_value=z)


# def main():
#     sequence_asset = unreal.LevelSequence.cast(unreal.EditorAssetLibrary.load_asset(sequence_asset_path))
    
#     # Create a spawnable from an actor class
#     spawnable_camera_binding = sequence_asset.add_spawnable_from_class(unreal.CineCameraActor)

#     # Add keyframes to the camera actor from the .txt file
#     add_keyframes_from_txt(spawnable_camera_binding, video_frame_rate)

# if __name__ == "__main__":
#     main()


