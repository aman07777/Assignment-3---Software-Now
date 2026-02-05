import cv2
import numpy as np
from typing import Optional, Tuple
import copy


class ImageProcessor:
    """Image processing operations using OpenCV."""

    def __init__(self, image_path: Optional[str] = None):
        """Initialize processor with optional image path."""
        self.original_image = None
        self.current_image = None
        self.image_path = image_path
        self.history = []
        self.history_index = -1

        if image_path:
            self.load_image(image_path)

    def load_image(self, image_path: str) -> bool:
        """Load an image from file path."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return False
            self.original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.current_image = copy.deepcopy(self.original_image)
            self.image_path = image_path
            self.history = []
            self.history_index = -1
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False

    def save_image(self, file_path: str) -> bool:
        """Save the current image to file."""
        try:
            if self.current_image is None:
                return False
            # Convert RGB back to BGR for OpenCV
            image_bgr = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, image_bgr)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def _save_to_history(self):
        """Save current state to history for undo/redo functionality."""
        # Remove any redo history if we make a new edit
        self.history = self.history[:self.history_index + 1]
        self.history.append(copy.deepcopy(self.current_image))
        self.history_index += 1

    def undo(self) -> bool:
        """Undo the last operation."""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = copy.deepcopy(self.history[self.history_index])
            return True
        return False

    def redo(self) -> bool:
        """Redo the last undone operation."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = copy.deepcopy(self.history[self.history_index])
            return True
        return False

    def get_image(self) -> Optional[np.ndarray]:
        """Get the current image"""
        return self.current_image

    def get_image_dimensions(self) -> Tuple[int, int]:
        """Get the dimensions of the current image"""
        if self.current_image is None:
            return (0, 0)
        return (self.current_image.shape[1], self.current_image.shape[0])

    def convert_grayscale(self):
        """Convert image to grayscale."""
        if self.current_image is None:
            return False
        self._save_to_history()
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        return True

    def apply_blur(self, intensity: int = 5) -> bool:
        """Apply Gaussian blur to the image (intensity must be odd)"""
        if self.current_image is None:
            return False
        self._save_to_history()
        # Ensure intensity is odd
        intensity = max(1, intensity if intensity % 2 == 1 else intensity + 1)
        self.current_image = cv2.GaussianBlur(self.current_image, (intensity, intensity), 0)
        return True

    def detect_edges(self, threshold1: int = 100, threshold2: int = 200) -> bool:
        """Apply Canny edge detection to the image."""
        if self.current_image is None:
            return False
        self._save_to_history()
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        return True

    def adjust_brightness(self, factor: float = 1.0) -> bool:
        """Adjust image brightness by given factor."""
        if self.current_image is None:
            return False
        self._save_to_history()
        hsv = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 2] = hsv[:, :, 2] * factor
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        self.current_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        return True

    def adjust_contrast(self, factor: float = 1.0) -> bool:
        """Adjust image contrast by given factor."""
        if self.current_image is None:
            return False
        self._save_to_history()
        img = self.current_image.astype(np.float32)
        mean = np.mean(img, axis=(0, 1))
        img = (img - mean) * factor + mean
        img = np.clip(img, 0, 255)
        self.current_image = img.astype(np.uint8)
        return True

    def rotate_image(self, angle: int) -> bool:
        """Rotate image by the specified angle (90/180/270)."""
        if self.current_image is None:
            return False
        self._save_to_history()
        
        if angle == 90:
            self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif angle == 180:
            self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_180)
        elif angle == 270:
            self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_CLOCKWISE)
        else:
            return False
        
        return True

    def flip_image(self, direction: str = 'horizontal') -> bool:
        """Flip image horizontally or vertically."""
        if self.current_image is None:
            return False
        self._save_to_history()
        
        if direction.lower() == 'horizontal':
            self.current_image = cv2.flip(self.current_image, 1)
        elif direction.lower() == 'vertical':
            self.current_image = cv2.flip(self.current_image, 0)
        else:
            return False
        
        return True

    def resize_image(self, width: int, height: int) -> bool:
        """Resize the image to specified width and height."""
        if self.current_image is None:
            return False
        self._save_to_history()
        
        self.current_image = cv2.resize(self.current_image, (width, height))
        return True

    def reset_image(self) -> bool:
        """Reset image to original."""
        if self.original_image is None:
            return False
        self.current_image = copy.deepcopy(self.original_image)
        self.history = []
        self.history_index = -1
        return True
