from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # print('sender: ', sender)
    # print('insatnce: ', instance)
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def add_to_friends(sender, instance, created, **kwargs):
    req_sender = instance.sender
    req_receiver = instance.receiver
    if instance.status == 'accepted':
        req_sender.friends.add(req_receiver.user)
        req_receiver.friends.add(req_sender.user)
        req_sender.save()
        req_receiver.save()

@receiver(pre_delete, sender=Relationship)
def remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver

    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
