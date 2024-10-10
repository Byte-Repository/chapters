from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm, RatingForm
from .models import Post, Rating

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)   

    return render(
        request,
        'recipe/post/list.html',
        {
            'posts': posts,
            'tag': tag
            }
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # Calculate average rating
    average_rating = post.ratings.aggregate(Avg('score'))['score__avg'] or "No ratings yet" # Get the average rating

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id).annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'recipe/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'average_rating': average_rating,  # Pass the average rating to the context
            'similar_posts': similar_posts,
        }
    )

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'recipe/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'recipe/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }   
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'recipe/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )

    return render(
        request,
        'recipe/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        },
    )

def rate_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                post=post,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
            if not created:
                rating.score = form.cleaned_data['score']
                rating.save()
            # Redirect to post detail view
            return redirect('recipe:post_detail', year=post.publish.year, month=post.publish.month, day=post.publish.day, post=post.slug)
    else:
        form = RatingForm()

    return render(request, 'recipe/post/rate_post.html', {'form': form, 'post': post})

from .forms import RecipeForm
from .models import Post

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect('recipe:post_detail', year=recipe.publish.year, month=recipe.publish.month, day=recipe.publish.day, post=recipe.slug)
    else:
        form = RecipeForm()
    return render(request, 'recipe/post/create.html', {'form': form})

def edit_recipe(request, year, month, day, post):
    recipe = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe:post_detail', year=recipe.publish.year, month=recipe.publish.month, day=recipe.publish.day, post=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe/post/edit.html', {'form': form, 'recipe': recipe})
