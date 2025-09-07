import sys
import argparse
import cv2
from PIL import Image
from rich.console import Console

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

def print_colored_ascii(image, ascii_chars, new_width=100):
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
    for index, pixel_value in enumerate(grayscale_image.getdata()):
        r, g, b = rgb_data[index]
        char = map_pixel_to_char(pixel_value, ascii_chars)
        # Print the character with its color
        console.print(char, end="", style=f"rgb({r},{g},{b})")
        # Add a newline after every width characters
        if (index + 1) % resized_image.width == 0:
            console.print("")  # Print a newline

def process_image_file(image_path, ascii_chars, new_width=100):
    try:
        # Load the image from file
        image = Image.open(image_path)
        print_colored_ascii(image, ascii_chars, new_width)
    except FileNotFoundError:
        print(f"Error: File not found at '{image_path}'")
    except IOError:
        print(f"Error: Cannot open image file '{image_path}'. Please check the file format and permissions.")

def capture_webcam(ascii_chars, new_width=100):
    # Initialize OpenCV capture object
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR (OpenCV) to RGB (Pillow)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to Pillow Image
            pil_image = Image.fromarray(frame_rgb)

            # Print ASCII art of the current frame
            print_colored_ascii(pil_image, ascii_chars, new_width)

            # Check for the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        print("\nWebcam capture stopped. Goodbye!")

def main():
    parser = argparse.ArgumentParser(description="Converts images or webcam feed to ASCII art.")
    parser.add_argument("image_path", nargs='?', default=None, help="Path to the image file.")
    parser.add_argument("--chars", type=int, default=100, help="Width of the ASCII art in characters. Default is 100.")
    parser.add_argument("--ramp", type=str, default="@%#*+=-:. ", help="Custom ASCII character ramp. Default is '@%#*+=-:. '.")

    args = parser.parse_args()

    ascii_ramp = args.ramp if args.ramp else "@%#*+=-:. "

    if args.image_path:
        process_image_file(args.image_path, ascii_ramp, args.chars)
    else:
        capture_webcam(ascii_ramp, args.chars)

if __name__ == "__main__":
    main()