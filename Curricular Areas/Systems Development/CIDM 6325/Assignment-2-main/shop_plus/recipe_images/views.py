from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from actions.utils import create_action
from django.conf import settings
import redis

from .forms import RecipeImageCreateForm
from .models import RecipeImage

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

@login_required
def recipe_image_create(request):
    if request.method == 'POST':
        # form is sent
        form = RecipeImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_recipe_image = form.save(commit=False)
            # assign current user to the item
            new_recipe_image.user = request.user
            new_recipe_image.save()
            create_action(request.user, 'bookmarked image', new_recipe_image)
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail view
            return redirect(new_recipe_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = RecipeImageCreateForm(data=request.GET)
    return render(
        request,
        'recipe_images/recipe_image/create.html',
        {'section': 'recipe_images', 'form': form},
    )


def recipe_image_detail(request, id, slug):
    recipe_image = get_object_or_404(RecipeImage, id=id, slug=slug)
    total_views = r.incr(f'recipe_image:{recipe_image.id}:views')
    r.zincrby('recipe_image_ranking', 1, recipe_image.id)
    return render(
        request,
        'recipe_images/recipe_image/detail.html',
        {
            'section': 'recipe_images', 
            'recipe_image': recipe_image,
            'total_views': total_views
        },
    )


@login_required
@require_POST
def recipe_image_like(request):
    recipe_image_id = request.POST.get('id')
    action = request.POST.get('action')
    if recipe_image_id and action:
        try:
            recipe_image = RecipeImage.objects.get(id=recipe_image_id)
            if action == 'like':
                recipe_image.users_like.add(request.user)
                create_action(request.user, 'likes', recipe_image)
            else:
                recipe_image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except RecipeImage.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def recipe_image_list(request):
    recipe_images = RecipeImage.objects.all()
    paginator = Paginator(recipe_images, 8)
    page = request.GET.get('page')
    recipe_images_only = request.GET.get('recipe_images_only')
    try:
        recipe_images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        recipe_images = paginator.page(1)
    except EmptyPage:
        if recipe_images_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        recipe_images = paginator.page(paginator.num_pages)
    if recipe_images_only:
        return render(
            request,
            'recipe_images/recipe_image/list_images.html',
            {'section': 'recipe_images', 'recipe_images': recipe_images},
        )
    return render(
        request,
        'recipe_images/recipe_image/list.html',
        {'section': 'recipe_images', 'recipe_images': recipe_images},
    )

@login_required
def recipe_image_ranking(request):
    # get recipe_image ranking dictionary
    recipe_image_ranking = r.zrange(
        'recipe_image_ranking', 0, -1,
        desc=True
    )[:10]
    recipe_image_ranking_ids = [int(id) for id in recipe_image_ranking]
    # get most viewed recipe_images
    most_viewed = list(
        RecipeImage.objects.filter(
            id__in=recipe_image_ranking_ids
        )
    )
    most_viewed.sort(key=lambda x: recipe_image_ranking_ids.index(x.id))
    return render(
        request,
        'recipe_images/recipe_image/ranking.html',
        {'section': 'recipe_images', 'most_viewed': most_viewed},
    )