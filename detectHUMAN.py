import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils


def detect_single_image(model: str, image_path: str, output_path: str, num_threads: int, enable_edgetpu: bool) -> None:
    """Run inference on a single image and save the output with detections only if a person is detected.

    Args:
        model: Path to the TFLite object detection model.
        image_path: Path to the input image file.
        output_path: Path to save the output image with detections.
        num_threads: The number of CPU threads to run the model.
        enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """
    # Load and prepare the image
    image = cv2.imread(image_path)
    if image is None:
        sys.exit(f'ERROR: Unable to read image from {image_path}. Check the file path.')

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    # Check if a person is detected
    person_detected = False
    for detection in detection_result.detections:
        # Check if any of the detected categories is labeled as "person"
        if "person" in [category.category_name for category in detection.categories]:
            person_detected = True
            break

    # Save the output image only if a person is detected
    if person_detected:
        image_with_detections = utils.visualize(image, detection_result)
        cv2.imwrite(output_path, image_with_detections)
        print(f'Person detected. Output image saved to {output_path}')
    else:
        print('No person detected. Output image was not saved.')



def run(model: str, camera_id: int, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    """Continuously run inference on images acquired from the camera."""
    # Existing camera-based detection code here...


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '--imagePath',
        help='Path to the input image file.',
        required=False)
    parser.add_argument(
        '--outputPath',
        help='Path to save the output image with detections.',
        required=False)

    args = parser.parse_args()

    # Check if image-based detection should be run
    if args.imagePath and args.outputPath:
        detect_single_image(args.model, args.imagePath, args.outputPath, int(args.numThreads), bool(args.enableEdgeTPU))
    else:
        # Fall back to running the camera detection if no image path is provided
        run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight, int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
    main()

