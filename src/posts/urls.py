from django.urls import path
from .views import posts_view, like_view, PostDeleteView, PostEditView
from django.conf import settings

from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('', posts_view, name='main_post_view'),
    path('liked/', like_view, name='like_post_view'),
    path('<pk>/delete', PostDeleteView.as_view(), name='delete_post'),
    path('<pk>/update', PostEditView.as_view(), name='edit_post'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)