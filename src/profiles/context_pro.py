from .models import Profile, Relationship


def avatar_disp(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        p_avatar = profile_obj.avatar
        return {'p_avatar': p_avatar}
    return {}


def invites_number(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        invites = Relationship.objects.invites_received(profile_obj).count()
        return {'invites': invites}
    return {}
