import sys
import argparse
from rich.console import Console
from PIL import Image

# Define your character ramp
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    """Resize image and maintain aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def map_pixel_to_char(pixel_value, ascii_chars):
    """Convert pixel value to a character."""
    char_index = min(pixel_value * (len(ascii_chars) - 1) // 255, len(ascii_chars) - 1)
    return ascii_chars[char_index]

def print_colored_ascii(image, new_width=100):
    """Resize, convert to grayscale, and print ASCII art with colors based on the image."""
    # Resize the image
    resized_image = resize_image(image, new_width)
    # Convert to grayscale
    grayscale_image = resized_image.convert("L")
    # Get RGB data for colored output
    rgb_data = resized_image.getdata()

    # Initialize Rich Console for styled text output
    console = Console()

    # Build the ASCII string and print with RGB colors
    ascii_str = ""
    for index, pixel_value in enumerate(grayscale_image.getdata()):
        r, g, b = rgb_data[index]
        char = map_pixel_to_char(pixel_value, ASCII_CHARS)
        # Print the character with its color
        console.print(char, end="", style=f"rgb({r},{g},{b})")
        # Add a newline after every width characters
        if (index + 1) % resized_image.width == 0:
            ascii_str += "\n"
            console.print("")

def main():
    parser = argparse.ArgumentParser(description="Converts images to ASCII art with colors.")
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

    # Print the colored ASCII art
    print_colored_ascii(image, args.chars)

if __name__ == "__main__":
    main()