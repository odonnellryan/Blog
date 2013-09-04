
def return_method_dict(get_object, get_method_array):
    tag_values = {}
    for tag in get_method_array:
            form_method = getattr(get_object, tag)
            tag_values[tag] = form_method
    return tag_values