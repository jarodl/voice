from django import template

register = template.Library()

@register.filter
def votes_left(feature):
    return feature.votes_left()

@register.filter
def state(feature):
    return feature.get_state_display()

@register.filter
def votes(feature):
    return feature.total_votes()
