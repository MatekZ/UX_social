from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def posts_view(requset):
    query_set = Post.objects.all()
    profile = Profile.objects.get(user=requset.user)
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_add_check = False

    if 'submit_post' in requset.POST:
        post_form = PostModelForm(requset.POST, requset.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_add_check = True



    if 'submit_comment' in requset.POST:
        comment_form = CommentModelForm(requset.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=requset.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()


    context = {
        'qs': query_set,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_add_ckeck': post_add_check,
    }

    return render(requset, 'posts/main.html', context)


@login_required
def like_view(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        post_obj.save()
        like.save()

        data = {
            'value': like.value,
            'like_count': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('posts:main_post_view')


def get_like_value(user, post):
    like_data = Like.objects.filter(user=user, post=post).first()
    return like_data.value if like_data else None


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('posts:main_post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)

        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'Błąd w usuwaniu posta. Nie jesteś jego autorem!')
        return obj


class PostEditView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)

        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Błąd w edytowaniu posta. Nie jesteś jego autorem!')
            return super().form_valid(form)
