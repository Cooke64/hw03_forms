from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail

from .forms import PostForm
from .models import Post, User, Group


send_mail(
    'Тема письма',
    'Текст письма.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)

AMOUNT_POST = 10


def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, AMOUNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, AMOUNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counter_posts = author.posts.count()
    context = {
        'author': author,
        'page_obj': page_obj,
        'counter_posts': counter_posts,

    }
    template = 'posts/profile.html'
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = 'Записи сообщества'
    group = get_object_or_404(Group, slug=slug)
    get_posts = Post.objects.filter(group=group)
    posts = get_posts.order_by('-pub_date')[:AMOUNT_POST]
    paginator = Paginator(posts, AMOUNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    username = posts.author
    username_obj = User.objects.get(username=username)
    posts_counter = username_obj.posts.count()
    template = 'posts/post_detail.html'
    title = 'Подробная информация'
    context = {
        'title': title,
        'posts': posts,
        'posts_counter': posts_counter

    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('post:profile', request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    author = get_object_or_404(User, username=request.user)
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if author != post.author:
        return redirect("post:post_detail", post_id=post_id)
    if form.is_valid():
        post.author = author
        post.save()
        return redirect('post:post_detail', post_id=post_id)
    is_edit = True
    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'posts/create_post.html', context)
