import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import ImageProcessor
import os


class ControlPanel:
    """Control panel for image processing UI."""

    def __init__(self, parent, image_processor: ImageProcessor, callback):
        """Initialize control panel with parent, processor, and callback."""
        self.processor = image_processor
        self.callback = callback
        self.frame = ttk.Frame(parent, style='Dark.TFrame')
        self.create_controls()

    def create_controls(self):
        """Create all control buttons and sliders."""
        # Blur intensity slider
        blur_frame = ttk.LabelFrame(self.frame, text="Blur Intensity", padding=10)
        blur_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.blur_var = tk.IntVar(value=5)
        blur_slider = ttk.Scale(blur_frame, from_=1, to=31, orient=tk.HORIZONTAL,
                               variable=self.blur_var, command=lambda x: self.apply_blur())
        blur_slider.pack(fill=tk.X)
        self.blur_label = ttk.Label(blur_frame, text="Intensity: 5", style='TLabel')
        self.blur_label.pack()

        # Brightness slider
        brightness_frame = ttk.LabelFrame(self.frame, text="Brightness", padding=10)
        brightness_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.brightness_var = tk.DoubleVar(value=1.0)
        brightness_slider = ttk.Scale(brightness_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                     variable=self.brightness_var, command=lambda x: self.apply_brightness())
        brightness_slider.pack(fill=tk.X)
        self.brightness_label = ttk.Label(brightness_frame, text="Factor: 1.0", style='TLabel')
        self.brightness_label.pack()

        # Contrast slider
        contrast_frame = ttk.LabelFrame(self.frame, text="Contrast", padding=10)
        contrast_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_slider = ttk.Scale(contrast_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                   variable=self.contrast_var, command=lambda x: self.apply_contrast())
        contrast_slider.pack(fill=tk.X)
        self.contrast_label = ttk.Label(contrast_frame, text="Factor: 1.0", style='TLabel')
        self.contrast_label.pack()

        # Filter buttons
        filter_frame = ttk.LabelFrame(self.frame, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="Grayscale", command=self.apply_grayscale).pack(fill=tk.X, pady=2)
        ttk.Button(filter_frame, text="Edge Detection", command=self.apply_edges).pack(fill=tk.X, pady=2)

        # Transformation buttons
        transform_frame = ttk.LabelFrame(self.frame, text="Transform", padding=10)
        transform_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(transform_frame, text="Rotate 90", command=lambda: self.rotate(90)).pack(fill=tk.X, pady=2)
        ttk.Button(transform_frame, text="Rotate 180", command=lambda: self.rotate(180)).pack(fill=tk.X, pady=2)
        ttk.Button(transform_frame, text="Rotate 270", command=lambda: self.rotate(270)).pack(fill=tk.X, pady=2)
        ttk.Button(transform_frame, text="Flip Horizontal", command=lambda: self.flip('horizontal')).pack(fill=tk.X, pady=2)
        ttk.Button(transform_frame, text="Flip Vertical", command=lambda: self.flip('vertical')).pack(fill=tk.X, pady=2)

        # Resize
        resize_frame = ttk.LabelFrame(self.frame, text="Resize", padding=10)
        resize_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(resize_frame, text="Resize Image", command=self.resize_dialog).pack(fill=tk.X, pady=2)

        # Reset
        reset_frame = ttk.LabelFrame(self.frame, text="Reset", padding=10)
        reset_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(reset_frame, text="Reset to Original", command=self.reset_image, style='Alt.TButton').pack(fill=tk.X, pady=2)

    def apply_grayscale(self):
        """Apply grayscale filter."""
        try:
            if self.processor.convert_grayscale():
                self.callback()
            else:
                messagebox.showerror("Error", "Failed to apply grayscale filter")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying grayscale: {str(e)}")

    def apply_edges(self):
        """Apply edge detection."""
        try:
            if self.processor.detect_edges():
                self.callback()
            else:
                messagebox.showerror("Error", "Failed to apply edge detection")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying edge detection: {str(e)}")

    def apply_blur(self):
        """Apply blur with current slider value."""
        try:
            intensity = int(self.blur_var.get())
            self.blur_label.config(text=f"Intensity: {intensity}")
            if self.processor.apply_blur(intensity):
                self.callback()
            else:
                messagebox.showerror("Error", "Failed to apply blur")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying blur: {str(e)}")

    def apply_brightness(self):
        """Apply brightness adjustment."""
        try:
            factor = float(self.brightness_var.get())
            self.brightness_label.config(text=f"Factor: {factor:.2f}")
            if self.processor.adjust_brightness(factor):
                self.callback()
            else:
                messagebox.showerror("Error", "Failed to apply brightness adjustment")
        except Exception as e:
            messagebox.showerror("Error", f"Error adjusting brightness: {str(e)}")

    def apply_contrast(self):
        """Apply contrast adjustment."""
        try:
            factor = float(self.contrast_var.get())
            self.contrast_label.config(text=f"Factor: {factor:.2f}")
            if self.processor.adjust_contrast(factor):
                self.callback()
            else:
                messagebox.showerror("Error", "Failed to apply contrast adjustment")
        except Exception as e:
            messagebox.showerror("Error", f"Error adjusting contrast: {str(e)}")

    def rotate(self, angle):
        """Rotate image."""
        try:
            if self.processor.rotate_image(angle):
                self.callback()
            else:
                messagebox.showerror("Error", f"Failed to rotate image by {angle} degrees")
        except Exception as e:
            messagebox.showerror("Error", f"Error rotating image: {str(e)}")

    def flip(self, direction):
        """Flip image."""
        try:
            if self.processor.flip_image(direction):
                self.callback()
            else:
                messagebox.showerror("Error", f"Failed to flip image {direction}")
        except Exception as e:
            messagebox.showerror("Error", f"Error flipping image: {str(e)}")

    def resize_dialog(self):
        """Open dialog for image resizing."""
        try:
            current_w, current_h = self.processor.get_image_dimensions()
            
            dialog = tk.Toplevel()
            dialog.title("Resize Image")
            dialog.geometry("300x150")
            dialog.resizable(False, False)
            
            ttk.Label(dialog, text=f"Current Size: {current_w}x{current_h}").pack(pady=10)
            
            ttk.Label(dialog, text="Width:").pack(side=tk.LEFT, padx=5)
            width_var = tk.StringVar(value=str(current_w))
            ttk.Entry(dialog, textvariable=width_var, width=10).pack(side=tk.LEFT, padx=5)
            
            ttk.Label(dialog, text="Height:").pack(side=tk.LEFT, padx=5)
            height_var = tk.StringVar(value=str(current_h))
            ttk.Entry(dialog, textvariable=height_var, width=10).pack(side=tk.LEFT, padx=5)
            
            def apply_resize():
                try:
                    width = int(width_var.get())
                    height = int(height_var.get())
                    if width > 0 and height > 0:
                        if self.processor.resize_image(width, height):
                            self.callback()
                            dialog.destroy()
                            messagebox.showinfo("Success", "Image resized successfully")
                        else:
                            messagebox.showerror("Error", "Failed to resize image")
                    else:
                        messagebox.showerror("Invalid Input", "Width and height must be positive")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers")
                except Exception as e:
                    messagebox.showerror("Error", f"Error resizing image: {str(e)}")
            
            ttk.Button(dialog, text="Apply", command=apply_resize).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening resize dialog: {str(e)}")

    def reset_image(self):
        """Reset image to original."""
        try:
            if self.processor.reset_image():
                self.callback()
                messagebox.showinfo("Success", "Image reset to original")
            else:
                messagebox.showerror("Error", "Failed to reset image")
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting image: {str(e)}")


class StatusBar:
    """Status bar display component."""

    def __init__(self, parent):
        """Initialize status bar with parent widget."""
        self.label = ttk.Label(parent, text="Ready", relief=tk.SUNKEN, anchor=tk.W, style='Status.TLabel')
        self.label.pack(fill=tk.X, side=tk.BOTTOM)

    def update_status(self, filename: str, width: int, height: int):
        """Update status bar with image information."""
        status_text = f"File: {filename}  |  Dimensions: {width}x{height} px"
        self.label.config(text=status_text)

    def set_status(self, message: str):
        """Set custom status message."""
        self.label.config(text=f"{message}")
