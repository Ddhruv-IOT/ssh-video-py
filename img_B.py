import cv2
import time
import sys
import paramiko
import os

def capture_and_transfer_image(ip_address, username, password):
    # Initialize the camera (0 is usually the default camera, change it if needed)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Wait for 3 seconds (you can adjust the delay as needed)
    time.sleep(3)

    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        cap.release()
        return

    # Specify the path and filename to save the captured image
    image_filename = "captured_image.jpg"

    # Save the captured image to the specified filename
    cv2.imwrite(image_filename, frame)

    # Release the camera
    cap.release()

    print(f"Image captured and saved as {image_filename}")

    # Transfer the image to the remote system using SCP
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote system using the provided IP address, username, and password
        ssh_client.connect(ip_address, username=username, password=password)

        # Specify the path where you want to store the image on the remote system
        remote_image_path = "img/captured_image.jpg"

        # Transfer the image using SCP
        with open(image_filename, "rb") as local_image:
            ssh_client.open_sftp().putfo(local_image, remote_image_path)

        print(f"Image transferred to {ip_address}:{remote_image_path}")

        # Close the SSH connection
        ssh_client.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python capture_and_transfer.py <IP_ADDRESS> <USERNAME> <PASSWORD>")
        sys.exit(1)

    ip_address = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    # Call the capture_and_transfer_image function with the provided IP address, username, and password
    capture_and_transfer_image(ip_address, username, password)

