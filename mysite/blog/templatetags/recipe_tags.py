import markdown
from django import template
from ..models import Recipe
from django.db.models import Count
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def total_recipes():
    return Recipe.published.count()

@register.inclusion_tag('blog/recipe/latest_recipes.html')
def show_latest_recipes(count=5):
    latest_recipes = Recipe.published.order_by('-publish')[:count]
    return {'latest_recipes': latest_recipes}

@register.simple_tag
def get_most_commented_recipes(count=5):
    return Recipe.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))