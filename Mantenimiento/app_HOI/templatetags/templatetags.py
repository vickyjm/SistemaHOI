from django import template
from django.contrib.auth.models import Group
from app_HOI.models import Categoria, Item

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.inclusion_tag("templatetags/categoria.html")
def lista_categorias():
    return {'categorias' : Categoria.objects.all()}