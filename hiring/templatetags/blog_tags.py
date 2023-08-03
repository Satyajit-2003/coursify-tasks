from django import template

register = template.Library()

@register.filter(name='get_skills')
def get_skills(job):
    return job.skills.split(',')

@register.filter(name='private')
def private(obj, attribute):
    return getattr(obj, attribute)