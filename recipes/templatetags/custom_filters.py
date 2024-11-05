from django import template

register = template.Library()

@register.filter
def duration_to_string(value):
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours} hr {minutes} min"
    elif minutes > 0:
        return f"{minutes} min"
    else:
        return f"{seconds} sec"
