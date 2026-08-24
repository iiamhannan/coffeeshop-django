from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',        views.home,        name='home'),
    path('menu/',        views.menu,        name='menu'),
    path('feedback/',    views.feedback,    name='feedback'),
    path('about/',       views.about,       name='about'),
    path('order-ahead/', views.order_ahead, name='order_ahead'),
]


# Media files (uploaded images) serve karne ke liye
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
