from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForms
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def search_view(request):
    # is_check = False
    if request.method == "POST":
        searched = request.POST['searched']
        found = Profile.objects.filter(user__username__icontains=searched)
        # is_check = True
        return render(request, 'profiles/search.html', {'searched': searched, 'found': found})
    else:
        return redirect('posts:main_post_view')


@login_required
def my_profile_view(request):
    my_profile = Profile.objects.get(user=request.user)

    form = ProfileModelForms(request.POST or None, request.FILES or None, instance=my_profile)
    updated = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            updated = True

    context = {
        'my_profile': my_profile,
        'form': form,
        'updated': updated,
    }

    return render(request, 'profiles/myprofile.html', context)


@login_required
def invites_received_view(request):
    my_profile = Profile.objects.get(user=request.user)
    query_set = Relationship.objects.invites_received(my_profile)
    invites = list(map(lambda x: x.sender, query_set))
    no_inv = False

    if len(invites) == 0:
        no_inv = True

    context = {
        'qs': invites,
        'no_inv': no_inv,
    }

    return render(request, 'profiles/myinvites.html', context)


@login_required
def accept_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()

    return redirect('profiles:invites_received_view')


@login_required
def reject_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()

    return redirect('profiles:invites_received_view')


@login_required
def profiles_view(request):
    user = request.user
    query_set = Profile.objects.get_profiles(user)

    context = {
        'qs': query_set
    }

    return render(request, 'profiles/allprofiles.html', context)


class ProfilesDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detailview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relation_receiver = Relationship.objects.filter(sender=profile)
        relation_sender = Relationship.objects.filter(receiver=profile)
        receiver_list = []
        sender_list = []

        for item in relation_receiver:
            receiver_list.append(item.receiver.user)

        for item in relation_sender:
            sender_list.append(item.sender.user)

        context["receiver_list"] = receiver_list
        context["sender_list"] = sender_list
        context["posts"] = self.get_object().get_posts()
        context["posts_ckeck"] = True if len(self.get_object().get_posts()) > 0 else False

        return context


class ProfilesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/allprofiles.html'

    def get_queryset(self):
        query_set = Profile.objects.get_profiles(self.request.user)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        relation_receiver = Relationship.objects.filter(sender=profile)
        relation_sender = Relationship.objects.filter(receiver=profile)
        receiver_list = []
        sender_list = []

        for item in relation_receiver:
            receiver_list.append(item.receiver.user)

        for item in relation_sender:
            sender_list.append(item.sender.user)

        context["receiver_list"] = receiver_list
        context["sender_list"] = sender_list
        context["qs_empty"] = False

        if len(self.get_queryset()) == 0:
            context["qs_empty"] = True

        return context


@login_required
def send_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')


@login_required
def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        relationship.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')
