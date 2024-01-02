# Markdown TOC Generator

## About
The Markdown TOC Generator is a Python script that automatically creates a Markdown-formatted table of contents (TOC) for any given directory. It's designed to process directories recursively, listing all directories and text files along with their contents in a structured Markdown file.

## Features
- Recursively processes directories and files to create a detailed TOC.
- Supports a wide range of text file extensions, including code files.
- Option to include files with any chosen extension in the TOC.
- Ability to exclude specific files or directories using patterns.
- Generates a Markdown file (.md) with the complete structure and contents of the specified directory.

## Installation
No special installation is required. Ensure you have Python installed on your system.

## Usage
The script is executed from the command line, with several options available to customize its behavior:

### Basic Command Structure
```bash
python script.py -i <input_directory_path> -o <output_file_name>
```

### Parameters
- `-i`, `--input`: Path to the input directory to process.
- `-o`, `--output`: Output file name for the Markdown TOC (without the .md extension).
- `-ext`, `--extension`: (Optional) Treat files with this extension as text files for inclusion in the TOC.
- `-x`, `--exclude`: (Optional) Exclude files/folders matching these patterns (supports wildcards).

### Examples
1. **Basic TOC Generation**
   ```bash
   python markdown-toc.py -i /path/to/directory -o output_filename
   ```
   This will generate a TOC for all text files in the specified directory.

2. **Including Specific File Extensions**
   ```bash
   python markdown-toc.py -i /path/to/directory -o output_filename -ext .xyz
   ```
   This will include `.xyz` files as text in the TOC.

3. **Excluding Specific Files and Directories**
   ```bash
   python markdown-toc.py -i /path/to/directory -o output_filename -x "*.log" "temp/*"
   ```
   This will exclude all `.log` files and everything in the `temp` directory.

4. **Combining Inclusion and Exclusion**
   ```bash
   python markdown-toc.py -i /path/to/directory -o output_filename -ext .py -x ".git"
   ```
   This will treat `.py` files as text and exclude `.git` folders.

## Output
The output is a Markdown file containing the TOC. Directories are indicated with "#" based on their depth, and files are listed with their contents (for text files).

## Contribution
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/RetroYogi/markdown-toc/issues) if you want to contribute.

## License
to-do
---

**Note:** This script is highly customizable to suit various needs for directory content visualization. Great for documentation or managing file structures in projects.
