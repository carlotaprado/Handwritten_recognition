import numpy as np
import cv2
import os
import random
import time

# Step 1: Load Dataset
def load_images_from_folder(folder):
    images = {}
    for label in os.listdir(folder):
        path = os.path.join(folder, label)
        if not os.path.isdir(path):
            continue
        images[label] = []  # Use digit keys for consistency
        for file in os.listdir(path):
            img_path = os.path.join(path, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Read in grayscale
            if img is not None:
                # Resize to 28x28 as preprocessing
                img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
                images[label].append(img)
    return images

# Step 2: Read input from the text file
def read_user_input(file_path):
    previous_last_digit = None  # To track the last displayed digit
    while True:
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()  # Read the entire file content
                digits = [ch for ch in content if ch.isdigit()]  # Extract digits

                if digits:  # Ensure there are digits
                    last_digit = digits[-1]  # Get the most recent digit

                    # Only return if it's a new digit
                    if last_digit != previous_last_digit:
                        previous_last_digit = last_digit
                        return last_digit  # Return the last digit to display

        except Exception as e:
            print(f"Error reading input file: {e}")
        time.sleep(1)  # Check for changes every second

# Step 3: Display Handwritten Digit Dynamically
def on_mouse(event, x, y, flags, param):
    # Check if mouse is inside the OpenCV window
    window_name = "Handwritten Sample"
    window_rect = cv2.getWindowImageRect(window_name)
    if not (window_rect[0] <= x <= window_rect[0] + window_rect[2] and window_rect[1] <= y <= window_rect[1] + window_rect[3]):
        # Mouse click is outside the window
        return  # Ignore the click

def display_handwritten(images, input_file):
    print("Type a digit in the text file to see its handwritten version.")
    print("Press Ctrl+C in the terminal to quit.")

    # Create a blank placeholder image
    blank_image = np.ones((100, 100), dtype=np.uint8) * 255
    cv2.imshow("Handwritten Sample", blank_image)
    cv2.setWindowProperty("Handwritten Sample", cv2.WND_PROP_TOPMOST, 1)
    last_displayed_digit = None

    # Set the mouse callback to handle clicks outside the window
    cv2.setMouseCallback("Handwritten Sample", on_mouse)

    while True:
        # Read user input from the text file
        user_input = read_user_input(input_file)

        # Skip if the input is unchanged, invalid, or None
        if user_input == last_displayed_digit or user_input is None or not user_input.isdigit():
            continue

        # Update the last displayed digit
        last_displayed_digit = user_input

        # Check if the digit exists in the dataset
        if user_input not in images or len(images[user_input]) == 0:
            print(f"No handwritten samples found for the digit '{user_input}'.")
            cv2.imshow("Handwritten Sample", blank_image)
            continue

        # Randomly select an image for the typed digit
        handwritten_image = random.choice(images[user_input])

        # Resize with high-quality interpolation for better resolution
        handwritten_image_resized = cv2.resize(handwritten_image, (100, 100), interpolation=cv2.INTER_CUBIC)

        # Invert the colors: white background becomes black, and digit becomes white
        handwritten_image_inverted = cv2.bitwise_not(handwritten_image_resized)

        # Display the inverted image
        cv2.imshow("Handwritten Sample", handwritten_image_inverted)
        print(f"Displaying handwritten sample for digit '{user_input}'.")

        # Check if the mouse is inside the OpenCV window before accepting key press
        if cv2.waitKey(500) == 27:  # Press 'ESC' to exit
            break

# Main Function
if __name__ == "__main__":
    # Specify the dataset folder
    folder = r"C:\Users\Acer\Desktop\Handwritten_recognition\dataset"  # Replace with your actual dataset path
    input_file = r"C:\Users\Acer\Desktop\Handwritten_recognition\input.txt"  # Replace with your text file path

    # Check if the folder exists
    if not os.path.exists(folder):
        print("Error: Dataset path does not exist!")
        exit()

    # Check if the input file exists
    if not os.path.exists(input_file):
        print("Error: Input file does not exist! Please create the file first.")
        exit()

    # Load dataset
    images = load_images_from_folder(folder)
    if not images:
        print("Error: No images found in the dataset.")
        exit()

    # Display handwritten images dynamically
    try:
        display_handwritten(images, input_file)
    except KeyboardInterrupt:
        print("Exiting program.")
        cv2.destroyAllWindows()
