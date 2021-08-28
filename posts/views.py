from django.shortcuts import render
from users.models import User

from .models import Posts
from .forms import CreatePostForm


def main_page_view(request):
    posts = Posts.objects.all()
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            Posts.objects.create(
                author=user,
                text=form.cleaned_data['text'],
                post_image=form.cleaned_data['image']
            )
    else:
        form = CreatePostForm()
    return render(request, 'posts/main.html', {
        'form': form,
        'posts': posts
    })
