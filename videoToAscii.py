import os
import time
import cv2
import pygame  # For audio playback


# Convert RGB values to an ANSI true-color (24-bit) escape sequence
def rgb_to_ansi(r, g, b, text="█"):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


# Denser ASCII characters for better image representation
ASCII_CHARS = "@%#*+=-:. "


def get_terminal_dimensions():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 100, 30  # Default fallback if terminal size cannot be detected


def process_frame(frame):
    term_width, term_height = 200, 45

    aspect_ratio = frame.shape[0] / frame.shape[1]

    new_height = term_height
    new_width = int(new_height / aspect_ratio * 2.3)

    if new_width > term_width:
        new_width = term_width
        new_height = int(new_width * aspect_ratio / 2.3)

    resized = cv2.resize(frame, (new_width, new_height))

    return resized


def play_colored_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Initialize the Pygame mixer and start audio playback
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(
            video_path
        )  # Extract and play audio from the video file if an audio track exists

        pygame.mixer.music.play()

    except Exception as e:
        print(f"Audio playback failed: {e}")

    # Hide the terminal cursor to reduce flickering
    print("\033[?25l", end="")

    try:
        while cap.isOpened():
            start_time = time.time()

            ret, frame = cap.read()

            if not ret:
                break

            # Resize the frame according to the terminal dimensions
            resized_frame = process_frame(frame)

            height, width, _ = resized_frame.shape

            output_lines = []

            for y in range(height):
                line_str = ""

                for x in range(width):
                    b, g, r = resized_frame[y, x]

                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)

                    char_idx = int(
                        gray / 255 * (len(ASCII_CHARS) - 1)
                    )

                    char = ASCII_CHARS[char_idx]

                    line_str += rgb_to_ansi(r, g, b, char)

                output_lines.append(line_str)

            # Clear the screen and print the entire frame at once
            os.system("cls" if os.name == "nt" else "clear")

            print("\n".join(output_lines), end="")

            # FPS control to maintain approximately 30 FPS
            elapsed = time.time() - start_time

            if elapsed < 0.03:
                time.sleep(0.03 - elapsed)

    finally:
        cap.release()

        # Stop the audio so it does not continue playing in the background
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Show the terminal cursor again
        print("\033[?25h")

        os.system("cls" if os.name == "nt" else "clear")

        print("Playback finished!")


if __name__ == "__main__":
    video_file = input("Enter the Video Path ")

    play_colored_video(video_file)  