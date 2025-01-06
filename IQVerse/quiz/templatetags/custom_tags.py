# templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def map_attribute(queryset, attr_name):
    """
    Extracts an attribute from each item in a queryset or list.
    Usage: queryset|map_attribute:"attribute_name"
    """
    try:
        return [getattr(item, attr_name, None) for item in queryset]
    except AttributeError:
        return []
