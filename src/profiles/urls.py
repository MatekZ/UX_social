from django.urls import path
from .views import my_profile_view, invites_received_view, profiles_view, ProfilesView, \
    send_invite, remove_friend, accept_invite, reject_invite, ProfilesDetailView, search_view

app_name = 'profiles'

urlpatterns = [
    path('', ProfilesView.as_view(), name='profiles_view'),
    path('myprofile/', my_profile_view, name='my_profile_view'),
    path('myinvites/', invites_received_view, name='invites_received_view'),
    path('sendinvite/', send_invite, name='send_invite'),
    path('removefriend/', remove_friend, name='remove_friend'),
    path('myinvites/accept/', accept_invite, name='accept_invite'),
    path('myinvites/reject/', reject_invite, name='reject_invite'),
    path('search/', search_view, name='search_view'),
    path('<slug>/', ProfilesDetailView.as_view(), name='profiles_detail_view'),

]
