from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    re_path('has-mutated', views.has_mutated, name='body'),
    re_path('add-message', views.addMessage, name='body'),
    re_path('get-messages', views.get_messages, name='body'),
    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),
    re_path(r'', views.pages, name='pages'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)