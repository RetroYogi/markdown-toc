
    
import os
import argparse
import mimetypes
import fnmatch

def is_text_file(file_path, extra_extension):
    """ Check if a file is a text file or has the extra extension. """
    text_extensions = [
        '.txt', '.csv', '.html', '.css', '.js', '.json', '.xml', '.log',
        '.md', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.sh', '.sql',
        '.php', '.c', '.cpp', '.h', '.hpp', '.java', '.py', '.rb', '.pl',
        '.lua', '.perl', '.bat', '.ps1', '.r', '.scala', '.swift', '.vb',
        '.ts', '.jsx', '.tsx', '.scss', '.sass', '.less', '.coffee',
        '.ejs', '.handlebars', '.pug', '.tmpl', '.tmpl'
    ]
    if extra_extension and not extra_extension.startswith('.'):
        extra_extension = '.' + extra_extension
    _, ext = os.path.splitext(file_path)
    return ext.lower() in text_extensions or ext.lower() == extra_extension

def is_excluded(root_path, current_path, exclude_patterns):
    """ Check if a file or directory should be excluded based on the patterns. """
    # Calculate relative path
    relative_path = os.path.relpath(current_path, root_path)
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
    return False

def process_directory(dir_path, root_path, depth=0, extra_extension=None, exclude_patterns=[]):
    """ Recursively process directories and files to create the TOC. """
    toc = []
    for item in sorted(os.listdir(dir_path)):
        full_path = os.path.join(dir_path, item)
        if is_excluded(root_path, full_path, exclude_patterns):
            continue
        if os.path.isdir(full_path):
            toc.append("#" * (depth + 1) + " " + item)
            toc.extend(process_directory(full_path, depth + 1, extra_extension, exclude_patterns))
        elif os.path.isfile(full_path):
            mime_type = mimetypes.guess_type(full_path)[0] or 'unknown'
            if is_text_file(full_path, extra_extension):
                toc.append("- " + item)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                    toc.extend(["    " + line.strip() for line in file.readlines()])
            else:
                toc.append("- " + item)
                toc.append("    (MIME type: " + mime_type + ")")
    return toc

def main(input_path, output_file, extra_extension, exclude_patterns):
    """ Generate the Markdown TOC and save it to a file. """
    if extra_extension and any(fnmatch.fnmatch(extra_extension, pattern) for pattern in exclude_patterns):
        print(f"Error: Conflict between inclusion of extension '{extra_extension}' and exclusion patterns {exclude_patterns}")
        return

    toc = process_directory(input_path, input_path, extra_extension=extra_extension, exclude_patterns=exclude_patterns)
    md_content = "\n".join(toc)


    if not output_file.endswith('.md'):
        output_file += '.md'

    if os.path.exists(output_file):
        overwrite = input(f"The file {output_file} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled.")
            return

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(md_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a Markdown TOC for a directory.',
        epilog="""
        Most known extensions for files with raw text content are included automatically in the
        generated Markdown TOC.

        Example Usages:

          1. Generate a TOC for a directory, force including .xyz files:
             python script.py -i /path/to/directory -o output_filename -ext xyz

          2. Generate a TOC, force excluding all .log files and everything in the 'temp' directory:
             python script.py -i /path/to/directory -o output_filename -x "*.log" "temp/*"

          3. Generate a TOC for a directory, treating .py files as text and excluding .git folders:
             python script.py -i /path/to/directory -o output_filename -ext py -x ".git"

        Parameters:
          -i, --input    Path to the input directory to process.
          -o, --output   Output file name for the Markdown TOC (without .md extension).
          -ext, --extension   Treat files with this extension as text files for inclusion in the TOC.
          -x, --exclude  Exclude files/folders matching these patterns (supports wildcards).

        The script creates a Markdown formatted table of contents for the specified directory.
        It includes the names of all directories and readable text files, and their content.
        Use '-x' to exclude specific files or directories.
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Path to the input directory to process.')
    parser.add_argument('-o', '--output', required=True, help='Output file name (without .md extension).')
    parser.add_argument('-ext', '--extension', help='Treat files with this extension as text files.')
    parser.add_argument('-x', '--exclude', nargs='*', default=[], help='List of files/folders to exclude (supports wildcards).')

    args = parser.parse_args()

    # Display help text if no arguments are provided
    if len(vars(args)) == 0:
        parser.print_help()
    else:
        main(args.input, args.output, args.extension, args.exclude)
