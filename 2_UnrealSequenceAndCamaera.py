import unreal

def create_sequence(sequence_name, length_seconds=30, fps=30):
    # Create a new LevelSequence
    level_sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(sequence_name, '/Game/Sequences', unreal.LevelSequence, unreal.LevelSequenceFactoryNew())

    # Get the MovieScene from the LevelSequence
    movie_scene = level_sequence.get_movie_scene()

    # Save the sequence
    sequence_path = '/Game/Sequences/{}'.format(sequence_name)

# Example usage
sequence_name = '' #HERE THE NAME OF YOUR SEQUENCE
create_sequence(sequence_name)

def createCamera(location=unreal.Vector(), rotation=unreal.Rotator()):
    # Get the CineCameraActor class
    cine_camera_actor_class = unreal.CineCameraActor.static_class()

    # Place it in the level
    camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cine_camera_actor_class, location, rotation)

    # Create a new CameraComponent
    camera_component = unreal.CineCameraComponent()

    # Attach the CameraComponent to the CineCameraActor
    location_rule = unreal.AttachmentRule.SNAP_TO_TARGET
    rotation_rule = unreal.AttachmentRule.SNAP_TO_TARGET
    scale_rule = unreal.AttachmentRule.SNAP_TO_TARGET

    # Corrected attachment with socket
    socket_name = 'CameraSocket'  # Adjust the socket name as needed
    camera_component.attach_to_component(camera_actor.root_component, socket_name, location_rule, rotation_rule, scale_rule)

    # Save the level after making changes
    unreal.EditorLevelLibrary.save_current_level()

# Example usage
createCamera(location=unreal.Vector(100, 0, 200), rotation=unreal.Rotator(0, 0, 0))



