from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'admin'

urlpatterns = [
    path('login/', admin_login, name = 'admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('index/', admin_index, name='admin_main'),
    path('member/', member_manage, name='member'),
    path('update/<int:id>', member_update, name='info_update'),
    path('faq/', faq_manage, name='m2m_faq'),
    path('answer/<int:id>', answer_window, name='m2m_answer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)