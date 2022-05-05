from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('register/', userRegistration, name='register'),
    path('tweet-details/', RetrieveTweetDetails, name="tweet-details"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create-tweet/', InsertTweetDetails, name="create-tweet"),
    path('delete-tweet/', DeleteTweetDetails, name="delete-tweet"),

]