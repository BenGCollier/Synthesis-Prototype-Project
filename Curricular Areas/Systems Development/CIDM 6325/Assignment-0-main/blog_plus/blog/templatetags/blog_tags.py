import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post, Recipe

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

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
        total_recipe_comments=Count('recipe_comments')
    ).order_by('-total_recipe_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))