import concurrent.futures
from PIL import ImageGrab, Image

from utils import IMAGE_SIZE

import time

def get_screen_sub(location):
    return ImageGrab.grab(bbox=(location.left, location.top, location.left + location.width, location.top + location.height))

def get_screen(location, num_threads=4):
    # Divide the location into smaller parts
    sub_locations = divide_location(location, num_threads)

    # Use ThreadPoolExecutor to parallelize the screen grabbing
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        screenshots = list(executor.map(get_screen_sub, sub_locations))

    # Recombine the screenshots
    combined_screenshot = combine_screenshots(screenshots)

    # Downscale the image
    combined_screenshot = combined_screenshot.resize((IMAGE_SIZE, IMAGE_SIZE))
    
    return combined_screenshot

def divide_location(location, num_parts):
    # Divide the location into num_parts smaller locations
    sub_locations = []
    part_width = location.width // num_parts

    for i in range(num_parts):
        left = location.left + i * part_width
        right = left + part_width if i < num_parts - 1 else location.left + location.width
        sub_location = Location(left, location.top, right - left, location.height)
        sub_locations.append(sub_location)

    return sub_locations

def combine_screenshots(screenshots):
    # Combine the screenshots into a single image
    combined_image = Image.new('RGB', (sum(screen.width for screen in screenshots), screenshots[0].height))

    offset = 0
    for screenshot in screenshots:
        combined_image.paste(screenshot, (offset, 0))
        offset += screenshot.width

    return combined_image

# Assuming you have a Location class defined
class Location:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

# Example usage
start_time = time.time()
for i in range(100):
    location = Location(left=0, top=0, width=800, height=600)
    screenshot = get_screen(location, num_threads=16)

screenshot.show()
# Record end time
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")