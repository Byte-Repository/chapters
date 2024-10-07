from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post

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
        'blog/post/list.html',
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
        publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

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
        'blog/post/share.html',
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
        'blog/post/comment.html',
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
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        },
    )

# def recipe_list(request, tag_slug=None):
#     recipe_list = Recipe.published.all()
#     tag = None
#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         recipe_list = recipe_list.filter(tags__in=[tag])
    
#     # Pagination with 3 recipes per page
#     paginator = Paginator(recipe_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         recipes = paginator.page(page_number)
#     except PageNotAnInteger:
#         recipes = paginator.page(1)
#     except EmptyPage:
#         recipes = paginator.page(paginator.num_pages)

#     return render(
#         request,
#         'blog/recipe/list.html',
#         {'recipes': recipes, 'tag': tag}
#     )

# def recipe_detail(request, year, month, day, recipe):
#     recipe = get_object_or_404(
#         Recipe,
#         status=Recipe.Status.PUBLISHED,
#         slug=recipe,
#         publish__year=year,
#         publish__month=month,
#         publish__day=day
#     )
    
#     # List of active comments for this recipe
#     comments = recipe.comments.filter(active=True)
#     form = CommentForm()

#     # Similar recipes based on tags
#     recipe_tags_ids = recipe.tags.values_list('id', flat=True)
#     similar_recipes = Recipe.published.filter(tags__in=recipe_tags_ids).exclude(id=recipe.id)
#     similar_recipes = similar_recipes.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

#     # Calculate average rating
#     average_rating = recipe.ratings.aggregate(average=Avg('score'))['average']

#     return render(
#         request,
#         'blog/recipe/detail.html',
#         {
#             'recipe': recipe,
#             'comments': comments,
#             'form': form,
#             'similar_recipes': similar_recipes,
#             'average_rating': average_rating,
#         }
#     )

# @require_POST
# def recipe_comment(request, recipe_id):
#     recipe = get_object_or_404(
#         Recipe,
#         id=recipe_id,
#         status=Recipe.Status.PUBLISHED
#     )
#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.recipe = recipe
#         comment.save()
#         return redirect(recipe.get_absolute_url())  # Redirect after comment submission
#     return render(
#         request,
#         'blog/recipe/comment.html',
#         {
#             'recipe': recipe,
#             'form': form,
#         }
#     )

# @require_POST
# def submit_rating(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     form = RatingForm(request.POST)
    
#     if form.is_valid():
#         score = form.cleaned_data['score']
#         comment = form.cleaned_data['comment']
        
#         # Update or create the rating to avoid duplicate ratings by the same user
#         Rating.objects.update_or_create(
#             recipe=recipe,
#             user=request.user,  # Assuming you're using a logged-in user
#             defaults={'score': score, 'comment': comment}
#         )
#         return redirect(recipe.get_absolute_url())
    
#     return render(request, 'blog/recipe/detail.html', {
#         'recipe': recipe,
#         'rating_form': form,
#         'comment_form': CommentForm(),  # Load an empty comment form as well
#     })

# def recipe_share(request, recipe_id):
#     # Retrieve recipe by id
#     recipe = get_object_or_404(
#         Recipe,
#         id=recipe_id,
#         status=Recipe.Status.PUBLISHED
#     )
#     sent = False

#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)  # You can reuse the same form for recipes
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             recipe_url = request.build_absolute_uri(
#                 recipe.get_absolute_url()
#             )
#             subject = (
#                 f"{cd['name']} ({cd['email']}) "
#                 f"recommends you try the recipe {recipe.title}"
#             )
#             message = (
#                 f"Try the recipe {recipe.title} at {recipe_url}\n\n"
#                 f"{cd['name']}\'s comments: {cd['comments']}"
#             )
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=None,
#                 recipient_list=[cd['to']]
#             )
#             sent = True
#     else:
#         form = EmailPostForm()

#     return render(
#         request,
#         'blog/recipe/share.html',  # Create this template similarly to 'post/share.html'
#         {
#             'recipe': recipe,
#             'form': form,
#             'sent': sent
#         }
#     )


# @require_POST
# def submit_rating(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     form = RatingForm(request.POST)
    
#     if form.is_valid():
#         score = form.cleaned_data['score']
#         comment = form.cleaned_data['comment']
        
#         # Check if the user has already rated this recipe
#         rating, created = Rating.objects.update_or_create(
#             recipe=recipe,
#             user=request.user,  # Assuming you're using a logged-in user
#             defaults={'score': score, 'comment': comment}
#         )
        
#         if created:
#             # Rating was created
#             message = "Thank you for your rating!"
#         else:
#             # Rating was updated
#             message = "Your rating has been updated!"

#         # Optionally, add a success message to be displayed on the recipe detail page
#         # Add `message` to the context if you want to display it
        
#         return redirect(recipe.get_absolute_url())
    
#     # If the form is not valid, you might want to handle the error appropriately
#     return render(request, 'blog/recipe/rating.html', {
#         'recipe': recipe,
#         'rating_form': form,
#         'comment_form': CommentForm(),  # Load an empty comment form as well
#     })
