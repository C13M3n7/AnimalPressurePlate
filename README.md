# Animal Pressure Plate Detection System

## Project Setup

### Create Project Directory and Virtual Environment
```bash
# Create and navigate to project folder
mkdir animal-detection-project
cd animal-detection-project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Install Dependencies
```bash
# Install required libraries
pip install \
    RPi.GPIO pillow adafruit_dht \
    tflite-support opencv-python-headless \
    google-api-python-client google-auth-httplib2 numpy
```
#### Hardware Interaction
- `RPi.GPIO`: GPIO pin control
- `board`: Board pin mapping
- `adafruit_dht`: Temperature/humidity sensor

#### Image Processing
- `Pillow (PIL)`: Image manipulation
- `cv2 (OpenCV)`: Computer vision
- `numpy`: Numerical computing

#### Machine Learning
- `tflite_support`: TensorFlow Lite object detection

#### System Utilities
- `smtplib`: Email sending
- `email`: MIME email composition
- `os`: File operations
- `subprocess`: System command execution
- `time`: Timestamp generation
- `argparse`: Command-line parsing
- `pickle`: Object serialization

### Deactivate Virtual Environment
```bash
# When finished working
deactivate
```
## Hardware & software Requirements
- Raspberry Pi
- Camera module
- Temperature/humidity sensor (DHT11/DHT22)
- Pressure sensor or GPIO button
- Internet connectivity
- Python 3.7+
- Virtual environment support

## Workflow
1. Create project directory
2. Create virtual environment
3. Activate environment
4. Install dependencies
5. Configure GPIO pins
6. Set up Google Drive API credentials by running:
```bash
# generate token
python google_upload.py
8. Adjust email settings by setting up 
9. Calibrate detection sensitivity
10. Run scripts
11. Deactivate when done

## Development Tips
- Always activate venv before working
- Install new packages within venv

## Troubleshooting
- Ensure correct Python version
- Check venv activation
- Verify library compatibility

## System Overview
Automated wildlife monitoring system using Raspberry Pi for detection, imaging, and data logging.

## Configuration Steps
1. Install dependencies
2. Configure GPIO pins
3. Set up Google Drive API credentials
4. Adjust email settings
5. Calibrate detection sensitivity

## Key Features
- Automated wildlife detection
- Image capture
- Environmental logging
- Cloud storage integration
- Email notifications

## Usage
```bash
# Run main detection script
python3 cambutton.py
```

## Security Considerations
- Protect sensitive credentials
- Use environment variables
- Implement secure file permissions

## Troubleshooting
- Verify sensor connections
- Check camera access
- Validate API permissions

## Potential Improvements
- Add machine learning model retraining
- Implement more robust error handling
- Create configuration file
- Add logging mechanisms
