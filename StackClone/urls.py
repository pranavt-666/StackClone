"""
URL configuration for StackClone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firstpage/',  views.IndexView.as_view(), name="index"),
    path('registration/' ,views.SignupView.as_view(), name='registration'),
    path('', views.LoginView.as_view(), name='login'),
    path('questions/<int:id>/' ,views.QuestionDetailView.as_view(), name='questiondetials'),
    path('questions/<int:id>/upvote', views.upvote_answer, name='upvote'),
    path('questions/answer/add/<int:id>/' ,views.post_answer, name='postanswer' ),
    path('questions/question-detail/answers/<int:id>/delete', views.delete_answer, name='delete-answer'),
    path('questions/logout/', views.signoutview, name='logout')
]
