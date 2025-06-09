# 🗂️ File Organizer

A powerful Python-based utility that automatically sorts your files into organized folders! 🚀

## ✨ Features

### 📁 Smart File Organization
- Automatically sorts files by type (images, documents, videos, etc.)
- Date-based organization (Year/Month structure)
- Magic number detection for accurate file type identification
- Creates folders only when needed (no empty folders)

### 🎨 Modern User Interface
- Clean and intuitive GUI
- Dark mode support 🌙
- Drag and drop functionality
- Real-time status logging
- Progress tracking
- Statistics dashboard 📊

### 🔄 Real-Time Monitoring
- Watch folders for new files
- Automatic organization of new files
- Start/stop monitoring with one click
- Background processing

### 🛠️ Technical Features
- Both CLI and GUI modes
- Cross-platform compatibility
- Standalone executable support
- Customizable organization rules

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# GUI Mode
python file_organizer.py

# CLI Mode
python file_organizer.py --mode cli --source /path/to/directory
```

## 💻 Usage

### GUI Mode
1. Launch the application
2. Select a directory using the Browse button or drag and drop
3. Choose organization options:
   - Toggle date-based organization
   - Enable/disable dark mode
4. Click "Organize Files" to start
5. Use "Start Monitoring" to watch for new files

### CLI Mode
```bash
# Basic usage
python file_organizer.py --mode cli --source /path/to/directory

# With date-based organization
python file_organizer.py --mode cli --source /path/to/directory --date-based
```

## 🏗️ Building Executable

### Creating the Executable
1. Make sure you have PyInstaller installed:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
# Basic build
pyinstaller --onefile file_organizer.py

# Build with icon (optional)
pyinstaller --onefile --icon=path/to/icon.ico file_organizer.py
```

The executable will be created in the `dist` directory.

### Using the Executable
1. Navigate to the `dist` directory
2. Run the executable:
   - Windows: Double-click `file_organizer.exe`
   - Linux/Mac: `./file_organizer`

### Executable Features
- 🚀 Standalone application (no Python installation required)
- 📦 All dependencies included
- 🔄 Full functionality of the Python version
- 💻 Works on any compatible system

### Executable Usage
```bash
# GUI Mode (default)
file_organizer.exe

# CLI Mode
file_organizer.exe --mode cli --source /path/to/directory

# With date-based organization
file_organizer.exe --mode cli --source /path/to/directory --date-based
```

### Distribution
- Share the executable with others
- No need to install Python or dependencies
- Works on systems without Python installed
- Single file distribution

## 📋 Requirements
- Python 3.6+ (for development)
- Required packages (automatically installed):
  - watchdog
  - python-magic-bin
  - tkinterdnd2
  - pyinstaller
  - humanize

## 🎯 Supported File Types

### 📸 Images
- JPG, JPEG, PNG, GIF, BMP, SVG

### 📄 Documents
- PDF, DOC, DOCX, TXT
- XLSX, XLS
- PPT, PPTX

### 🎥 Videos
- MP4, AVI, MKV, MOV, WMV

### 🎵 Audio
- MP3, WAV, FLAC, M4A

### 📦 Archives
- ZIP, RAR, 7Z, TAR, GZ

### 💻 Code
- PY, JS, HTML, CSS
- JAVA, CPP, C, H

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⭐ Show Your Support
Give a ⭐️ if this project helped you!

## 🐛 Known Issues
- None at the moment! Report any issues you find.

## 🔮 Future Plans
- [ ] Custom organization rules
- [ ] File preview
- [ ] Batch processing
- [ ] Cloud storage integration
- [ ] More file type support

---
Made with ❤️ by [Your Name]