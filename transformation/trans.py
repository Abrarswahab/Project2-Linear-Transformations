import cv2
import numpy as np
import matplotlib.pyplot as plt


class Transformations:
  # Store the image and extract its height and width
    def __init__(self, image):
        self.image = image
        self.h, self.w = image.shape[:2]

    # 1. Scaling: Changes image size
    def scaling(self, scale_x, scale_y):
      # Define the diagonal matrix for scaling coordinates
        scaling_matrix = np.float32([
            [scale_x, 0, 0],
             [0, scale_y, 0]])
        # Calculate new dimensions based on scale factors
        scaled_img = cv2.warpAffine(
            self.image,
            scaling_matrix,
            (int(self.image.shape[1] * scale_x), int(self.image.shape[0] * scale_y))
        )
        # Apply the transformation to the pixels
        return scaled_img


    # 2. Rotation: Turns the image
    def rotate(self, angle):
        # Convert the angle to radians
        theta = np.radians(angle)

        # Define cos and sin
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # Center of the image
        cx = self.w / 2
        cy = self.h / 2

        # Build matrix manually
        rotation_matrix = np.array([
            [cos_t, -sin_t, (1 - cos_t) * cx + sin_t * cy],
            [sin_t,  cos_t, (1 - cos_t) * cy - sin_t * cx]
        ], dtype=np.float32)

        rotated_img = cv2.warpAffine(self.image, rotation_matrix, (self.w, self.h))

        return rotated_img

    # 3. Shear: Slants the image
    def shear(self, k):
        # 1. Get dimensions from the image array
        h, w, c = self.image.shape
        # 2. Calculate new width to prevent cropping (Math: w + |k|*h)
        new_w = int(w + abs(k) * h)
        # 3. Create an empty canvas (Black background)
        sheared_img = np.zeros((h, new_w, c), dtype=np.uint8)
        # 4. Apply the Shear formula manually row by row
        for y in range(h):
            shift = int(k * y)
            # Copy the original row into the shifted position
            sheared_img[y, shift : shift + w] = self.image[y]
        return sheared_img

    # 4. Horizontal Reflection: Mirror effect
    def reflect_horizontal(self):
        # Matrix to negate X-axis and shift it back by width (w)
        m_reflect_h = np.float32([
            [-1, 0, self.w],
            [0, 1, 0]])
        return cv2.warpAffine(self.image, m_reflect_h, (self.w, self.h))

    # 5. Vertical Reflection: Upside down effect
    def reflect_vertical(self):
        # Matrix to negate Y-axis and shift it back by height (h)
        m_reflect_v = np.float32([
            [1, 0, 0],
             [0, -1, self.h]])
        return cv2.warpAffine(self.image, m_reflect_v, (self.w, self.h))

    # Display Function: Visualizes before and after
    def display(self, transformed_img, title):
        # Set up a figure with two side-by-side plots
        plt.figure(figsize=(10, 5))
        # Plot the original image for comparison
        plt.subplot(1, 2, 1)
        plt.imshow(self.image)
        plt.title("Original Image")
        plt.axis('off')
        # Plot the resulting transformed image
        plt.subplot(1, 2, 2)
        plt.imshow(transformed_img)
        plt.title(title)
        plt.axis('off')
        plt.show()

print("✅ Transformations Class is ready!")