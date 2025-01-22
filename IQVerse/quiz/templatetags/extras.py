from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    """Get a value from a dictionary safely."""
    return dictionary.get(key)
