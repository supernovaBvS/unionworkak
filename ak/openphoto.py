import cv2

# Load the image from file
image_path = '/Users/dev/Desktop/1 aug 2023/SUNP0018.JPG'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is not None:
    # Display the image in a window
    cv2.imshow('Image', image)

    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error loading the image.")