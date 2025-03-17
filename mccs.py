#!/usr/bin/env python3


import argparse

import os

import random


import sys
import re

# Directory where the script resides
PROGRAM_DIR = os.path.dirname(os.path.realpath(__file__))
# Directory containing the ASCII art files (placed in the "colorscripts" folder under the program directory)
COLORSCRIPTS_DIR = os.path.join(PROGRAM_DIR, "colorscripts")


def File2Array(filename):
    with open(filename, "r") as file:
        linecount = 0
        array = []
        for line in file:
            if linecount == 0:
                linecount += 1
                w, h = list(map(int, line.split()))
                continue
            array.append([])
            row = list(map(int, line.split()))
            for i in range(0, len(row), 3):
                array[linecount - 1].append(row[i : i + 3])
            linecount += 1
    return array, w, h


def File2BigAscii(array, width, height, scale=1):
    for y in range(height):
        for sy in range(scale):  # 纵向缩放
            for x in range(width):
                r, g, b = array[y][x]
                if (r, g, b) == (-1, -1, -1):  # 透明像
                    char = "  " * scale  # 透明部分用空格代替
                    sys.stdout.write(f"{char}")
                else:
                    char = "██" * scale  # 横向缩放
                    sys.stdout.write(
                        f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m{char}\033[0m"
                    )
            sys.stdout.write("\n")  # 换行


def get_ansi_color(r, g, b, is_bg=False):
    """返回 ANSI 颜色代码，处理透明颜色"""
    if (r, g, b) == (-1, -1, -1):  # 透明像素
        return ""  # 不添加颜色
    return f"\033[{48 if is_bg else 38};2;{r};{g};{b}m"


def File2SmallAscii(array, width, height):
    new_height = height // 2  # 不补充行，保持数据完整

    for y in range(0, new_height * 2, 2):
        for x in range(width):
            top_color = array[y][x]
            bottom_color = array[y + 1][x] if y + 1 < height else (-1, -1, -1)
            print("\033[0m",end="")  # 重置颜色，仅在行末执行

            if top_color == [-1, -1, -1] and bottom_color == [-1, -1, -1]:
                print(" ", end="")  # 完全透明
            elif top_color == [-1, -1, -1]:
                print(
                    f"{get_ansi_color(*bottom_color, is_bg=True)} ", end=""
                )  # 仅下半部分有颜色
            elif bottom_color == [-1, -1, -1]:
                print(f"{get_ansi_color(*top_color)}▀", end="")  # 仅上半部分有颜色
            else:
                print(
                    f"{get_ansi_color(*bottom_color, is_bg=True)}{get_ansi_color(*top_color)}▀",
                    end="",
                )  # 正常显示
        print("\033[0m")  # 重置颜色，仅在行末执行


def print_ascii(file_path: str, scale: int = 1) -> None:
    try:
        array, width, height = File2Array(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    dpi = width * height
    if scale == 1:
        if dpi <= 15:
            File2BigAscii(array, width, height, scale=2)
        elif dpi <= 143:
            File2BigAscii(array, width, height, scale=1)
        else:
            File2SmallAscii(array, width, height)
    else:
        if dpi <= 143:
            File2BigAscii(array, width, height, scale=scale - 1)
        else:
            File2BigAscii(array, width, height, scale=scale)


def list_ascii_files() -> None:
    """
    List all available ASCII art files (without file extensions) in the colorscripts directory.
    """
    if not os.path.isdir(COLORSCRIPTS_DIR):
        print(f"Directory does not exist: {COLORSCRIPTS_DIR}")
        sys.exit(1)
    files = [
        f
        for f in os.listdir(COLORSCRIPTS_DIR)
        if os.path.isfile(os.path.join(COLORSCRIPTS_DIR, f))
    ]
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
        "-l", "--list", action="store_true", help="List all available ASCII art files"
    )

    parser.add_argument(
        "-s",
        "--scale",
        type=int,
        default=1,
        help="Output scale factor (default is 1, no scaling)",
    )

    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Randomly select an ASCII art file to print",
    )

    parser.add_argument(
        "name",
        nargs="?",
        help="Name of the ASCII art file to print (without extension)",
    )

    args = parser.parse_args()

    if args.list:
        list_ascii_files()

        sys.exit(0)

    if args.random:
        if not os.path.isdir(COLORSCRIPTS_DIR):
            print(f"Directory does not exist: {COLORSCRIPTS_DIR}")

            sys.exit(1)

        files = [
            f
            for f in os.listdir(COLORSCRIPTS_DIR)
            if os.path.isfile(os.path.join(COLORSCRIPTS_DIR, f))
        ]

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
