from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('summarize/', views.summarize, name='summarize'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
