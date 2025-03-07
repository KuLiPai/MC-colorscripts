#!/usr/bin/env python3
import argparse
import os
import random
import re
import sys

# Directory where the script resides
PROGRAM_DIR = os.path.dirname(os.path.realpath(__file__))
# Directory containing the ASCII art files (placed in the "colorscripts" folder under the program directory)
COLORSCRIPTS_DIR = os.path.join(PROGRAM_DIR, "colorscripts")

def print_ascii(file_path: str, scale: int = 1) -> None:
    """
    Read the ASCII art file and print its content, scaling the output by the given factor.
    The scaling works by repeating each ANSI-colored "pixel cell" horizontally and duplicating each line vertically.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    # If no scaling is needed, output the original content
    if scale == 1:
        print("".join(lines))
        return

    scaled_lines = []
    for line in lines:
        line = line.rstrip("\n")
        # Use regex to match ANSI escape-coded "pixel cells"
        pixel_cells = re.findall(r'(\033\[[0-9;]+m.*?\033\[0m)', line)
        if pixel_cells:
            # Repeat each cell horizontally by the scale factor
            scaled_line = "".join(cell * scale for cell in pixel_cells)
        else:
            # Fallback: repeat each character if no ANSI sequences found
            scaled_line = "".join(ch * scale for ch in line)
        # Repeat the entire line vertically by the scale factor
        for _ in range(scale):
            scaled_lines.append(scaled_line)
    print("\n".join(scaled_lines))


def list_ascii_files() -> None:
    """
    List all available ASCII art files (without file extensions) in the colorscripts directory.
    """
    if not os.path.isdir(COLORSCRIPTS_DIR):
        print(f"Directory does not exist: {COLORSCRIPTS_DIR}")
        sys.exit(1)
    files = [f for f in os.listdir(COLORSCRIPTS_DIR)
             if os.path.isfile(os.path.join(COLORSCRIPTS_DIR, f))]
    if not files:
        print("No ASCII art files found.")
        return
    print("Available ASCII art files:")
    for filename in files:
        # Remove file extension for display purposes
        name, _ = os.path.splitext(filename)
        print(name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="mccs: A CLI tool to print ASCII art stored in the colorscripts folder",
        epilog="Examples:\n  mccs --scale 2 charmander\n  mccs --random --scale 3",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="List all available ASCII art files"
    )
    parser.add_argument(
        "-s", "--scale", type=int, default=1,
        help="Output scale factor (default is 1, no scaling)"
    )
    parser.add_argument(
        "-r", "--random", action="store_true",
        help="Randomly select an ASCII art file to print"
    )
    parser.add_argument(
        "name", nargs="?",
        help="Name of the ASCII art file to print (without extension)"
    )

    args = parser.parse_args()

    if args.list:
        list_ascii_files()
        sys.exit(0)

    if args.random:
        if not os.path.isdir(COLORSCRIPTS_DIR):
            print(f"Directory does not exist: {COLORSCRIPTS_DIR}")
            sys.exit(1)
        files = [f for f in os.listdir(COLORSCRIPTS_DIR)
                 if os.path.isfile(os.path.join(COLORSCRIPTS_DIR, f))]
        if not files:
            print("No ASCII art files found.")
            sys.exit(1)
        file_choice = random.choice(files)
    elif args.name:
        file_choice = args.name
        file_path = os.path.join(COLORSCRIPTS_DIR, file_choice)
        if not os.path.isfile(file_path):
            # Try adding a .txt extension if not found
            file_choice += ".txt"
            file_path = os.path.join(COLORSCRIPTS_DIR, file_choice)
            if not os.path.isfile(file_path):
                print(f"ASCII art file named '{args.name}' not found.")
                sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)

    full_path = os.path.join(COLORSCRIPTS_DIR, file_choice)
    print_ascii(full_path, scale=args.scale)


if __name__ == "__main__":
    main()
