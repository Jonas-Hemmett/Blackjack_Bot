from picamera2 import Picamera2
import time

# Create a camera object
cam = Picamera2()

# Configure the camera for a simple preview
cam.configure(cam.create_preview_configuration())

# Start the camera
cam.start()

# Give it some time to warm up
time.sleep(2)

# Capture an image and save it
cam.capture_file("test_image.jpg")

print("Image captured and saved as test_image.jpg")

# Stop the camera
cam.stop()