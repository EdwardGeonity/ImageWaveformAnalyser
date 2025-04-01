import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from datetime import datetime
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFilter, ImageOps
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define resampling method depending on Pillow version
if hasattr(Image, 'Resampling'):
    RESAMPLE_METHOD = Image.Resampling.LANCZOS
else:
    RESAMPLE_METHOD = Image.ANTIALIAS

class ImageEditor:
    def __init__(self, root):
        self.root = root
        root.title("Image ADB Waveform Analyzer")
        self.original_image = None  
        self.processed_image = None  

        # Frame for displaying the image
        self.frame_image = tk.Frame(root, bd=2, relief="sunken")
        self.frame_image.grid(row=0, column=0, padx=5, pady=5)

        # Frame for waveform scope (combined RGB graph)
        self.frame_waveform = tk.Frame(root, bd=2, relief="sunken")
        self.frame_waveform.grid(row=0, column=1, padx=5, pady=5)

        # Frame for color correction controls
        self.frame_controls = tk.Frame(root)
        self.frame_controls.grid(row=0, column=2, padx=5, pady=5, sticky="n")

        # Frame for Spatial (radius of the circle)
        self.frame_spatial = tk.Frame(root, bd=2, relief="sunken")
        self.frame_spatial.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Canvas for image display (600x450)
        self.image_canvas = tk.Canvas(self.frame_image, width=600, height=450, bg="gray")
        self.image_canvas.pack(padx=5, pady=5)

        # Open Image button
        self.btn_open = tk.Button(self.frame_image, text="Open Image", command=self.open_image)
        self.btn_open.pack(pady=5)

        # Frame for ADB buttons (next to Open Image)
        self.adb_frame = tk.Frame(self.frame_image)
        self.adb_frame.pack(pady=5)
        self.btn_adb_connect = tk.Button(self.adb_frame, text="ADB CONNECT", command=self.adb_connect)
        self.btn_adb_connect.pack(side=tk.LEFT, padx=5)
        self.btn_adb_take = tk.Button(self.adb_frame, text="ADB TAKE IMAGE", command=self.adb_take_image)
        self.btn_adb_take.pack(side=tk.LEFT, padx=5)
        self.btn_load_image = tk.Button(self.adb_frame, text="LOAD IMAGE", command=self.adb_get_image)
        self.btn_load_image.pack(side=tk.LEFT, padx=5)

        # Create a Matplotlib figure for waveform scope (600x450)
        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("RGB Waveform")
        self.ax.set_xlabel("Width (pixels)")
        self.ax.set_ylabel("Brightness")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_waveform)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Color correction sliders
        self.white_balance_scale = tk.Scale(self.frame_controls, from_=50, to=150, label="White Balance", orient="horizontal")
        self.white_balance_scale.set(100)
        self.white_balance_scale.pack(pady=5)
        self.luminance_scale = tk.Scale(self.frame_controls, from_=50, to=150, label="Luminance", orient="horizontal")
        self.luminance_scale.set(100)
        self.luminance_scale.pack(pady=5)
        self.red_scale = tk.Scale(self.frame_controls, from_=50, to=150, label="Red", orient="horizontal")
        self.red_scale.set(100)
        self.red_scale.pack(pady=5)
        self.green_scale = tk.Scale(self.frame_controls, from_=50, to=150, label="Green", orient="horizontal")
        self.green_scale.set(100)
        self.green_scale.pack(pady=5)
        self.blue_scale = tk.Scale(self.frame_controls, from_=50, to=150, label="Blue", orient="horizontal")
        self.blue_scale.set(100)
        self.blue_scale.pack(pady=5)
        self.btn_apply = tk.Button(self.frame_controls, text="Apply", command=self.apply_adjustments)
        self.btn_apply.pack(pady=10)

        # Controls for Spatial
        spatial_label = tk.Label(self.frame_spatial, text="Spatial")
        spatial_label.pack(pady=5)
        self.radius_scale = tk.Scale(self.frame_spatial, from_=10, to=150, label="Radius (px)", orient="horizontal")
        self.radius_scale.set(50)
        self.radius_scale.pack(pady=5)
        self.radius_percent_scale = tk.Scale(self.frame_spatial, from_=10, to=100, label="Radius (%)", orient="horizontal")
        self.radius_percent_scale.set(50)
        self.radius_percent_scale.pack(pady=5)
        self.smooth_scale = tk.Scale(self.frame_spatial, from_=0, to=10, label="Smooth", orient="horizontal")
        self.smooth_scale.set(5)
        self.smooth_scale.pack(pady=5)
        self.btn_apply_radius = tk.Button(self.frame_spatial, text="Apply Radius", command=self.apply_radius)
        self.btn_apply_radius.pack(pady=10)

    def open_image(self):
        # For Mac OS use "*.jpg" filter to open JPEG files
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*jpg")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.resize((600, 450), resample=RESAMPLE_METHOD)
            self.display_image(self.processed_image)
            self.update_waveform(self.processed_image)

    def display_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_canvas.delete("all")
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def update_waveform(self, img):
        np_img = np.array(img)
        height, width, channels = np_img.shape  # expected 450x600x3
        red_avg = np.mean(np_img[:, :, 0], axis=0)
        green_avg = np.mean(np_img[:, :, 1], axis=0)
        blue_avg = np.mean(np_img[:, :, 2], axis=0)
        self.ax.cla()
        self.ax.plot(range(width), red_avg, color='red', label='Red Channel')
        self.ax.plot(range(width), green_avg, color='green', label='Green Channel')
        self.ax.plot(range(width), blue_avg, color='blue', label='Blue Channel')
        self.ax.set_title("RGB Waveform")
        self.ax.set_xlabel("Width (pixels)")
        self.ax.set_ylabel("Brightness")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def apply_adjustments(self):
        if self.original_image:
            wb = self.white_balance_scale.get()
            lum = self.luminance_scale.get() / 100.0
            r_adj = self.red_scale.get() / 100.0
            g_adj = self.green_scale.get() / 100.0
            b_adj = self.blue_scale.get() / 100.0
            factor = (wb - 100) / 100.0
            r_wb = 1 + factor
            b_wb = 1 - factor
            img = self.original_image.resize((600, 450), resample=RESAMPLE_METHOD)
            r, g, b = img.split()
            r = r.point(lambda i: max(0, min(255, int(i * lum * r_adj * r_wb))))
            g = g.point(lambda i: max(0, min(255, int(i * lum * g_adj))))
            b = b.point(lambda i: max(0, min(255, int(i * lum * b_adj * b_wb))))
            self.processed_image = Image.merge("RGB", (r, g, b))
            self.display_image(self.processed_image)
            self.update_waveform(self.processed_image)

    def apply_radius(self):
        if self.processed_image:
            base_radius = self.radius_scale.get()
            percent = self.radius_percent_scale.get() / 100.0
            smooth_val = self.smooth_scale.get()
            final_radius = int(base_radius * percent)
            overlay = Image.new("RGBA", self.processed_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            center_x, center_y = self.processed_image.size[0] // 2, self.processed_image.size[1] // 2
            left = center_x - final_radius
            top = center_y - final_radius
            right = center_x + final_radius
            bottom = center_y + final_radius
            draw.ellipse((left, top, right, bottom), outline=(255, 255, 255, 255), width=5)
            if smooth_val > 0:
                overlay = overlay.filter(ImageFilter.GaussianBlur(radius=smooth_val))
            base = self.processed_image.convert("RGBA")
            combined = Image.alpha_composite(base, overlay)
            self.display_image(combined)

    def adb_connect(self):
        """
        Connects to the device via ADB and launches the camera app.
        """
        try:
            result = subprocess.run(
                ["adb", "shell", "am", "start", "-a", "android.media.action.IMAGE_CAPTURE"],
                capture_output=True, text=True
            )
            if "Error" in result.stderr:
                messagebox.showerror("Error", "Failed to connect to the camera via ADB.")
            else:
                messagebox.showinfo("Success", "Camera successfully launched via ADB.")
        except Exception as e:
            messagebox.showerror("Error", f"Error executing ADB command: {e}")

    def adb_take_image(self):
        """
        Takes a picture using ADB.
        """
        try:
            result = subprocess.run(
                ["adb", "shell", "input", "keyevent", "27"],
                capture_output=True, text=True
            )
            if "Error" in result.stderr:
                messagebox.showerror("Error", "Failed to take a picture via ADB.")
            else:
                messagebox.showinfo("Success", "Image captured via ADB!")
        except Exception as e:
            messagebox.showerror("Error", f"Error executing ADB command: {e}")

    def adb_get_image(self):
        """
        Retrieves file list from /sdcard/DCIM via ADB, finds the latest JPEG,
        downloads it locally, and updates the UI.
        """
        try:
            if not os.path.exists("ImageCapture"):
                os.makedirs("ImageCapture")
            files_txt_path = os.path.join(os.getcwd(), "ImageCapture", "files.txt")
            result = subprocess.run(
                ["adb", "shell", "ls", "-R", "/sdcard/DCIM"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise Exception(result.stderr)
            with open(files_txt_path, "w", encoding="utf-8") as f:
                f.write(result.stdout)
            current_dir = None
            latest_file = None
            with open(files_txt_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.endswith(":"):
                        current_dir = line[:-1]
                    elif line.endswith(".jpg"):
                        if current_dir:
                            full_path = current_dir + "/" + line
                            latest_file = full_path
            if latest_file:
                local_image_path = os.path.join(
                    "ImageCapture",
                    f"captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                )
                pull_result = subprocess.run(
                    ["adb", "pull", latest_file, local_image_path],
                    capture_output=True, text=True
                )
                if pull_result.returncode != 0:
                    raise Exception(pull_result.stderr)
                self.original_image = Image.open(local_image_path)
                self.processed_image = self.original_image.resize((600, 450), resample=RESAMPLE_METHOD)
                self.display_image(self.processed_image)
                self.update_waveform(self.processed_image)
                messagebox.showinfo("Success", "Image successfully downloaded via ADB!")
            else:
                messagebox.showinfo("Info", "No images found in the DCIM folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving image via ADB: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
