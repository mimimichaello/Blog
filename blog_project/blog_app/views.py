from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpResponseForbidden
from .forms import PostForm

def home(request):
    posts = Post.objects.all()
    context = {
                'posts': posts,
                'title': 'Домашняя страница',
               }
    return render(request,'blog_app/home.html', context)


def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        if post.author != request.user:
            return HttpResponseForbidden("Вы не являетесь автором этого поста.")

        post.delete()
        return redirect('home')

    context = {
        'post': post,
        'title': post.title
    }
    return render(request, 'blog_app/single_post.html', context)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Привязываем пост к текущему пользователю
            post.save()

            request.user.profile.user_posts_count = Post.objects.filter(author=request.user).count()
            request.user.profile.save()

            return redirect('home')  # Перенаправляем на страницу статей после создания поста
    else:
        form = PostForm()
    return render(request, 'blog_app/create_post.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого поста.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog_app/edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого поста.")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    # Если запрос не POST, вы можете вернуть страницу подтверждения удаления,
    # где пользователь должен подтвердить свое намерение удалить пост.

    context = {
        'post': post,
        'title': 'Подтвердите удаление поста'
    }
    return render(request, 'blog_app/delete_post_confirm.html', context)
