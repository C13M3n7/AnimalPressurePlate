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

### Deactivate Virtual Environment
```bash
# When finished working
deactivate
```

## Workflow
1. Create project directory
2. Create virtual environment
3. Activate environment
4. Install dependencies
5. Run scripts
6. Deactivate when done

## Requirements
- Python 3.7+
- Virtual environment support
- Raspberry Pi hardware

## Development Tips
- Always activate venv before working
- Install new packages within venv
- Use `requirements.txt` for dependency tracking

## Troubleshooting
- Ensure correct Python version
- Check venv activation
- Verify library compatibility
