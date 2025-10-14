from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /accounts/register
    Body: {username, email, password, ...}
    Returns: created user + token (serializer handles token creation/return)
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    """
    POST /accounts/login
    Body: {username, password}
    Returns: {"token": "..."} (serializer handles token creation/return)
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()  # e.g., {"token": "..."}
        return Response(data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /accounts/profile
    PATCH/PUT /accounts/profile
    Auth: Token
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


User = get_user_model()


class FollowUserView(APIView):
    """
    POST /accounts/follow/<int:user_id>/
    Auth: Token
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # returns False if already following
        created = request.user.follow(target)
        return Response(
            {
                "followed_user": target.id,
                "created": created,
                "following_count": request.user.following_count,
                "target_followers_count": target.followers_count,
            },
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    """
    POST /accounts/unfollow/<int:user_id>/
    Auth: Token
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.unfollow(target)
        return Response(
            {
                "unfollowed_user": target.id,
                "following_count": request.user.following_count,
                "target_followers_count": target.followers_count,
            },
            status=status.HTTP_200_OK,
        )


CustomUser = get_user_model()


class UserListView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = CustomUser.objects.all()
