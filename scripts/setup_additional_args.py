"""
This script provides an extended set of arguments that can be passed from the command line to setup additional settings
that are otherwise not possible to modify from the command line.

Python can read all arguments passed to blender via sys.argv. By default blender ignores all arguments after the `--`
argument. We can use this information to extend blender's command line interface to allow us to set additional render
settings at runtime.
"""

import sys
import argparse
import bpy, _cycles


SCRIPT_DESCRIPTION = "Used to set the value of a number of Blender settings that can not be set through the command " \
                     "line."

BLENDER_IGNORE_ARGUMENT = '--'

CYCLES_COMPUTE_DEVICE = 'cycles_compute_device'
CYCLES_INTEGRATOR = 'cycles_integrator'
CYCLES_SAMPLES = 'cycles_samples'
CYCLES_SEED = 'cycles_seed'
CYCLES_SAMPLING_PATTERN = 'cycles_sampling_pattern'
CYCLES_SQUARE_SAMPLES = 'cycles_square_samples'
CYCLES_MIN_LIGHT_BOUNCES = 'cycles_min_light_bounces'
CYCLES_MIN_TRANSPARENT_BOUNCES = 'cycles_min_transparent_bounces'
CYCLES_LIGHT_SAMPLING_THRESHOLD = 'cycles_light_sampling_threshold'
CYCLES_MAX_BOUNCES = 'cycles_max_bounces'
CYCLES_DIFFUSE_BOUNCES = 'cycles_diffuse_bounces'
CYCLES_GLOSSY_BOUNCES = 'cycles_glossy_bounces'
CYCLES_TRANSPARENT_MAX_BOUNCES = 'cycles_transparent_max_bounces'
CYCLES_VOLUME_BOUNCES = 'cycles_volume_bounces'
CYCLES_SAMPLE_CLAMP_DIRECT = 'cycles_sample_clamp_direct'
CYCLES_SAMPLE_CLAMP_INDIRECT = 'cycles_sample_clamp_indirect'
CYCLES_BLUR_GLOSSY = 'cycles_blur_glossy'
CYCLES_CAUSTICS_REFLECTIVE = 'cycles_caustics_reflective'
CYCLES_CAUSTICS_REFRACTIVE = 'cycles_caustics_refractive'
CYCLES_VOLUME_STEP_SIZE = 'cycles_volume_step_size'
CYCLES_VOLUME_MAX_STEPS = 'cycles_volume_max_steps'
CYCLES_USE_MOTION_BLUR = 'cycles_use_motion_blur'
CYCLES_MOTION_BLUR_POSITION = 'cycles_motion_blur_position'
CYCLES_MOTION_BLUR_SHUTTER = 'cycles_motion_blur_shutter'
CYCLES_ROLLING_SHUTTER_TYPE = 'cycles_rolling_shutter_type'
CYCLES_ROLLING_SHUTTER_DURATION = 'cycles_rolling_shutter_duration'
CYCLES_FILM_EXPOSURE = 'cycles_film_exposure'
CYCLES_PICEL_FILTER_TYPE = 'cycles_pixel_filter_type'
CYCLES_PIXEL_FILTER_WIDTH = 'cycles_pixel_filter_width'
CYCLES_FILM_TRANSPARENT = 'cycles_film_transparent'
CYCLES_FILM_TRANSPARENT_GLASS = 'cycles_film_transparent_glass'
CYCLES_FILM_TRANSPARENT_ROUGHNESS = 'cycles_film_transparent_roughness'
OUTPUT_RESOLUTION_X = 'output_resolution_x'
OUTPUT_RESOLUTION_Y = 'output_resolution_y'
OUTPUT_RESOLUTION_PERCENTAGE = 'output_resolution_percentage'
OUTPUT_PIXEL_ASPECT_X = 'output_pixel_aspect_x'
OUTPUT_PIXEL_ASPECT_Y = 'output_pixel_aspect_y'


def set_cycles_compute_device(value: str):
    bpy.context.scene.cycles.device = value

    if value == "GPU":
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = "CUDA"
        bpy.context.user_preferences.addons['cycles'].preferences.devices[0].use = True

        # set performance settings for GPU rendering
        bpy.context.scene.render.tile_x = 256
        bpy.context.scene.render.tile_y = 256


def set_cycles_integrator(value: str):
    bpy.context.scene.cycles.progressive = value


def set_cycles_samples(value: int):
    bpy.context.scene.cycles.samples = value


def set_cycles_seed(value: int):
    bpy.context.scene.cycles.seed = value


def set_cycles_sampling_pattern(value: str):
    bpy.context.scene.cycles.sampling_pattern = value


def set_cycles_square_samples(value: bool):
    bpy.context.scene.cycles.use_square_samples = value


def set_cycles_min_light_bounces(value: int):
    bpy.context.scene.cycles.min_bounces = value


def set_cycles_min_transparent_bounces(value: int):
    bpy.context.scene.cycles.transparent_min_bounces = value


def set_cycles_light_sampling_threshold(value: float):
    bpy.context.scene.cycles.light_sampling_threshold = value


def set_cycles_max_bounces(value: int):
    bpy.context.scene.cycles.max_bounces = value


def set_cycles_diffuse_bounces(value: int):
    bpy.context.scene.cycles.diffuse_bounces = value


def set_cycles_glossy_bounces(value: int):
    bpy.context.scene.cycles.glossy_bounces = value


def set_cycles_transparent_max_bounces(value: int):
    bpy.context.scene.cycles.transmission_bounces = value


def set_cycles_volume_bounces(value: int):
    bpy.context.scene.cycles.volume_bounces = value


def set_cycles_sample_clamp_direct(value: float):
    bpy.context.scene.cycles.sample_clamp_direct = value


def set_cycles_sample_clamp_indirect(value: float):
    bpy.context.scene.cycles.sample_clamp_indirect = value


def set_cycles_blur_glossy(value: float):
    bpy.context.scene.cycles.blur_glossy = value


def set_cycles_caustics_reflective(value: bool):
    bpy.context.scene.cycles.caustics_reflective = value


def set_cycles_caustics_refractive(value: bool):
    bpy.context.scene.cycles.caustics_refractive = value


def set_cycles_volume_step_size(value: float):
    bpy.context.scene.cycles.volume_step_size = value


def set_cycles_volume_max_steps(value: int):
    bpy.context.scene.cycles.volume_max_steps = value


def set_cycles_use_motion_blur(value: bool):
    bpy.context.scene.render.use_motion_blur = value


def set_cycles_motion_blur_position(value: str):
    bpy.context.scene.cycles.motion_blur_position = value


def set_cycles_motion_blur_shutter(value: float):
    bpy.context.scene.render.motion_blur_shutter = value


def set_cycles_rolling_shutter_type(value: str):
    bpy.context.scene.cycles.rolling_shutter_type = value


def set_cycles_rolling_shutter_duration(value: float):
    bpy.context.scene.cycles.rolling_shutter_duration = value


def set_cycles_film_exposure(value: float):
    bpy.context.scene.cycles.film_exposure = value


def set_cycles_pixel_filter_type(value: str):
    bpy.context.scene.cycles.pixel_filter_type = value


def set_cycles_pixel_filter_width(value: int):
    bpy.context.scene.cycles.filter_width = value


def set_cycles_film_transparent(value: bool):
    bpy.context.scene.cycles.film_transparent = value


def set_cycles_film_transparent_glass(value: bool):
    # added in 2.80
    pass


def set_cycles_film_transparent_roughness(value: float):
    # added in 2.80
    pass


def set_output_resolution_x(value: int):
    bpy.context.scene.render.resolution_x = value


def set_output_resolution_y(value: int):
    bpy.context.scene.render.resolution_y = value


def set_output_resolution_percentage(value: int):
    bpy.context.scene.render.resolution_percentage = value


def set_output_pixel_aspect_x(value: float):
    bpy.context.scene.render.pixel_aspect_x = value


def set_output_pixel_aspect_y(value: float):
    bpy.context.scene.render.pixel_aspect_y = value



# create the argument parser
parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
argument_map = list()


def add_argument_to_parser(name: str, method, help: str = None, type: type = None, choices=None, required: bool = False,
                           default=None):
    """ Helper method for adding arguments to the parser """

    parser.add_argument('--%s' % name,
                           dest=name,
                           help=help,
                           type=type,
                           choices=choices,
                           required=required,
                           default=default)

    argument_map.append([name, method])


add_argument_to_parser(CYCLES_COMPUTE_DEVICE,
                       set_cycles_compute_device,
                       help='Sets the compute device to use for rendering',
                       type=str,
                       choices=['CPU', 'GPU'],
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_INTEGRATOR,
                       set_cycles_integrator,
                       help='Sets the path tracing integrator',
                       type=str,
                       choices=['BRANCHED_PATH', 'PATH'],
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_SAMPLES,
                       set_cycles_samples,
                       help='Sets the number of samples to use for each pixel',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_SEED,
                       set_cycles_seed,
                       help='Sets the seed value for the integrator. Used to get different noise patterns',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_SAMPLING_PATTERN,
                       set_cycles_sampling_pattern,
                       help='Sets the random sampling pattern used by the integrator',
                       type=str,
                       required=False,
                       choices=['SOBOL', 'CORRELATED_MUTI_JITTER'],
                       default=None)

add_argument_to_parser(CYCLES_SQUARE_SAMPLES,
                       set_cycles_square_samples,
                       help='Sets the square samples flag. This flag squares(^2) the number of samples',
                       type=bool,
                       required=False,
                       choices=['True', 'False'],
                       default=None)

add_argument_to_parser(CYCLES_MIN_LIGHT_BOUNCES,
                       set_cycles_min_light_bounces,
                       help='Set the minimum number of light bounces. Setting this higher can reduce the noise in the '
                            'first bounces, but can also be less efficient for more complex geometry like hair and volumes',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_MIN_TRANSPARENT_BOUNCES,
                       set_cycles_min_transparent_bounces,
                       help='Set the minimum number of transparent bounces. Setting this higher can reduce the noise in '
                            'the first bounces, but can also be less efficient for more complex geometry like hair and '
                            'volumes',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_LIGHT_SAMPLING_THRESHOLD,
                       set_cycles_light_sampling_threshold,
                       help='Set the light threshold which probabilistically terminates light samples when the light '
                            'contribution is below this threshold (More noise but faster rendering). Zero disables the '
                            'test and never ignores lights',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_MAX_BOUNCES,
                       set_cycles_max_bounces,
                       help='Set the maximum number of bounces',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_DIFFUSE_BOUNCES,
                       set_cycles_diffuse_bounces,
                       help='Set the maximum number of diffuse bounces',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_GLOSSY_BOUNCES,
                       set_cycles_glossy_bounces,
                       help='Set the maximum number of glossy bounces',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_TRANSPARENT_MAX_BOUNCES,
                       set_cycles_transparent_max_bounces,
                       help='Set the maximum number of transparent bounces',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_VOLUME_BOUNCES,
                       set_cycles_volume_bounces,
                       help='Set the maximum number of volumetric scattering events',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_SAMPLE_CLAMP_DIRECT,
                       set_cycles_sample_clamp_direct,
                       help='If non zero, the maximum number for a direct sample, higher values will be scaled down to '
                            'avoid too much noise and slow convergence at the cost of accuracy',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_SAMPLE_CLAMP_INDIRECT,
                       set_cycles_sample_clamp_indirect,
                       help='If non zero, the maximum number for a indirect sample, higher values will be scaled down to '
                            'avoid too much noise and slow convergence at the cost of accuracy',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_BLUR_GLOSSY,
                       set_cycles_blur_glossy,
                       help='Adaptively blur glossy shaders after blurry bounces, to reduce noice at the cost of accuracy',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_CAUSTICS_REFLECTIVE,
                       set_cycles_caustics_reflective,
                       help='Use reflective caustics, resulting in a brighter image (more noise but added realism)',
                       type=bool,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_CAUSTICS_REFRACTIVE,
                       set_cycles_caustics_refractive,
                       help='Use refractive caustics, resulting in a brighter image (more noise but added realism)',
                       type=bool,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_VOLUME_STEP_SIZE,
                       set_cycles_volume_step_size,
                       help='Distance between volume shader samples when rendering the volume (lower values give more '
                            'accurate and detailed results, but also increase render time)',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_VOLUME_MAX_STEPS,
                       set_cycles_volume_max_steps,
                       help='Maximum number of steps through the volume before giving up, to avoid extremely long render '
                            'times with big objects or small step sizes',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_USE_MOTION_BLUR,
                       set_cycles_use_motion_blur,
                       help='Use multi-sampled 3D scene Motion blur',
                       type=bool,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_MOTION_BLUR_POSITION,
                       set_cycles_motion_blur_position,
                       help='Offset for the shutters time interval. Allows to change the motion blur trails',
                       type=str,
                       required=False,
                       choices=['START', 'CENTER', 'END'],
                       default=None)

add_argument_to_parser(CYCLES_MOTION_BLUR_SHUTTER,
                       set_cycles_motion_blur_shutter,
                       help='Time taken in frames between shutter open and close',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_ROLLING_SHUTTER_TYPE,
                       set_cycles_rolling_shutter_type,
                       help='Type of rolling shutter effect matching CMOS-based cameras',
                       type=str,
                       required=False,
                       choices=['TOP', 'NONE'],
                       default=None)

add_argument_to_parser(CYCLES_ROLLING_SHUTTER_DURATION,
                       set_cycles_rolling_shutter_duration,
                       help='Scanline "exposure" time for the rolling shutter effect',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_FILM_EXPOSURE,
                       set_cycles_film_exposure,
                       help='Image brightness scale',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_PICEL_FILTER_TYPE,
                       set_cycles_pixel_filter_type,
                       help='Set the pixel filter type',
                       type=str,
                       required=False,
                       choices=['BOX', 'GAUSSIAN', 'BLACKMAN_HARRIS'],
                       default=None)

add_argument_to_parser(CYCLES_PIXEL_FILTER_WIDTH,
                       set_cycles_pixel_filter_width,
                       help='Set the pixel filter width',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_FILM_TRANSPARENT,
                       set_cycles_film_transparent,
                       help='Sets the world background to transparent, for composting the world background over another',
                       type=bool,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_FILM_TRANSPARENT_GLASS,
                       set_cycles_film_transparent_glass,
                       help='Render transmissive surfaces as transparent, for compositing glass over another background',
                       type=bool,
                       required=False,
                       default=None)

add_argument_to_parser(CYCLES_FILM_TRANSPARENT_ROUGHNESS,
                       set_cycles_film_transparent_roughness,
                       help='For transparent transmission, keep surfaces with roughness above the threshold opaque',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(OUTPUT_RESOLUTION_X,
                       set_output_resolution_x,
                       help='Number of horizontal pixels in the image',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(OUTPUT_RESOLUTION_Y,
                       set_output_resolution_y,
                       help='Number of vertical pixels in the image',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(OUTPUT_RESOLUTION_PERCENTAGE,
                       set_output_resolution_percentage,
                       help='Percentage scale for render resolution',
                       type=int,
                       required=False,
                       default=None)

add_argument_to_parser(OUTPUT_PIXEL_ASPECT_X,
                       set_output_pixel_aspect_x,
                       help='Horizontal aspect ratio - for anamorphic or non-squared pixel output',
                       type=float,
                       required=False,
                       default=None)

add_argument_to_parser(OUTPUT_PIXEL_ASPECT_Y,
                       set_output_pixel_aspect_y,
                       help='Vertical aspect ratio - for anamorphic or non-squared pixel output',
                       type=float,
                       required=False,
                       default=None)

# Check that the `--` argument is passed
if BLENDER_IGNORE_ARGUMENT not in sys.argv:
    raise ValueError(BLENDER_IGNORE_ARGUMENT + " not provided as command line argument")

# Get the arguments after the BLENDER_IGNORE_ARGUMENT
argv = sys.argv[sys.argv.index(BLENDER_IGNORE_ARGUMENT) + 1:]
args = parser.parse_known_args(argv)[0]

for argument_mapping in argument_map:
    if getattr(args, argument_mapping[0]) is not None:
        argument_mapping[1](getattr(args, argument_mapping[0]))
