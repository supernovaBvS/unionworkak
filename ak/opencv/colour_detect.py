import cv2
import numpy as np

def color_detection(image, area):
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the ranges for different colors in HSV
    color_ranges = {
        'red': ([0, 70, 50], [10, 255, 255]),
        'orange': ([11, 70, 50], [25, 255, 255]),
        'yellow': ([26, 70, 50], [35, 255, 255]),
        'green': ([36, 70, 50], [70, 255, 255]),
        'blue': ([100, 70, 50], [130, 255, 255]),
        'purple': ([131, 70, 50], [160, 255, 255]),
        'pink': ([161, 70, 50], [179, 255, 255]),
        'white': ([0, 0, 200], [179, 30, 255]),
        'black': ([0, 0, 0], [179, 255, 30]),
        'gray': ([0, 0, 31], [179, 30, 230]),
        'brown': ([8, 70, 50], [20, 255, 255]),
        'cyan': ([81, 70, 50], [100, 255, 255]),
        'magenta': ([141, 70, 50], [160, 255, 255]),
        'gold': ([21, 70, 50], [40, 255, 255]),
        'silver': ([0, 0, 111], [179, 30, 190]),
        'maroon': ([0, 70, 50], [10, 255, 255]),
        'navy': ([100, 70, 50], [140, 255, 255]),
        'teal': ([71, 70, 50], [100, 255, 255]),
        'indigo': ([101, 70, 50], [130, 255, 255]),
        'lime': ([36, 70, 50], [70, 255, 255]),
        'olive': ([26, 70, 50], [45, 255, 255]),
        'aqua': ([76, 70, 50], [100, 255, 255]),
        'azure': ([91, 70, 50], [110, 255, 255]),
        'beige': ([26, 20, 150], [45, 100, 255]),
        'bisque': ([6, 30, 150], [20, 100, 255]),
        'chartreuse': ([36, 70, 50], [70, 255, 255]),
        'coral': ([1, 70, 50], [8, 255, 255]),
        'crimson': ([170, 70, 50], [180, 255, 255]),
        'fuchsia': ([141, 70, 50], [160, 255, 255]),
        'gainsboro': ([0, 0, 190], [179, 30, 220]),
        'goldenrod': ([26, 70, 50], [35, 255, 255]),
        'indianred': ([0, 70, 50], [5, 255, 255]),
        'ivory': ([0, 0, 200], [179, 20, 255]),
        'khaki': ([26, 30, 150], [45, 100, 255]),
        'lavender': ([131, 20, 150], [161, 100, 255]),
        'lemonchiffon': ([26, 100, 200], [45, 255, 255]),
        'lightblue': ([91, 20, 150], [130, 100, 255]),
        'lightcoral': ([1, 30, 150], [8, 100, 255]),
        'lightcyan': ([76, 20, 150], [100, 100, 255]),
        'lightgoldenrodyellow': ([26, 30, 150], [35, 100, 255]),
        'lightgray': ([0, 0, 180], [179, 30, 230]),
        'lightgreen': ([36, 30, 150], [70, 100, 255]),
        'lightpink': ([161, 30, 150], [179, 100, 255]),
        'lightsalmon': ([6, 30, 150], [20, 100, 255]),
        'lightseagreen': ([71, 30, 150], [100, 100, 255]),
        'lightskyblue': ([101, 20, 150], [130, 100, 255]),
        'lightslategray': ([101, 0, 100], [130, 30, 180]),
        'lightsteelblue': ([76, 0, 150], [100, 30, 230]),
        'lightyellow': ([21, 30, 200], [40, 100, 255]),
        'limegreen': ([36, 70, 50], [70, 255, 255]),
        'moccasin': ([6, 30, 150], [20, 100, 255]),
        'oldlace': ([21, 20, 200], [40, 100, 255]),
        'orchid': ([131, 70, 50], [161, 255, 255]),
        'palegreen': ([36, 20, 150], [70, 100, 255]),
        'peachpuff': ([11, 30, 150], [25, 100, 255]),
        'peru': ([6, 70, 50], [20, 255, 255]),
        'plum': ([131, 30, 150], [161, 100, 255]),
        'rosybrown': ([1, 30, 100], [8, 100, 200]),
        'seashell': ([0, 0, 200], [179, 30, 255]),
        'sienna': ([1, 70, 50], [8, 255, 255]),
        'skyblue': ([101, 30, 150], [130, 100, 255]),
        'slategray': ([101, 0, 70], [130, 30, 180]),
        'springgreen': ([71, 70, 50], [100, 255, 255]),
        'tan': ([11, 70, 50], [25, 255, 255]),
        'thistle': ([131, 20, 150], [161, 100, 255]),
        'tomato': ([1, 70, 50], [8, 255, 255]),
        'turquoise': ([71, 70, 50], [100, 255, 255]),
        'violet': ([141, 30, 150], [160, 100, 255]),
        'wheat': ([21, 30, 150], [40, 100, 255]),
        'whitesmoke': ([0, 0, 230], [179, 20, 255]),
        'yellowgreen': ([36, 70, 50], [70, 255, 255]),
        'aliceblue': ([101, 30, 200], [130, 100, 255]),
        'antiquewhite': ([0, 20, 200], [30, 100, 255]),
        'aquamarine': ([76, 30, 150], [100, 100, 255]),
        'blueviolet': ([131, 70, 50], [160, 255, 255]),
        'burlywood': ([11, 30, 150], [25, 100, 255]),
        'cadetblue': ([91, 30, 150], [110, 100, 255]),
        'cornflowerblue': ([101, 30, 150], [130, 100, 255]),
        'darkblue': ([100, 70, 50], [140, 255, 255]),
        'darkcyan': ([81, 70, 50], [100, 255, 255]),
        'darkgoldenrod': ([21, 70, 50], [35, 255, 255]),
        'darkgray': ([0, 0, 100], [179, 30, 180]),
        'darkgreen': ([36, 70, 50], [70, 255, 255]),
        'darkkhaki': ([26, 30, 150], [45, 100, 255]),
        'darkmagenta': ([141, 70, 50], [160, 255, 255]),
        'darkolivegreen': ([36, 30, 50], [70, 100, 255]),
        'darkorange': ([11, 70, 50], [25, 255, 255]),
        'darkorchid': ([131, 70, 50], [160, 255, 255]),
        'darkred': ([0, 70, 50], [10, 255, 255]),
        'darksalmon': ([6, 30, 150], [20, 100, 255]),
        'darkseagreen': ([71, 30, 50], [100, 100, 255]),
        'darkslateblue': ([101, 30, 50], [130, 100, 255]),
        'darkslategray': ([101, 0, 70], [130, 30, 180]),
        'darkturquoise': ([71, 70, 50], [100, 255, 255]),
        'darkviolet': ([141, 70, 50], [160, 255, 255]),
        'deeppink': ([161, 70, 50], [179, 255, 255]),
        'deepskyblue': ([101, 70, 50], [130, 255, 255]),
        'dimgray': ([0, 0, 70], [179, 30, 105]),
        'dodgerblue': ([91, 70, 50], [110, 255, 255]),
        'firebrick': ([1, 70, 50], [8, 255, 255]),
        'floralwhite': ([0, 20, 200], [30, 100, 255]),
        'forestgreen': ([36, 30, 50], [70, 100, 255]),
        'ghostwhite': ([0, 0, 200], [179, 30, 255]),
        'greenyellow': ([36, 70, 50], [70, 255, 255]),
        'honeydew': ([76, 0, 200], [100, 30, 255]),
        'hotpink': ([141, 70, 50], [160, 255, 255]),
        'indianred': ([0, 70, 50], [5, 255, 255]),
        'khaki': ([26, 30, 150], [45, 100, 255]),
        'lavenderblush': ([161, 20, 200], [179, 100, 255]),
        'lawngreen': ([36, 70, 50], [70, 255, 255]),
        'lightcoral': ([1, 30, 150], [8, 100, 255]),
        'lightcyan': ([76, 20, 150], [100, 100, 255]),
        'lightgoldenrod': ([26, 30, 150], [35, 100, 255]),
        'lightgray': ([0, 0, 180], [179, 30, 230]),
        'lightgreen': ([36, 30, 150], [70, 100, 255]),
        'lightpink': ([161, 30, 150], [179, 100, 255]),
        'lightsalmon': ([6, 30, 150], [20, 100, 255]),
        'aliceblue': ([101, 30, 200], [130, 100, 255]),
        'antiquewhite': ([0, 20, 200], [30, 100, 255]),
        'aquamarine': ([76, 30, 150], [100, 100, 255]),
        'blueviolet': ([131, 70, 50], [160, 255, 255]),
        'burlywood': ([11, 30, 150], [25, 100, 255]),
        'cadetblue': ([91, 30, 150], [110, 100, 255]),
        'cornflowerblue': ([101, 30, 150], [130, 100, 255]),
        'darkblue': ([100, 70, 50], [140, 255, 255]),
        'darkcyan': ([81, 70, 50], [100, 255, 255]),
        'darkgoldenrod': ([21, 70, 50], [35, 255, 255]),
        'darkgray': ([0, 0, 100], [179, 30, 180]),
        'darkgreen': ([36, 70, 50], [70, 255, 255]),
        'darkkhaki': ([26, 30, 150], [45, 100, 255]),
        'darkmagenta': ([141, 70, 50], [160, 255, 255]),
        'darkolivegreen': ([36, 30, 50], [70, 100, 255]),
        'darkorange': ([11, 70, 50], [25, 255, 255]),
        'darkorchid': ([131, 70, 50], [160, 255, 255]),
        'darkred': ([0, 70, 50], [10, 255, 255]),
        'darksalmon': ([6, 30, 150], [20, 100, 255]),
        'darkseagreen': ([71, 30, 50], [100, 100, 255]),
        'darkslateblue': ([101, 30, 50], [130, 100, 255]),
        'darkslategray': ([101, 0, 70], [130, 30, 180]),
        'darkturquoise': ([71, 70, 50], [100, 255, 255]),
        'darkviolet': ([141, 70, 50], [160, 255, 255]),
        'deeppink': ([161, 70, 50], [179, 255, 255]),
        'deepskyblue': ([101, 70, 50], [130, 255, 255]),
        'dimgray': ([0, 0, 70], [179, 30, 105]),
        'dodgerblue': ([91, 70, 50], [110, 255, 255]),
        'firebrick': ([1, 70, 50], [8, 255, 255]),
        'floralwhite': ([0, 20, 200], [30, 100, 255]),
        'forestgreen': ([36, 30, 50], [70, 100, 255]),
        'ghostwhite': ([0, 0, 200], [179, 30, 255]),
        'greenyellow': ([36, 70, 50], [70, 255, 255]),
        'honeydew': ([76, 0, 200], [100, 30, 255]),
        'hotpink': ([141, 70, 50], [160, 255, 255]),
        'indianred': ([0, 70, 50], [5, 255, 255]),
        'khaki': ([26, 30, 150], [45, 100, 255]),
        'lavenderblush': ([161, 20, 200], [179, 100, 255]),
        'lawngreen': ([36, 70, 50], [70, 255, 255]),
    }
    
    # Extract the area for color detection
    x, y, w, h = area
    roi = hsv_image[y:y+h, x:x+w]
    
    # Iterate over each color range and check if the image matches
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(roi, lower, upper)
        percentage = np.sum(mask == 255) / (mask.shape[0] * mask.shape[1])
        
        # Check if a significant portion of the image matches the color
        if percentage > 0.1:
            return color
    
    return 'unknown'  # Return 'unknown' if no color is detected significantly

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Define the dimensions and position of the color detection area
area_x = 500
area_y = 600
area_width = 50
area_height = 50

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    # Create a black box as the text background
    cv2.rectangle(frame, (10, 10), (300, 70), (0, 0, 0), -1)
    
    # Perform color detection
    detected_color = color_detection(frame, (area_x, area_y, area_width, area_height))

    # Display the color text on the frame
    cv2.putText(frame, 'Detected color: ' + detected_color, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Draw a box in the center for color detection
    cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Color Detection', frame)
    
    # Get the key pressed
    key = cv2.waitKey(1)
    
    # Move the color detection area based on arrow key presses
    if key & 0xFF == ord('w') and area_y > 0:  # Up arrow key
        area_y -= 100
    elif key & 0xFF == ord('s') and area_y + area_height < frame.shape[0]:  # Down arrow key
        area_y += 90
    elif key & 0xFF == ord('a') and area_x > 0:  # Left arrow key
        area_x -= 100
    elif key & 0xFF == ord('d') and area_x + area_height < frame.shape[1]:  # Right arrow key
        area_x += 90
    
    # Exit the loop if 'q' is pressed
    if key == 27:
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
