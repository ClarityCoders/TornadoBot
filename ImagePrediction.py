from ultralytics import YOLO

# Load a model
model = YOLO('best.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
screenx_center = 3840/2
screeny_center = 2160/2

decision = {
    "buy": False,
    "play": False,
    "continue": False,
    "next": False,
    "tornado": False,
    "tree": False,
    "building": False,
}

results = model(['test4.png'], conf=.80, save=True)  # return a list of Results objects
boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# Process results list
for box, cls, conf in zip(boxes, classes, confidences):
    x1, y1, x2, y2 = box
    
    center_x = (x1+x2) / 2
    center_y = (y1+y2) / 2

    confidence = conf
    detected_class = cls
    name = names[int(cls)]
    
    if name=="buy":
        decision["buy"] = True
        decision["buy_location"] = (center_x, center_y)
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
    
print(decision)