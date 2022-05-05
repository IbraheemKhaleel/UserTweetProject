import datetime
import logging

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import tweets
from .serializers import UserSerializerWithToken, TweetSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        If you want to add data outside token
         """

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user)

        for key, value in serializer.data.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RetrieveTweetDetails(request):
    username = request.GET.get('username')
    date = request.GET.get('date')
    tweets_values = tweets.objects.filter(is_delete=False, updated_at__gte=date, user__username=username).values()
    logging.info(f"tweet details fetched successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully fetched tweet details', 'status_code': 200, 'data' : tweets_values}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def InsertTweetDetails(request):
    data = request.data
    tweet_obj = tweets.objects.create(tweet=data['tweet'], user=data['user'])
    logging.info(f"tweet object with sapid {data['sapid']} created successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully created tweet details', 'status_code': 201})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteTweetDetails(request):
    username = request.data.get('username')
    if not username:
        return Response({'message': 'Please provide username', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    try:
        tweet_obj = tweets.objects.filter(user__username=username)
    except tweets.DoesNotExist:
        return Response({'message': 'Tweet of the respective username back does not exist', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    tweet_obj.update(is_delete=True, deleted_at=datetime.datetime.now())
    logging.info(f"tweet object with username {username} deleted successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully deleted tweet details', 'status_code': 200, 'data' : {'number_of_tweets': tweet_obj.count(), 'tweets' : tweet_obj.values('id','tweet')}},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def userRegistration(request):
    data = request.data
    try:
        user = User.objects.create_user(first_name=data['name'], email=data['email'],
                                        password=data['password'])
        serializer = UserSerializerWithToken(user, many=False).data
        return Response(serializer)
    except Exception as e:
        message = {'message': 'The username should be unique'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)