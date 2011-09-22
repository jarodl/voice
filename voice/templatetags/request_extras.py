from django import template

register = template.Library()

@register.filter
def votes_left(request):
    return request.votes_left()

@register.filter
def state(request):
    return request.get_state_display()
