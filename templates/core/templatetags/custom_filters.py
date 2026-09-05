from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Allows templates to look up a dictionary value by a dynamic key:
    {{ my_dict|get_item:some_variable }}
    Django's templates don't support this natively.
    """
    if not dictionary:
        return ''
    return dictionary.get(key, '')