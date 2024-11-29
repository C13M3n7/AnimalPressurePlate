import time
import os
import subprocess
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageDraw, ImageFont
import adafruit_dht
from detectHUMAN import detect_single_image
from google_upload import upload_image, share_file_with_user
import board

# Setup
GPIO.setmode(GPIO.BCM)
button_pin = 5
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Paths
model_path = 'efficientdet_lite0.tflite'  # Path to your TFLite model
detected_folder = 'detected_images'
non_detected_folder = 'non_detected_images'
num_threads = 4
enable_edgetpu = False

# Email settings
sender_email = "clementchangcheng@gmail.com"
receiver_email = "clementchangcheng@gmail.com"
email_password = "hyziewdloefmazjx"

# Google Drive sharing settings
drive_share_email = "paingchan211@gmail.com"  # Replace with the email to share the file with

# DHT sensor setup
DHT_SENSOR_PIN = board.D4  # Use the correct GPIO pin
dht_sensor = adafruit_dht.DHT11(DHT_SENSOR_PIN)

# Create folders if they don't exist
if not os.path.exists(detected_folder):
    os.makedirs(detected_folder)
if not os.path.exists(non_detected_folder):
    os.makedirs(non_detected_folder)

# Function to read temperature and humidity from the DHT sensor
def read_temperature():
    try:
        # Read temperature and humidity from the sensor
        temperature_c = dht_sensor.temperature
        humidity = dht_sensor.humidity

        if temperature_c is not None and humidity is not None:
            return temperature_c
        else:
            print("Failed to read data from sensor.")
            return None
    except RuntimeError as error:
        # Handle intermittent sensor read errors
        print(f"RuntimeError: {error.args[0]}")
        return None


# Function to add date, time, and temperature to the image
def add_text_to_image(image_path, temperature_c, humidity):
    # Open the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Define the font and text properties
    font = ImageFont.load_default()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    temp_text = f"Temp: {temperature_c}Â°C" if temperature_c is not None else "Temp: N/A"
    humidity_text = f"Humidity: {humidity}%" if humidity is not None else "Humidity: N/A"

    # Define text position and color
    text_position = (10, 10)
    temp_position = (10, 30)
    humidity_position = (10, 50)
    text_color = (255, 255, 255)  # White text

    # Add text to image
    draw.text(text_position, f"Date & Time: {timestamp}", fill=text_color, font=font)
    draw.text(temp_position, temp_text, fill=text_color, font=font)
    draw.text(humidity_position, humidity_text, fill=text_color, font=font)

    # Save the modified image
    img.save(image_path)


# Function to send email with the captured image
def send_email(attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Human detected"
    body = "A human has been detected in one of the captured images."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the detected image
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully with attachment.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to capture images and process them
def capture_images():
    for i in range(10):
        # Capture the image
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f'image_capture_{timestamp}_{i+1}.jpg'
        ffmpeg_command = ['ffmpeg', '-f', 'v4l2', '-i', '/dev/video0', '-frames:v', '1', output_file]
        subprocess.run(ffmpeg_command)
        
        # Read the temperature
        temperature_c = read_temperature()
        humidity = dht_sensor.humidity  # Add this to read humidity

        # Add text (timestamp, temperature, humidity) to the image
        add_text_to_image(output_file, temperature_c, humidity)

        # Run detection on the captured image
        detection_output_file = os.path.join(detected_folder, output_file)
        detect_single_image(model_path, output_file, detection_output_file, num_threads, enable_edgetpu)

        # Only keep the file if it contains a human
        if os.path.exists(detection_output_file):
            print(f"Human detected. Image saved to {detection_output_file}")
            send_email(detection_output_file)  # Send email notification with attachment
        else:
            # Move non-detected image to separate folder
            non_detected_path = os.path.join(non_detected_folder, output_file)
            os.rename(output_file, non_detected_path)
            print(f"No human detected. Image saved to {non_detected_path}")
            upload_image(non_detected_path)
            
            # Upload non-detected image to Google Drive
            file_id = upload_image(non_detected_path)
            if file_id:
                share_file_with_user(file_id, drive_share_email)  # Share the file with the specified email address
        
        time.sleep(1)  # Delay between captures

try:
    print("Press the button to capture 10 images...")
    while True:
        # Wait for the button to be pressed
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:  # Button pressed
            print("Button pressed! Capturing images...")
            capture_images()
            print("Images captured. Waiting for the next button press...")
            time.sleep(1)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()

