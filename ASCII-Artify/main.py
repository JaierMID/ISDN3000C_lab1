import sys
import argparse
from PIL import Image

# Define your character ramp
ASCII_CHARS = "@%#*+=-:. "

def resize_and_grayscale(image, new_width=100):
    """Resize and convert image to grayscale."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    grayscale_image = resized_image.convert("L")
    return grayscale_image

def map_pixel_to_char(pixel_value, ascii_chars):
    """Convert pixel value to a character."""
    char_index = min(pixel_value * (len(ascii_chars) - 1) // 255, len(ascii_chars) - 1)
    return ascii_chars[char_index]

def main():
    parser = argparse.ArgumentParser(description="Converts images to ASCII art.")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("--chars", type=int, default=100, help="Width of the ASCII art in characters. Default is 100.")

    args = parser.parse_args()

    try:
        image = Image.open(args.image_path)
    except FileNotFoundError:
        print(f"Error: File not found at '{args.image_path}'")
        return
    except IOError:
        print(f"Error: Cannot open image file '{args.image_path}'. Please check the file format and permissions.")
        return

    # 1. Resize and convert the image
    grayscale_image = resize_and_grayscale(image, args.chars)

    # 2. Get the pixel data
    pixels = grayscale_image.getdata()

    # 3. Build the ASCII string
    ascii_str = ''.join(map(lambda pixel_value: map_pixel_to_char(pixel_value, ASCII_CHARS), pixels))
    image_width = grayscale_image.width
    ascii_img = '\n'.join(ascii_str[i:i+image_width] for i in range(0, len(ascii_str), image_width))

    # 4. Print the final ASCII art
    print(ascii_img)

if __name__ == "__main__":
    main()