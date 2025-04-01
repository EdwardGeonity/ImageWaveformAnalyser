# ImageWaveformAnalyser

# 📷 Image ADB Waveform Analyzer

A desktop utility for analyzing images captured from Android devices via ADB, with real-time waveform visualization and basic color correction tools.

---

## ✨ Features

- 📷 Open and view JPEG images (local or via ADB)
- 📈 Real-time RGB waveform display using Matplotlib
- 🎛 Color adjustment sliders:
  - White Balance
  - Luminance
  - Red, Green, Blue channels
- 🌀 Spatial circle overlay with radius and feather control
- ⚡ One-click ADB integration:
  - Connect to device
  - Trigger camera shutter
  - Pull latest captured image from DCIM folder

---

## 🖼 GUI Overview

- Left panel: image preview (600x450 canvas)
- Right panel: waveform scope (RGB brightness across image width)
- Side panel: color correction sliders
- Bottom panel: spatial overlay controls

---

## 🧰 Requirements

- Python 3.7 or newer
- [Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- `adb` (Android Debug Bridge) in your system path

Install dependencies:

```bash
pip install Pillow numpy matplotlib


🚀 How to Run

python image_waveform_gui.py

To use ADB features:

    Connect your Android device via USB or over Wi-Fi.

    Enable Developer Mode and USB Debugging.

    Make sure adb devices shows your device.

    Use the ADB CONNECT, ADB TAKE IMAGE, and LOAD IMAGE buttons.

📦 Packaging (optional)

You can package this app as .exe (Windows) or .app (macOS) using:

    PyInstaller

    py2app

    See build instructions in the Issues or Wiki (coming soon).

📸 Screenshots

![Screen Shot 2](https://github.com/user-attachments/assets/af884798-69e8-45cb-9399-a8a16ea8fe30)
![Screen Shot 1](https://github.com/user-attachments/assets/5483b8cf-ddcb-4e44-851a-6e268794843c)




🛠 TODO

Save corrected images

Support for PNG and RAW (DNG) formats

Histogram view

    Export waveform data

📄 License

MIT License
