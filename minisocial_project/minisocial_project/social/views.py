from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Like, Follow, Profile

def ensure_profile(user):
    Profile.objects.get_or_create(user=user)

def signup(request):
    if request.user.is_authenticated:
        return redirect("feed")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        ensure_profile(user)
        login(request, user)
        messages.success(request, "Welcome to MiniSocial!")
        return redirect("feed")
    return render(request, "registration/signup.html", {"form": form})

def feed(request):
    if request.user.is_authenticated:
        ensure_profile(request.user)
    posts = Post.objects.select_related("author", "author__profile").prefetch_related("comments__author", "likes").annotate(like_count=Count("likes", distinct=True))
    if request.user.is_authenticated:
        followed_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
        posts = posts.filter(author_id__in=list(followed_ids) + [request.user.id]) if request.GET.get("following") else posts
    post_form = PostForm()
    comment_form = CommentForm()
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    return render(request, "social/feed.html", {
        "posts": posts, "post_form": post_form, "comment_form": comment_form, "liked_ids": liked_ids,
    })

@login_required
@require_POST
def create_post(request):
    ensure_profile(request.user)
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post is live.")
    else:
        messages.error(request, "Please enter a post (up to 2,000 characters).")
    return redirect("feed")

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("feed")

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
    return redirect("profile", username=target.username)

@login_required
@require_POST
def edit_profile(request):
    ensure_profile(request.user)
    form = ProfileForm(request.POST, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
    else:
        messages.error(request, "Check your profile details and try again.")
    return redirect("profile", username=request.user.username)

def profile(request, username):
    person = get_object_or_404(User.objects.select_related("profile"), username=username)
    ensure_profile(person)
    posts = Post.objects.filter(author=person).select_related("author").prefetch_related("comments__author", "likes").annotate(like_count=Count("likes", distinct=True))
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=person).exists()
    follower_count = Follow.objects.filter(following=person).count()
    following_count = Follow.objects.filter(follower=person).count()
    liked_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True)) if request.user.is_authenticated else set()
    return render(request, "social/profile.html", {
        "person": person, "posts": posts, "is_following": is_following,
        "follower_count": follower_count, "following_count": following_count, "liked_ids": liked_ids,
        "profile_form": ProfileForm(instance=person.profile) if request.user == person else None,
        "comment_form": CommentForm(),
    })

def explore(request):
    users = User.objects.exclude(id=request.user.id if request.user.is_authenticated else None).annotate(
        follower_total=Count("follower_links", distinct=True)
    ).select_related("profile").order_by("-follower_total", "username")[:30]
    following_ids = set(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)) if request.user.is_authenticated else set()
    return render(request, "social/explore.html", {"users": users, "following_ids": following_ids})

def search(request):
    query = request.GET.get("q", "").strip()[:50]
    users = User.objects.filter(username__icontains=query).select_related("profile")[:20] if query else User.objects.none()
    posts = Post.objects.filter(body__icontains=query).select_related("author", "author__profile")[:30] if query else Post.objects.none()
    return render(request, "social/search.html", {"query": query, "users": users, "posts": posts, "liked_ids": set(Like.objects.filter(user=request.user).values_list("post_id", flat=True)) if request.user.is_authenticated else set(), "comment_form": CommentForm()})
