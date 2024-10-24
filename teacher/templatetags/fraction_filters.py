from django import template
import re

register = template.Library()

@register.filter
def format_fraction(text):
    # This regex will find all fractions in the format "numerator/denominator"
    fraction_pattern = r'(\d+)/(\d+)'
    
    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        # Return formatted fraction HTML with a dash
        return f'<span class="fraction"><span class="numerator">{numerator}</span><span class="separator"></span><span class="denominator">{denominator}</span></span>'
    
    # Substitute all occurrences of fractions in the text
    formatted_text = re.sub(fraction_pattern, replace_fraction, text)
    
    # Adding operator styling for plus and minus signs
    formatted_text = formatted_text.replace('+', '<span class="operator">+</span>')
    formatted_text = formatted_text.replace('-', '<span class="operator">-</span>')
    formatted_text = formatted_text.replace('×', '<span class="operator">×</span>')
    formatted_text = formatted_text.replace('÷', '<span class="operator">÷</span>')

    return formatted_text
