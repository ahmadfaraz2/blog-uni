from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, PostForm
from django.contrib.auth.decorators import login_required

from taggit.models import Tag
from django.db.models import Count
from django.utils.text import slugify

from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from django.views.generic import ListView

# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not a integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {'posts':posts, "tag":tag})

@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
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
    post_tags_id = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:4]

    return render(request,
                "blog/post/detail.html",
                {"post": post, 
                "comments": comments, 
                "form": form,
                "similar_posts": similar_posts})

@login_required
def post_share(request, post_id):
    # Retrieve post by id 
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields pass validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email="ahmadfarazjanjua780@gmail.com",
                recipient_list=[cd['to']]
                )
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


@require_POST
@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(request.POST)
    if form.is_valid():
        # Create a comment object without saving it to database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to database
        comment.save()

    return render(request, "blog/post/comment.html", {"post":post, "form": form, "comment":comment})


# --------------------------------------Adding CRUD Functionality------------------------------------

# Create View
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = Post.Status.PUBLISHED
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()  # Save the tags
            return redirect("blog:post_detail", post.publish.year, post.publish.month, post.publish.day, post.slug)
        
    else: 
        form = PostForm()

    return render(request, "blog/post/post_form.html", {"form":form})


@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    if post.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.status = Post.Status.PUBLISHED
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            form.save_m2m() # Save the tags
            return redirect("blog:post_detail", post.publish.year, post.publish.month, post.publish.day, post.slug)
        
    else: 
        form = PostForm(instance=post)
    
    return render(request, "blog/post/post_form.html", {"form":form, "post": post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')

    return render(request, 'blog/post/post_confirm_delete.html', {'post': post})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"