from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm

from .forms import BlogPostForm
from .models import BlogPost


def post_list(request):
    posts = BlogPost.objects.all().order_by("-created_at")

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts}
    )


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post}
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("post_detail", pk=post.pk)

    else:
        form = BlogPostForm()

    return render(
        request,
        "blog/post_form.html",
        {"form": form}
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)

    else:
        form = BlogPostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {"form": form}
    )


@login_required
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return render(
        request,
        "blog/post_confirm_delete.html",
        {"post": post}
    )


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("post_list")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )
