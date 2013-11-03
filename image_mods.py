import db_structure
post = db_structure.Posts
import helper_funcs
import os
import config
import db_mods
from werkzeug.utils import secure_filename


def array_to_comma_list(get_image_array):
    if get_image_array:
        return ",".join(get_image_array)
    else:
        return None

def image_array(post_id):
    query = post.get(post.id == post_id)
    if not query.images:
        return None
    return query.images.split(',')

def update_images(post_id, image_list):
    query = post.update(images=image_list).where(post.id == post_id)
    query.execute()

def delete_images(current_images, images_to_remove):
    """
        gets current images, and images to remove, and returns a list of remaining images
    """
    try:
        for image in images_to_remove:
            current_images.remove(image)
            try:
                os.remove(image.encode()[1:])
            except IOError or WindowsError:
                pass
    except TypeError:
        pass
    return current_images

def remove_images(post_id, images_to_remove):
    """
        images_to_remove is a dictionary. the data is a form value.
    """
    #gets the array of current images
    current_images = image_array(post_id)
    #takes the images_to_remove dict and turns it into a list of images to remove
    remove = db_mods.post_tag_identifier(images_to_remove)
    if remove:
        current_images = delete_images(current_images, remove)
        return update_images(post_id, array_to_comma_list(current_images))


def image_name_tool(get_file, get_path, get_filename):
    """
    Gets a file in a request-post method and renames it if a file with that name exists.
    then returns a string which is that file location
    """
    image_web_path = ""
    image_number = 1
    filename = get_filename
    file_path = get_path
    file_ = get_file
    new_name = filename
    while True:
        try:
            with open(file_path):
                new_path = filename.split(".")
                _file_name = new_path[0]
                extension = new_path[1]
                new_name = "".join((_file_name, "(", str(image_number), ").", extension))
                image_number += 1
                file_path = "".join((config.UPLOAD_FOLDER, new_name))
        except IOError:
            image_web_path = "".join(('/static/', 'uploads/', new_name))
            file_.save(file_path)
            break
    return image_web_path

def call_image_tool_posts(images):
    image_list = []
    for image in images:
        file_ = images[image]
        if file_ and helper_funcs.allowed_file(file_.filename):
            filename = secure_filename(file_.filename).replace(",", "")
            file_path = os.path.join(config.UPLOAD_FOLDER, filename)
            image_list.append(image_name_tool(file_, file_path, filename))
    return image_list

def image_tool_logo(images):
    image_list = []
    for image in images:
        file_ = images[image]
        if file_ and helper_funcs.allowed_file(file_.filename):
            filename = 'logo.jpg'
            file_path = os.path.join('static/imgs/', filename)
            file_.save(file_path)
    return image_list