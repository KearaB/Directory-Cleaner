# File Handler Script 📁

## Introduction
This repository contains a Python script designed to handle and organize files automatically based on their extensions. It monitors a specified directory and moves new or modified files to designated folders. Although it's a basic project, it's fun and quite helpful, especially for keeping your downloads organized!

The script was originally created for a Windows machine, but instructions for adapting it to macOS and Linux are included.

## Features
* Monitors a specific directory for new and modified files.
* Automatically moves files based on their extension to predefined folders.
* Configurable through a JSON file to specify file types and destination paths.

## Prerequisites
Before you can run this script, you need to have `Python` installed on your machine. This script is compatible with `Python 3.6` and above. Additionally, you need to install the `watchdog` library, which is used for monitoring file system events.

## Installation
### 1. Clone Repository
```bash
git clone https://github.com/KearaB/Directory-Cleaner.git
cd Directory-Cleaner
```

### 2. Install Required Python Modules
Ensure Python and pip are installed on your system, then run:
```bash
pip install watchdog
```
This command will install the `watchdog` library needed for the script to function.

## Configuration
Edit the `configs/file_paths.json` file to set up your specific file paths and file types. Here's a sample configuration:
```json
{
    "file_paths": {
        ".pdf": "C:\\Users\\x\\Downloads\\documents",
        ".py": "C:\\Users\\x\\Downloads\\scripts"
        // Add more file types and paths as needed
    },
    "downloads_dir": "C:\\Users\\x\\Downloads"
}
```

## Running the script
To run the script on your local device, execute:
```bash
python main.py
```
This will start monitoring the specified downloads directory and automatically organize incoming files into the appropriate folders.

## Adapting for macOS and Linux
The script is written for Windows by default. To adapt it for macOS or Linux:

* Change the file paths in `configs/file_paths.json` to match the Unix-like file system structure, e.g., `/Users/x/Downloads/documents`.
* Modify any path-related code in `main.py` to use Unix-style paths if necessary.

## Contribution
Feel free to fork this project and submit pull requests. You can also open an issue if you find bugs or have feature requests.