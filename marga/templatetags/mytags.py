# mytags.py
from django import template
register = template.Library()

@register.filter(is_safe=True)
def format_percent(value, args: str=""):
    """
    Format a numeric value as percentage
    :param value: the numeric value
    :param args: a CSV string of arguments to the formatting operation
    :return: the formatted value
    """
    # splits the arguments string into a list of arguments
    arg_list = [arg.strip() for arg in args.split(',')] if args else []
    # sets the precision (number of decimal digits)
    precision = int(arg_list[0]) if len(arg_list) > 0 else 0
    # should the "%" symbol be included?
    include_symbol = bool(arg_list[1]) if len(arg_list) > 1 else True
    symbol = " %" if include_symbol else ""
    # builds and returns the formatted value
    return f"{float(value) * 100.0:.{precision}f}{symbol}"

@register.filter
def as_percentage_of(part, whole):
    try:
        if whole == None:
            return ""
        return "%d%%" % (100 - (float(part) / float(whole) * 100))
    except (ValueError, ZeroDivisionError):
        return ""