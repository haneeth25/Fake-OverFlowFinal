from django.urls import path
from . import views

urlpatterns = [
    path('login',views.loginPage,name='login'),
    path('create',views.createUser,name='create'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logoutUser,name='logout'),
    path('',views.home,name = 'home'),
    path('qna/<str:pk>/',views.qna,name ='qna'),
    path('create-question',views.createQuestion,name='create-question'),
    path('delete-question/<str:pk>/',views.deleteQuestion,name='delete-question'),
    path('delete-answer/<str:pk>/',views.deleteAnswer,name='delete-answer')
]
