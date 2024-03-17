import threading
import pyautogui
import keyboard
from PIL import Image
from ultralytics import YOLO
import pydirectinput


def run_bot(decision):
    # Should we use lightning/met?
    distance_target = 1000

    if "buy_location" in decision:
        pyautogui.click(decision["buy_location"])
    elif "play_location" in decision:
        pyautogui.click(decision["play_location"])
        print("Pressing Play")
    elif "no_thanks_location" in decision:
        pyautogui.click(decision["no_thanks_location"])
        print("Pressing No Thanks")
    elif "continue_location" in decision:
        pyautogui.click(decision["continue_location"])
        print("Pressing Continue")
    elif "next_location" in decision:
        pyautogui.click(decision["next_location"])
    elif "fuel_location" in decision and decision["fuel_distance"] < 1000:
        pyautogui.moveTo(decision["fuel_location"])
    else:
        if decision["tree"] and decision["building"]:
            if decision["tree_distance"] + 300 < decision["building_distance"]:
                pyautogui.moveTo(decision["tree_location"])
                distance_target = decision["tree_distance"]
                print("Going to Tree: ", decision["tree_location"])
            else:
                pyautogui.moveTo(decision["building_location"])
                distance_target = decision["building_distance"]
                print("Going to Building: ", decision["building_location"])
        elif decision["tree"]:
            pyautogui.moveTo(decision["tree_location"])
            distance_target = decision["tree_distance"]
            print("Going to Tree: ", decision["tree_location"])
        elif decision["building"]:
            pyautogui.moveTo(decision["building_location"])
            distance_target = decision["building_distance"]
            print("Going to Building: ", decision["building_location"])
    if distance_target < 300:
        pydirectinput.press('1')
        pydirectinput.press('2')

# Function to take screenshots
def take_screenshot(stop_event, model):
    screenx_center = 3840/2
    screeny_center = 2160/2
    pyautogui.FAILSAFE = False

    while not stop_event.is_set():

        decision = {
            "buy": False,
            "play": False,
            "continue": False,
            "next": False,
            "tornado": False,
            "tree": False,
            "fuel": False,
            "building": False,
            "no_thanks": False,
        }

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
        
        results = model([screenshot], conf=.70)  # return a list of Results objects
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        # Process results list
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box
            
            center_x = (x1+x2) / 2
            center_y = (y1+y2) / 2

            name = names[int(cls)]
            
            if name=="buy":
                decision["buy"] = True
                decision["buy_location"] = (center_x, center_y)
            if name == "no_thanks":
                decision["no_thanks"] = True
                decision["no_thanks_location"] = (center_x, center_y)
            elif name == "continue":
                decision["continue"] = True
                decision["continue_location"] = (center_x, center_y)
            elif name == "play":
                decision["play"] = True
                decision["play_location"] = (center_x, center_y)
            elif name == "next":
                decision["next"] = True
                decision["next_location"] = (center_x, center_y)
            elif name == "tree":
                decision["tree"] = True
                distance = ((center_x - screenx_center) ** 2 + (center_y - screeny_center) **2) **.5
                if "tree_location" in decision:
                    # Calculate if closer
                    if distance < decision["tree_distance"]:
                        decision["tree_location"] = (center_x, center_y)
                        decision["tree_distance"] = distance
                else:
                    decision["tree_location"] = (center_x, center_y)
                    decision["tree_distance"] = distance
            elif name == "building":
                decision["building"] = True
                distance = ((center_x - screenx_center) ** 2 + (center_y - screeny_center) **2) **.5
                if "building_location" in decision:
                    # Calculate if closer
                    if distance < decision["building_distance"]:
                        decision["building_location"] = (center_x, center_y)
                        decision["building_distance"] = distance
                else:
                    decision["building_location"] = (center_x, center_y)
                    decision["building_distance"] = distance
            elif name == "fuel":
                decision["fuel"] = True
                distance = ((center_x - screenx_center) ** 2 + (center_y - screeny_center) **2) **.5
                if "fuel_location" in decision:
                    # Calculate if closer
                    if distance < decision["fuel_distance"]:
                        decision["fuel_location"] = (center_x, center_y)
                        decision["fuel_distance"] = distance
                else:
                    decision["fuel_location"] = (center_x, center_y)
                    decision["fuel_distance"] = distance
        
        run_bot(decision)
        

# Main function
def main():
    print(pyautogui.KEYBOARD_KEYS)
    model = YOLO('best.pt')
    stop_event = threading.Event()
    
    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, args=(stop_event, model))
    screenshot_thread.start()

    # Listen for keyboard input to quit the program
    keyboard.wait("q")

    # Set the stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
