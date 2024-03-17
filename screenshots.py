import os
import time
import threading
import pyautogui
import keyboard

# Function to take screenshots
def take_screenshot(interval, stop_event):
    # Create a directory for screenshots if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    while not stop_event.is_set():
        # Take screenshot
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshots/screenshot_{timestamp}.png")

        # Wait for the specified interval
        stop_event.wait(interval)

# Main function
def main():
    # Ask for the interval between screenshots
    interval = int(input("Enter the interval between screenshots (in seconds): "))
    
    # Create a stop event for the screenshot thread
    stop_event = threading.Event()
    
    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, args=(interval, stop_event))
    screenshot_thread.start()

    print("Screenshot program started. Press 'q' to quit.")

    # Listen for keyboard input to quit the program
    keyboard.wait("q")

    # Set the stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
