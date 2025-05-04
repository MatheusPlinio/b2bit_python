from django.urls import path, include

urlpatterns = [
    path('auth/', include('twitter.urls.auth_urls')),
    path('posts/', include('twitter.urls.post_urls')),
    path('user/', include('twitter.urls.user_urls')),
    path('follow/', include('twitter.urls.follow_urls')),
]
