import tkinter as tk  
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import os
from image_processor import ImageProcessor
from gui_controls import ControlPanel, StatusBar


class ImageEditorGUI:
    """
    Main application class for the Image Editor GUI.  
    Demonstrates OOP principles: Class Interaction, Encapsulation, Constructor, and Methods.
    """

    def __init__(self, root):
        """
        Constructor: Initialize the main application window and components.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        
        self.root.title("Image Editor Professional Image Processing Application")
        self.root.geometry("1400x900")
        
        self.root.configure(bg='#1e1e2e')
        
        # Setup custom style
        self.setup_style()
        
        # Initialize image processor
        self.processor = ImageProcessor()
        self.current_image_path = ""
        self.photo_image = None
        
        # Create GUI components
        self.create_menu_bar()
        self.create_main_layout()
        
        # Set window icon and appearance
        self.root.resizable(True, True)

    def setup_style(self):
        """Configure custom ttk styles with modern colors."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color scheme
        bg_primary = '#1e1e2e'
        bg_secondary = '#2a2a3e'
        bg_tertiary = '#3a3a50'
        accent_color = '#00d4ff'
        accent_color_alt = '#ff006e'
        accent_color_success = '#00ff88'
        text_primary = '#ffffff'
        text_secondary = '#b0b0c0'
        
        # Configure TFrame
        style.configure('TFrame', background=bg_primary, foreground=text_primary)
        style.configure('Dark.TFrame', background=bg_secondary, foreground=text_primary)
        style.configure('Darker.TFrame', background=bg_tertiary, foreground=text_primary)
        
        # Configure TLabel
        style.configure('TLabel', background=bg_primary, foreground=text_primary, font=('Arial', 10))
        style.configure('Title.TLabel', background=bg_primary, foreground=accent_color, font=('Arial', 12, 'bold'))
        style.configure('Section.TLabel', background=bg_secondary, foreground=accent_color, font=('Arial', 11, 'bold'))
        style.configure('Status.TLabel', background=bg_tertiary, foreground=accent_color_success, font=('Arial', 12, 'bold'))
        
        # Configure TLabelFrame
        style.configure('TLabelframe', background=bg_secondary, foreground=accent_color, font=('Arial', 10, 'bold'), borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', background=bg_secondary, foreground=accent_color, font=('Arial', 10, 'bold'))
        
        # Configure TButton with gradient-like effect
        style.configure('TButton', 
                       background=accent_color, 
                       foreground='#000000',
                       font=('Arial', 10, 'bold'),
                       borderwidth=0,
                       padding=8,
                       relief='raised')
        style.map('TButton',
                 background=[('active', '#00ffff'), ('pressed', accent_color_alt)],
                 foreground=[('active', '#000000'), ('pressed', text_primary)])
        
        style.configure('Alt.TButton',
                       background=accent_color_alt,
                       foreground=text_primary,
                       font=('Arial', 10, 'bold'),
                       borderwidth=0,
                       padding=8)
        style.map('Alt.TButton',
                 background=[('active', '#ff3366'), ('pressed', '#cc0055')],
                 foreground=[('active', text_primary), ('pressed', text_primary)])
        
        # Configure TScale
        style.configure('TScale', background=bg_secondary, foreground=accent_color)
        
        # Configure Scrollbar
        style.configure('TScrollbar', background=bg_tertiary, troughcolor=bg_secondary, arrowcolor=accent_color)

    def create_menu_bar(self):
        """Create the menu bar with File and Edit menus."""
        menubar = tk.Menu(self.root, bg='#2a2a3e', fg='#00d4ff', activebackground='#ff006e', activeforeground='#ffffff', font=('Arial', 10, 'bold'))
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, bg='#2a2a3e', fg='#ffffff', activebackground='#00d4ff', activeforeground='#000000', font=('Arial', 10))
        menubar.add_cascade(label="File", menu=file_menu, foreground='#00d4ff')
        file_menu.add_command(label="Open", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_image_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")

        # Edit menu
        edit_menu = tk.Menu(menubar, bg='#2a2a3e', fg='#ffffff', activebackground='#00d4ff', activeforeground='#000000', font=('Arial', 10))
        menubar.add_cascade(label="Edit", menu=edit_menu, foreground='#00ff88')
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")

        # Help menu
        help_menu = tk.Menu(menubar, bg='#2a2a3e', fg='#ffffff', activebackground='#00d4ff', activeforeground='#000000', font=('Arial', 10))
        menubar.add_cascade(label="Help", menu=help_menu, foreground='#ff006e')
        help_menu.add_command(label="About", command=self.show_about)

        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_image_as())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())

    def create_main_layout(self):
        """Create the main layout with image display and control panel."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header frame
        header_frame = ttk.Frame(self.root, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(5, 10), padx=5)
        
        header_label = ttk.Label(header_frame, text="Professional Image Editor", style='Title.TLabel')
        header_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Left panel - Control panel
        left_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))

        left_title = ttk.Label(left_frame, text="Controls Panel", style='Section.TLabel')
        left_title.pack(fill=tk.X, padx=5, pady=(0, 10))

        scroll_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_frame, bg='#2a2a3e', highlightthickness=0, relief=tk.FLAT)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg='#2a2a3e')

        # Create control panel inside scrollable frame
        self.control_panel = ControlPanel(scrollable_frame, self.processor, self.update_display)
        self.control_panel.frame.pack(fill=tk.BOTH, expand=True)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right panel - Image display
        right_frame = ttk.Frame(main_frame, style='Darker.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        right_title = ttk.Label(right_frame, text="Image Preview", style='Section.TLabel')
        right_title.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Image display canvas with border
        canvas_frame = ttk.Frame(right_frame, style='Darker.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_canvas = tk.Canvas(canvas_frame, bg='#0a0a0f', cursor="cross", relief=tk.SUNKEN, bd=3, highlightthickness=0)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar at bottom
        self.status_bar = StatusBar(self.root)
        self.status_bar.set_status("Ready - Open an image to start editing")

    def open_image(self):
        """Open image file dialog and load image."""
        file_types = [("Image files", "*.jpg *.jpeg *.png *.bmp *.JPG *.JPEG *.PNG *.BMP"),
                      ("All files", "*.*")]
        
        try:
            file_path = filedialog.askopenfilename(
                title="Open Image",
                filetypes=file_types
            )

            if file_path:
                if not os.path.exists(file_path):
                    messagebox.showerror("Error", "File does not exist.")
                    return
                
                if self.processor.load_image(file_path):
                    self.current_image_path = file_path
                    self.update_display()
                    self.status_bar.set_status(f"Loaded: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Failed to load image. Unsupported format or corrupted file.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {str(e)}")

    def save_image(self):
        """Save the current image."""
        if self.processor.current_image is None:
            messagebox.showwarning("Warning", "No image to save. Please open an image first.")
            return

        if not self.current_image_path:
            self.save_image_as()
        else:
            try:
                if self.processor.save_image(self.current_image_path):
                    messagebox.showinfo("Success", "Image saved successfully")
                    self.status_bar.set_status(f"Saved: {os.path.basename(self.current_image_path)}")
                else:
                    messagebox.showerror("Error", "Failed to save image. Check file permissions.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")

    def save_image_as(self):
        """Save image with a new filename."""
        if self.processor.current_image is None:
            messagebox.showwarning("Warning", "No image to save. Please open an image first.")
            return

        file_types = [("JPEG files", "*.jpg *.jpeg"),
                      ("PNG files", "*.png"),
                      ("BMP files", "*.bmp"),
                      ("All files", "*.*")]
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Image As",
                filetypes=file_types,
                defaultextension=".png"
            )

            if file_path:
                if self.processor.save_image(file_path):
                    self.current_image_path = file_path
                    messagebox.showinfo("Success", "Image saved successfully")
                    self.status_bar.set_status(f"Saved: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Failed to save image. Check file permissions or disk space.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {str(e)}")

    def undo(self):
        """Undo last operation."""
        try:
            if self.processor.undo():
                self.update_display()
                self.status_bar.set_status("Undo completed")
            else:
                messagebox.showinfo("Info", "No more operations to undo")
        except Exception as e:
            messagebox.showerror("Error", f"Error during undo: {str(e)}")

    def redo(self):
        """Redo last undone operation."""
        try:
            if self.processor.redo():
                self.update_display()
                self.status_bar.set_status("Redo completed")
            else:
                messagebox.showinfo("Info", "No more operations to redo")
        except Exception as e:
            messagebox.showerror("Error", f"Error during redo: {str(e)}")

    def update_display(self):
        """Update the image display on canvas."""
        try:
            image = self.processor.get_image()
            
            if image is None:
                self.status_bar.set_status("No image loaded")
                return

            # Convert to PIL Image
            pil_image = Image.fromarray(image)
            
            # Scale image to fit canvas
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 600

            # Maintain aspect ratio
            img_width, img_height = pil_image.size
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            if scale < 1:
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(pil_image)

            # Update canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.photo_image
            )

            # Update status bar
            width, height = self.processor.get_image_dimensions()
            filename = os.path.basename(self.current_image_path) if self.current_image_path else "Unnamed"
            self.status_bar.update_status(filename, width, height)
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {str(e)}")

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "Image Editor v1.0\n\n"
            "A desktop application for image processing using:\n"
            "- OpenCV for image processing\n"
            "- Tkinter for GUI\n"
            "- Python OOP principles\n\n"
            "Features:\n"
            "- Multiple filters (grayscale, blur, edges)\n"
            "- Image adjustments (brightness, contrast)\n"
            "- Transformations (rotate, flip, resize)\n"
            "- Undo/Redo functionality"
        )


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = ImageEditorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
