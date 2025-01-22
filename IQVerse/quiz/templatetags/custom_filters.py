from django import template

register = template.Library()

@register.filter
def add_class(field, class_name):
    """
    Adds a CSS class to the form field widget.
    """
    # Check if the field has a widget and attrs attribute
    if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
        # If the widget already has a class attribute, append the new class
        existing_classes = field.widget.attrs.get('class', '')
        if existing_classes:
            field.widget.attrs['class'] = f'{existing_classes} {class_name}'
        else:
            field.widget.attrs['class'] = class_name
    return field

@register.filter
def capitalize_words(value):
    """Capitalizes the first letter of each word in the string."""
    if isinstance(value, str):
        return ' '.join([word.capitalize() for word in value.split()])
    return value

@register.filter
def get(dictionary, key):
    """Retrieve the value of a key in a dictionary."""
    return dictionary.get(key, None)  # Returns None if the key doesn't exist
