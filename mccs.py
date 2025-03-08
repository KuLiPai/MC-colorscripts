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



def File2Array(filename):
    with open(filename, 'r') as file:
        linecount = 0
        array = []
        for line in file:
            # Skip the first row
            if linecount == 0:
                linecount += 1
                w,h = list(map(int, line.split()))
                continue
            array.append([])
            row = list(map(int, line.split()))
            for i in range(0,len(row),3):
                array[linecount-1].append(row[i:i+3])
            linecount += 1
    return array, w, h



def File2BigAscii(array, width, height, scale=1):
    #array, width, height = File2Array(filename)
    for y in range(height):
        for sy in range(scale):  # 纵向缩放
            for x in range(width):
                r, g, b = array[y][x]
                char = "██" * scale  # 横向缩放
                sys.stdout.write(f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m{char}\033[0m")
                # 写到文件a.txt
                
            sys.stdout.write("\n")  # 打印换行
            

def get_ansi_color(r, g, b):
    """返回ANSI 256色代码"""
    return f"\033[38;2;{r};{g};{b}m"

def File2SmallAscii(array, width, height):
    #array, width, height = File2Array(filename)
    if height % 2 == 1:
        height += 1
        array.append([])  # 补充一行黑色底色
        for x in range(width):
            array[-1].append([0, 0, 0])  # 补充一行黑色底色
    

    # 计算新高度（缩小一半）
    aspect_ratio =height / width
    new_height = int((width * aspect_ratio) // 2)
       # 调整图像大小
    
    for y in range(0, new_height * 2, 2):  # 每次跳过两行
        for x in range(width):
            top_color = r, g, b = array[y][x]
  # 读取上半部分颜色
            bottom_color = r, g, b = array[y+1][x] if y + 1 < new_height * 2 else (0, 0, 0)  # 读取下半部分颜色
            
            top_ansi = get_ansi_color(*top_color)   # 设置上半部分前景色
            bottom_ansi = get_ansi_color(*bottom_color).replace('38', '48')  # 设置下半部分背景色（ANSI 48 是背景色）
            
            print(f"{bottom_ansi}{top_ansi}▀", end="")  # 使用 ▀ 符号，前景色是上半部分，背景色是下半部分
        print("\033[0m")  # 重置颜色



def print_ascii(file_path: str, scale: int = 1) -> None:
    try:
        array, width, height = File2Array(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    dpi = width * height
    if scale == 1:
        if dpi <=  15:
            File2BigAscii(array, width, height, scale=2)
        elif dpi <= 143:
            File2BigAscii(array, width, height, scale=1)
        else:
            File2SmallAscii(array, width, height)
    else:
        if dpi <= 143:
            File2BigAscii(array, width, height, scale=scale-1)
        else:
            File2BigAscii(array, width, height, scale=scale)
    




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
