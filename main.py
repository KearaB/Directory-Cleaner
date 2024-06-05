import os
import shutil
import json
from datetime import datetime
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def load_config(path):
    """
    Load a JSON configuration file from a specified path.

    Args:
        path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary if file is loaded successfully, None otherwise.
    """
    try:
        with open(path, 'r') as config_file:
            return json.load(config_file)
    except json.JSONDecodeError:
        print("Error reading the JSON configuration file.")
        return None
    except FileNotFoundError:
        print("Configuration file not found.")
        return None

class FileHandler(FileSystemEventHandler):
    """
    Custom event handler for file system events that processes files based on their type and modifies their storage location.
    """
    def __init__(self, file_types, downloads_dir):
        """
        Initialize the file handler with specific file types and a target directory.

        Args:
            file_types (dict): Dictionary of file extensions and corresponding target directories.
            downloads_dir (str): Path to the directory to monitor for file changes.
        """
        self.file_types = file_types
        self.downloads_dir = downloads_dir

    def on_created(self, event):
        """
        Event hook for created files.

        Args:
            event: The event object representing file creation.
        """
        self.process_event(event)

    def on_modified(self, event):
        """
        Event hook for modified files.

        Args:
            event: The event object representing file modification.
        """
        self.process_event(event)

    def process_event(self, event):
        """
        Process file creation or modification events by filtering and handling valid files.

        Args:
            event: The event object representing file creation or modification.
        """
        if not event.is_directory and not event.src_path.endswith('.crdownload') and not event.src_path.endswith('.part'):
            self.process_file(event.src_path)

    def process_file(self, path):
        """
        Process and relocate the file to the appropriate directory based on its type and creation date.

        Args:
            path (str): Path to the file to be processed.
        """
        sleep(1)  # Delay to ensure file is not being written to or locked
        file_name = os.path.basename(path)
        file_ext = os.path.splitext(file_name)[1].lower()

        if file_ext in self.file_types:
            today = datetime.now().strftime("%Y-%m-%d")
            dest_folder = os.path.join(self.file_types[file_ext], today)
            dest_path = os.path.join(dest_folder, file_name)

            print(f"File detected: {file_name} ({file_ext})")
            print(f"Destination Folder: {dest_folder}")
            print(f"Destination Path: {dest_path}")

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder, exist_ok=True)

            if os.path.exists(dest_path):
                base_name = os.path.splitext(file_name)[0]
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_name = f"{base_name}_{timestamp}{file_ext}"
                dest_path = os.path.join(dest_folder, new_name)

            try:
                shutil.move(path, dest_path)
                print(f"Successfully moved {file_name} to {dest_path}")
            except Exception as e:
                print(f"Error moving {file_name}: {e}")

def main():
    """
    Main function to initialize the file monitoring system.
    """
    config = load_config('configs/file_paths.json')
    if config:
        file_types = config['file_paths']
        downloads_dir = config['downloads_dir']

        observer = Observer()
        handler = FileHandler(file_types, downloads_dir)
        observer.schedule(handler, downloads_dir, recursive=False)
        observer.start()

        try:
            print("Monitoring downloads directory...")
            while True:
                observer.join(timeout=1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
        print("Stopped monitoring.")

if __name__ == "__main__":
    main()
