import db_mods
import blog_mods
import forms
from flask import request
from wtforms import BooleanField

def return_updated_form_values(form, tag_values, post_tags, post_id):
    page_content = db_mods.get_post_content(post_id)
    form.post_title.data = page_content['title']
    form.post_body.data = page_content['body']
    current_tags = page_content['tags']
    if post_tags and current_tags:
        for tag in current_tags:
            if tag in tag_values:
                tag_values[tag].data = 'y'
    page_content['body_html'] = blog_mods.get_html_content(page_content['body'])

    return form, tag_values, page_content

def image_list_change(uploaded_images=None, current_images=None):
    image_list = []
    if uploaded_images:
        image_list.append(uploaded_images)
    if current_images:
        image_list.append(current_images)
    return image_list

def dynamic_form(image_array, post_tags):
    #some stuff to make sure the correct tags are highlighted, etc.. dynamic form generation blah blah blah
    # class inside a function? hmm.
    class NewPostTags(forms.NewPost):
                pass
    if post_tags:
        for name in post_tags:
            setattr(NewPostTags, name, BooleanField(name))
    if image_array:
        for im_name in image_array:
            setattr(NewPostTags, im_name, BooleanField(""))
    form = NewPostTags(request.form)
    return form