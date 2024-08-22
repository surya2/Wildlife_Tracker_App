from django import template
register = template.Library()

@register.inclusion_tag('navbar.html')
def show_navbar(is_admin):
    return {'is_admin': is_admin}