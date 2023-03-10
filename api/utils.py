from PIL.Image import Image

def make_thumbnail(image: Image, height: int):
    image.thumbnail((image.width, height))
