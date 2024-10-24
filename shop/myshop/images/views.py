import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user  # Assign the current user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)  # Use GET data if applicable
    
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(
        request,
        'images/image/detail.html',
        {
            'section': 'images',
            'image': image,
            'total_views': total_views,
        },
    )

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)  # 8 images per page
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)  # Deliver first page
    except EmptyPage:
        if images_only:
            return HttpResponse('')  # Return an empty page for AJAX requests
        images = paginator.page(paginator.num_pages)  # Return last page of results

    if images_only:
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})

@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange(
        'image_ranking', 0, -1,
        desc=True
    )[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(
        Image.objects.filter(
            id__in=image_ranking_ids
        )
    )
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        'images/image/ranking.html',
        {'section': 'images', 'most_viewed': most_viewed},
    )

from recipe.models import Post 
from .forms import ImageCreateForm

def create_image(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            # Associate the image with a post (if applicable)
            post_id = request.POST.get('post_id')
            if post_id:
                new_image.post = Post.objects.get(id=post_id)
            new_image.save()
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm()

    return render(request, 'images/create.html', {'form': form})