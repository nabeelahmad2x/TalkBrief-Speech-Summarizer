from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('summarize/', views.summarize, name='summarize'),
    path('history/' , views.history, name='history'),
    path('howto/' , views.howto, name='howto'),
    path('whyus/' , views.whyus, name='whyus'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
