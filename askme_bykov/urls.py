"""
URL configuration for askme_bykov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:question_id>', views.question, name="question"),
    path('ask', views.ask, name="ask"),
    path('login', views.log_in, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('settings', views.settings, name="settings"),
    path('hot', views.hot, name="hot"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('admin/', admin.site.urls),
    path('404', views.not_found, name="not_found"),
    path('like_question', views.like_question, name="like_question"),
    path('like_answer', views.like_answer, name="like_answer"),
    path('correct_answer', views.correct_answer, name="correct_answer"),
    path('set-language/<str:language>/', views.set_language, name='set_language'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
