# Animal Pressure Plate Detection System

## Hardware & software Requirements
- Raspberry Pi 4 model B
- Camera module
- Temperature/humidity sensor (DHT11/DHT22)
- Pressure sensor or GPIO button
- Internet connectivity
- Python 3.7+
- Virtual environment

### Initial setup
```bash
#free up space
cat /etc/os-release

# get updates and upgrade
sudo apt update
sudo apt upgrade

# Create and navigate to project folder
mkdir animal-detection-project
cd animal-detection-project

# Create virtual environment
virtualenv env

# Activate virtual environment
source /path/to/your/env/bin/activate

# Upgrade pip
pip install --upgrade pip

#System packages
sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev

#If you're using a PiCamera run:
pip install "picamera[array]"

#Users of PiCamera may also have to enable Camera Support:
sudo raspi-config
Inferface Options
Legacy Camera Support -- Enable
```

### Python downgrade
```bash
restart terminal

# downgrade python
sudo apt get install curl
curl https://pyenv.run | bash
sudo nano ~/.bashrc

# Add the following three lines to the botton of the .bashrc file:
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

# Restart the terminal
exec $SHELL

# Install system packages
sudo apt-get install --yes libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev lzma lzma-dev tcl-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev wget make openssl

# Update pyenv
pyenv update

# Install python versions
pyenv install --list
pyenv install 3.7.12

# got into your project folder and activate the downgraded python
cd animal-detection-project
pyenv local 3.7.12
```

### Install Dependencies
```bash
# Install required libraries
pip install RPi.GPIO
pip install pillow
pip install adafruit_dht
pip install tflite-support
pip install numpy
pip install opencv-python
pip install secure-smtplib
pip install email
sudo apt install python3-googleapi
sudo apt install python3-oauth2client
sudo apt install python3-google-auth-oauthlib
```

## Email and Database connection Setup
Set up Google Drive API credentials by running:
```bash
# generate token
python google_upload.py
```
Adjust email settings by setting up Google cloud:
- open google cloud console
- create a new project
- enable google drive API
- find the search bar type credentials
- make OAUTH 2.0 Client ID
- download the credentials and then save as credentials.json
- put the code in google_upload.py at:
```bash
if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Name of generated .json file', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)
```
- place the credentials.json in the same directory as your code
- run the code you it will bring u to a google login page in raspberry pi
- login with the gmail you used in google cloud console
- after login, it will ask to grant permissions, grant it
- after u run it the first time you should see a file called token.pickle created in the same directory as your code and the crendentials.json
- you can now logout of your google account in raspberry pi as the token.pickle saves your credentials for future use

Set up app passwords to establish connection
```bash
https://myaccount.google.com/apppasswords
```

App passwords would be placed in cambutton.py at
```bash
# Email settings
sender_email = "youremail.com"
receiver_email = "youremail.com"
email_password = "your app password for youremail.com"
```

## Development Tips
- Always activate venv before working
- Install new packages within venv

## Troubleshooting
- Ensure correct Python version
- Check venv activation
- Verify library compatibility
- Rerun the google_uploads.py as the token might have expired

## System Overview
Automated wildlife monitoring system using Raspberry Pi for detection, imaging, and data logging.


## Main Usage
```bash
# Run main detection script in virtual environment
python3 cambutton.py

# place this code into rc.local directory to run the code on startup
sudo nano /etc/rc.local

# Add the following line before the exit 0 line
source /path/to/your/env/bin/activate
/path/to/cambutton.sh &
```

## Security Considerations
- Protect sensitive credentials
- Use environment variables
- Implement secure file permissions
