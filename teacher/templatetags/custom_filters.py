# teacher/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))  # Use str(key) to match with JSON keys

@register.filter
def percentage(value, total):
    try:
        return int((value / total) * 100)
    except (ZeroDivisionError, TypeError):
        return 0

@register.filter
def format_fraction(value):
    # Assuming `value` is a string in the format "numerator/denominator"
    if isinstance(value, str) and '/' in value:
        numerator, denominator = value.split('/')
        return f"{numerator} / {denominator}"  # Adjust formatting as needed
    return value