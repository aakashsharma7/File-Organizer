import os
import shutil
import argparse
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
import calendar
from pathlib import Path
from collections import defaultdict
import tkinterdnd2 as tkdnd
import humanize

# Try to import magic, if it fails, we'll use extension-based detection only
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("Warning: python-magic-bin not available. Using extension-based detection only.")

class FileOrganizer:
    def __init__(self):
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h']
        }
        
        # Statistics tracking
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'space_freed': 0,
            'files_by_category': defaultdict(int),
            'size_by_category': defaultdict(int)
        }
        
        # Magic number MIME type mappings
        self.mime_types = {
            'image/': 'Images',
            'application/pdf': 'Documents',
            'application/msword': 'Documents',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Documents',
            'application/vnd.ms-excel': 'Documents',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Documents',
            'application/vnd.ms-powerpoint': 'Documents',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'Documents',
            'text/': 'Documents',
            'video/': 'Videos',
            'audio/': 'Audio',
            'application/zip': 'Archives',
            'application/x-rar-compressed': 'Archives',
            'application/x-7z-compressed': 'Archives',
            'application/x-tar': 'Archives',
            'application/gzip': 'Archives',
            'text/x-python': 'Code',
            'text/javascript': 'Code',
            'text/html': 'Code',
            'text/css': 'Code',
            'text/x-java': 'Code',
            'text/x-c++': 'Code',
            'text/x-c': 'Code'
        }

    def reset_stats(self):
        """Reset all statistics to zero."""
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'space_freed': 0,
            'files_by_category': defaultdict(int),
            'size_by_category': defaultdict(int)
        }

    def get_file_size(self, file_path):
        """Get the size of a file in bytes."""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0

    def get_file_category(self, file_path):
        """Determine the category of a file using both extension and magic numbers."""
        # First try magic number detection if available
        if MAGIC_AVAILABLE:
            try:
                mime_type = magic.from_file(file_path, mime=True)
                for mime_prefix, category in self.mime_types.items():
                    if mime_type.startswith(mime_prefix):
                        return category
            except Exception as e:
                print(f"Magic number detection failed: {str(e)}")
        
        # Fallback to extension-based detection
        file_extension = os.path.splitext(file_path)[1].lower()
        for category, extensions in self.file_types.items():
            if file_extension in extensions:
                return category
        return 'Others'

    def get_date_based_path(self, file_path, directory):
        """Get the date-based path for a file."""
        try:
            # Try to get creation time first, fall back to modification time
            timestamp = os.path.getctime(file_path)
            if timestamp is None:
                timestamp = os.path.getmtime(file_path)
            
            date = datetime.fromtimestamp(timestamp)
            year = str(date.year)
            month = calendar.month_name[date.month]
            
            return os.path.join(directory, year, month)
        except Exception as e:
            print(f"Error getting date-based path: {str(e)}")
            return directory

    def organize_files(self, source_dir, date_based=False):
        """Organize files into appropriate folders based on their extensions or dates."""
        # Reset statistics before starting
        self.reset_stats()
        
        # First, collect all files and their categories
        files_by_category = defaultdict(list)
        
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            
            # Skip if it's a directory
            if os.path.isdir(file_path):
                continue
            
            try:
                if date_based:
                    destination_dir = self.get_date_based_path(file_path, source_dir)
                    files_by_category[destination_dir].append((file_path, filename))
                else:
                    category = self.get_file_category(file_path)
                    destination_dir = os.path.join(source_dir, category)
                    files_by_category[destination_dir].append((file_path, filename))
                    
                    # Update statistics
                    file_size = self.get_file_size(file_path)
                    self.stats['total_files'] += 1
                    self.stats['total_size'] += file_size
                    self.stats['files_by_category'][category] += 1
                    self.stats['size_by_category'][category] += file_size
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        
        # Only create folders and move files if there are files for that category
        for destination_dir, files in files_by_category.items():
            if files:  # Only create folder if there are files to move
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                
                for file_path, filename in files:
                    try:
                        destination = os.path.join(destination_dir, filename)
                        # Calculate space that will be freed (if file is being moved to a different drive)
                        source_drive = os.path.splitdrive(file_path)[0]
                        dest_drive = os.path.splitdrive(destination)[0]
                        if source_drive != dest_drive:
                            self.stats['space_freed'] += self.get_file_size(file_path)
                        
                        shutil.move(file_path, destination)
                    except Exception as e:
                        print(f"Error moving {filename}: {str(e)}")

class FileHandler(FileSystemEventHandler):
    def __init__(self, organizer, source_dir, date_based=False):
        self.organizer = organizer
        self.source_dir = source_dir
        self.date_based = date_based
        self.last_modified = {}  # Track last modified times to prevent duplicate processing

    def on_created(self, event):
        if not event.is_directory:
            # Add a small delay to ensure file is completely written
            time.sleep(1)
            self.organizer.organize_files(self.source_dir, self.date_based)

    def on_modified(self, event):
        if not event.is_directory:
            # Check if we've already processed this file recently
            current_time = time.time()
            if event.src_path in self.last_modified:
                if current_time - self.last_modified[event.src_path] < 1:  # 1 second threshold
                    return
            self.last_modified[event.src_path] = current_time
            self.organizer.organize_files(self.source_dir, self.date_based)

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x700")
        
        # Initialize theme
        self.style = ttk.Style()
        self.is_dark_mode = tk.BooleanVar(value=False)
        self.apply_theme()
        
        self.organizer = FileOrganizer()
        self.source_dir = None
        self.observer = None
        self.monitoring = False
        self.date_based = tk.BooleanVar(value=False)
        
        # Configure drag and drop
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        
        self.setup_gui()
        
        # Show warning if magic is not available
        if not MAGIC_AVAILABLE:
            self.log_message("Warning: python-magic-bin not available. Using extension-based detection only.")
            messagebox.showwarning(
                "Limited Functionality",
                "python-magic-bin is not available. File type detection will be based on extensions only.\n"
                "To enable magic number detection, please install python-magic-bin:\n"
                "pip install python-magic-bin"
            )

    def apply_theme(self):
        """Apply the current theme (light/dark) to the application."""
        if self.is_dark_mode.get():
            # Dark theme colors
            self.style.configure(".", 
                background="#2b2b2b",
                foreground="#ffffff",
                fieldbackground="#3c3f41",
                troughcolor="#3c3f41",
                selectbackground="#4b6eaf",
                selectforeground="#ffffff"
            )
            self.style.configure("TFrame", background="#2b2b2b")
            self.style.configure("TLabel", background="#2b2b2b", foreground="#ffffff")
            self.style.configure("TButton", 
                background="#3c3f41",
                foreground="#ffffff",
                padding=5
            )
            self.style.configure("TCheckbutton", 
                background="#2b2b2b",
                foreground="#ffffff"
            )
            self.style.configure("TLabelframe", 
                background="#2b2b2b",
                foreground="#ffffff"
            )
            self.style.configure("TLabelframe.Label", 
                background="#2b2b2b",
                foreground="#ffffff"
            )
            self.root.configure(bg="#2b2b2b")
        else:
            # Light theme colors
            self.style.configure(".", 
                background="#f0f0f0",
                foreground="#000000",
                fieldbackground="#ffffff",
                troughcolor="#e0e0e0",
                selectbackground="#0078d7",
                selectforeground="#ffffff"
            )
            self.style.configure("TFrame", background="#f0f0f0")
            self.style.configure("TLabel", background="#f0f0f0", foreground="#000000")
            self.style.configure("TButton", 
                background="#e0e0e0",
                foreground="#000000",
                padding=5
            )
            self.style.configure("TCheckbutton", 
                background="#f0f0f0",
                foreground="#000000"
            )
            self.style.configure("TLabelframe", 
                background="#f0f0f0",
                foreground="#000000"
            )
            self.style.configure("TLabelframe.Label", 
                background="#f0f0f0",
                foreground="#000000"
            )
            self.root.configure(bg="#f0f0f0")

    def log_message(self, message):
        """Add a message to the log panel with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_panel.configure(state='normal')
        self.log_panel.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_panel.see(tk.END)
        self.log_panel.configure(state='disabled')

    def update_dashboard(self):
        """Update the dashboard with current statistics."""
        stats = self.organizer.stats
        
        # Update total files
        self.total_files_var.set(f"{stats['total_files']:,}")
        
        # Update total size
        self.total_size_var.set(humanize.naturalsize(stats['total_size']))
        
        # Update space freed
        self.space_freed_var.set(humanize.naturalsize(stats['space_freed']))
        
        # Update category breakdown
        self.category_tree.delete(*self.category_tree.get_children())
        for category, count in stats['files_by_category'].items():
            size = humanize.naturalsize(stats['size_by_category'][category])
            self.category_tree.insert('', 'end', values=(category, count, size))

    def handle_drop(self, event):
        """Handle files/folders dropped onto the window."""
        path = event.data
        # Remove curly braces if present (Windows path format)
        path = path.strip('{}')
        if os.path.isdir(path):
            self.source_dir = path
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)
            self.log_message(f"Directory selected: {path}")
        else:
            self.log_message(f"Error: {path} is not a directory")

    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Left panel (controls)
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Source directory selection
        source_frame = ttk.LabelFrame(left_panel, text="Source Directory", padding="10")
        source_frame.pack(fill="x", pady=5)
        
        self.source_entry = ttk.Entry(source_frame)
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(source_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side="right")
        
        # Organization options
        options_frame = ttk.LabelFrame(left_panel, text="Organization Options", padding="10")
        options_frame.pack(fill="x", pady=5)
        
        date_based_check = ttk.Checkbutton(
            options_frame, 
            text="Date-based organization (Year/Month)", 
            variable=self.date_based
        )
        date_based_check.pack(anchor="w", pady=5)
        
        theme_check = ttk.Checkbutton(
            options_frame,
            text="Dark Mode",
            variable=self.is_dark_mode,
            command=self.apply_theme
        )
        theme_check.pack(anchor="w", pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(left_panel, padding="10")
        action_frame.pack(fill="x", pady=5)
        
        organize_btn = ttk.Button(action_frame, text="Organize Files", command=self.organize_files)
        organize_btn.pack(side="left", padx=5)
        
        self.monitor_btn = ttk.Button(action_frame, text="Start Monitoring", command=self.toggle_monitoring)
        self.monitor_btn.pack(side="left", padx=5)
        
        # Dashboard
        dashboard_frame = ttk.LabelFrame(left_panel, text="📊 Dashboard", padding="10")
        dashboard_frame.pack(fill="x", pady=5)
        
        # Statistics
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(fill="x", pady=5)
        
        # Total files
        ttk.Label(stats_frame, text="Total Files:").grid(row=0, column=0, sticky="w", padx=5)
        self.total_files_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.total_files_var).grid(row=0, column=1, sticky="w", padx=5)
        
        # Total size
        ttk.Label(stats_frame, text="Total Size:").grid(row=1, column=0, sticky="w", padx=5)
        self.total_size_var = tk.StringVar(value="0 B")
        ttk.Label(stats_frame, textvariable=self.total_size_var).grid(row=1, column=1, sticky="w", padx=5)
        
        # Space freed
        ttk.Label(stats_frame, text="Space Freed:").grid(row=2, column=0, sticky="w", padx=5)
        self.space_freed_var = tk.StringVar(value="0 B")
        ttk.Label(stats_frame, textvariable=self.space_freed_var).grid(row=2, column=1, sticky="w", padx=5)
        
        # Category breakdown
        category_frame = ttk.LabelFrame(dashboard_frame, text="Category Breakdown", padding="5")
        category_frame.pack(fill="both", expand=True, pady=5)
        
        # Create Treeview for category breakdown
        self.category_tree = ttk.Treeview(category_frame, columns=("Category", "Files", "Size"), show="headings", height=5)
        self.category_tree.heading("Category", text="Category")
        self.category_tree.heading("Files", text="Files")
        self.category_tree.heading("Size", text="Size")
        self.category_tree.column("Category", width=100)
        self.category_tree.column("Files", width=50)
        self.category_tree.column("Size", width=100)
        self.category_tree.pack(fill="both", expand=True)
        
        # Status log panel
        log_frame = ttk.LabelFrame(left_panel, text="Status Log", padding="10")
        log_frame.pack(fill="both", expand=True, pady=5)
        
        self.log_panel = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=40,
            height=10,
            state='disabled'
        )
        self.log_panel.pack(fill="both", expand=True)
        
        # Initial log message
        self.log_message("Application started. Drag and drop a folder or use the Browse button to begin.")
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir = directory
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, directory)
            self.log_message(f"Directory selected: {directory}")
            
    def organize_files(self):
        if not self.source_dir:
            self.log_message("Error: Please select a source directory")
            return
            
        try:
            self.log_message("Starting file organization...")
            self.organizer.organize_files(self.source_dir, self.date_based.get())
            self.update_dashboard()
            self.log_message("Files organized successfully!")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_message(error_msg)
            
    def toggle_monitoring(self):
        if not self.source_dir:
            self.log_message("Error: Please select a source directory")
            return
            
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        self.observer = Observer()
        event_handler = FileHandler(self.organizer, self.source_dir, self.date_based.get())
        self.observer.schedule(event_handler, self.source_dir, recursive=False)
        self.observer.start()
        self.monitoring = True
        self.monitor_btn.config(text="Stop Monitoring")
        self.log_message("Folder monitoring started")
        
    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.monitoring = False
            self.monitor_btn.config(text="Start Monitoring")
            self.log_message("Folder monitoring stopped")

def main():
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("--source", help="Source directory to organize")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", help="Operation mode")
    parser.add_argument("--date-based", action="store_true", help="Organize files by date (Year/Month)")
    args = parser.parse_args()
    
    if args.mode == "cli":
        if not args.source:
            print("Please provide a source directory using --source")
            return
            
        organizer = FileOrganizer()
        organizer.organize_files(args.source, args.date_based)
        print("Files organized successfully!")
    else:
        root = tkdnd.Tk()
        app = FileOrganizerGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main() 