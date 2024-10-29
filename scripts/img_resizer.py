import PIL.Image
import os

# Get access to Downloads folder
def get_downloads_folder():
    home_dir = os.path.expanduser("D:\\Users\\kayai\\")
    downloads_folder = os.path.join(home_dir, "Downloads")
    return downloads_folder

downloads_folder = get_downloads_folder()

# Get image from downloads folder
def get_image_from_downloads():
    image_path = os.path.join(downloads_folder, "laserbulletblue.png")
    return image_path

image_path = get_image_from_downloads()

try:
    # image resizing
    img = PIL.Image.open(image_path)
    img = img.resize((24, 24))
    print("Resizing image...")
    new_img_name = "laserbulletblue24x24.png"
    img.save(new_img_name)
    print(f"Image succesfully resized and saved as '{new_img_name}'")
except Exception as e:
    print(f"An error occurred: {e}")
    


