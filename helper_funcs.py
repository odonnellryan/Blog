from config import ALLOWED_EXTENSIONS


def return_method_dict(get_object, get_method_array):
    """
    returns a dictionary tied to different methods of an object. useful for building 
     dynamic forms, etc.. lets you
     dynamically access methods of an object.
    """
    tag_values = {}
    for tag in get_method_array:
        form_method = getattr(get_object, tag)
        tag_values[tag] = form_method
    return tag_values


def allowed_file(filename):
    """
    finds the allowed filename and extensions.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS