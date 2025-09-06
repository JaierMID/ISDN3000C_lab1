import cv2
from PIL import Image
from io import BytesIO
from rich.console import Console

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
    for index, pixel_value in enumerate(grayscale_image.getdata()):
        r, g, b = rgb_data[index]
        char = map_pixel_to_char(pixel_value, ASCII_CHARS)
        # Print the character with its color
        console.print(char, end="", style=f"rgb({r},{g},{b})")
        # Add a newline after every width characters
        if (index + 1) % resized_image.width == 0:
            console.print("")  # Print a newline

def capture_webcam():
    # Initialize OpenCV capture object
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BRG (OpenCV) to RGB (Pillow)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to Pillow Image
            pil_image = Image.fromarray(frame_rgb)

            # Print ASCII art of the current frame
            print_colored_ascii(pil_image, new_width=100)
            
            # Wait a bit for better visualization
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_webcam()