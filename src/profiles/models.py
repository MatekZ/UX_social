from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse


class ProfileManager(models.Manager):
    def get_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_profiles_available_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        query_set = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set([])

        for relationship in query_set:
            if relationship.status == 'accepted':
                accepted.add(relationship.receiver)
                accepted.add(relationship.sender)

        available = [profile for profile in profiles if profile not in accepted]
        return available


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Brak opisu", max_length=350)
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def get_absolute_url(self):
        return reverse("profiles:profiles_detail_view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def friends_count(self):
        return self.friends.all().count()

    def posts_count(self):
        return self.posts.all().count()

    def get_posts(self):
        return self.posts.all()


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        slug_exists = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                slug_exists = Profile.objects.filter(slug=to_slug).exists()
                while slug_exists:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    slug_exists = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class InvitesReceivedManager(models.Manager):
    def invites_received(self, receiver):
        query_set = Relationship.objects.filter(receiver=receiver, status='send')
        return query_set


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = InvitesReceivedManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
