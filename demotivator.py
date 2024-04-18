import pathlib
import tempfile
import argparse
import textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ImageClip

# Define constants
IMAGE_WIDTH = 539
IMAGE_HEIGHT = 423
FONT = ImageFont.truetype(str(pathlib.Path(__file__).parent /'ref' / 'Montserrat-ExtraBoldItalic.ttf'), 36)
BACKGROUND_IMAGE = pathlib.Path(__file__).parent /'ref' /'background.jpg'
AUDIO_FILE = pathlib.Path(__file__).parent /'ref' / 'demotivator.mp3'
VIDEO_FILE = pathlib.Path(__file__).parent / 'demotivator.mov'


def start_dialog_with_user():
    """Parses the command-line arguments for the image and the text.

    Returns:
        file_of_image (pathlib.Path): The path to the image file.
        input_text (str): The text to be printed on the image.
    """
    parser = argparse.ArgumentParser(description='Create a demotivator video from an image and a text.')
    parser.add_argument('image', type=pathlib.Path, help='The path to the image file.')
    parser.add_argument('text', type=str, help='The text to be printed on the image.')
    args = parser.parse_args()

    file_of_image = args.image.resolve()
    input_text = args.text

    return file_of_image, input_text

def set_image_in_frame(file_of_image: pathlib.Path, input_text: str) -> pathlib.Path:
    """Resizes the image, pastes it on a background, and prints the text on it.

    Args:
        file_of_image (pathlib.Path): The path to the image file.
        input_text (str): The text to be printed on the image.

    Returns:
        pathlib.Path: The path to the final image file.
    """
    with Image.open(file_of_image) as image:
        resized_image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    with Image.open(BACKGROUND_IMAGE) as final_image:
        final_image.paste(resized_image, (59, 66))

        print_text(final_image, input_text)

        path_for_photo = tempfile.NamedTemporaryFile(suffix='.png').name
        final_image.save(path_for_photo)

    return pathlib.Path(path_for_photo)

def print_text(final_image: Image, text: str):
    """Prints the text on the final image.

    Args:
        final_image (Image): The final image object.
        text (str): The text to be printed on the image.
    """
    draw_image = ImageDraw.Draw(final_image)

    lines = textwrap.wrap(text, 28)
    [draw_image.text(((654 - draw_image.textbbox((0, 0), line, FONT)[2]) // 2, 600 + (i - len(lines) // 2) * 40), line, 'white', FONT) for i, line in enumerate(lines)]

def add_sound_to_photo(file_of_image: pathlib.Path):
    """Adds sound to the final image and saves it as a video file.

    Args:
        file_of_image (pathlib.Path): The path to the final image file.
    """
    image = ImageClip(str(file_of_image))
    audio = AudioFileClip(str(AUDIO_FILE))
    image = image.set_duration(audio.duration)
    image_with_music = image.set_audio(audio)
    image_with_music.write_videofile(str(VIDEO_FILE), fps=24, codec='libx264', logger=None)


if __name__ == "__main__":
    add_sound_to_photo(set_image_in_frame(*start_dialog_with_user()))