import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_skew_angle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Detect coordinates of non-zero pixels
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Correct angle logic
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    print(f"[INFO] Detected angle: {angle:.2f} degrees")
    return angle

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def deskew_image(image_path):
    image = cv2.imread(image_path)
    angle = compute_skew_angle(image)
    rotated = rotate_image(image, angle)

    # Show input and output
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Skewed Image')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
    plt.title('Deskewed Image')

    plt.show()

# Example usage:
deskew_image('download.jpeg')  # Replace with your file path
