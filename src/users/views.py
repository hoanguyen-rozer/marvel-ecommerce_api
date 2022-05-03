from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from src.common.mixins import UpdateModelMixin
from src.common.serializers import TokenObtainPairResponseSerializer, NotificationSerializer
from src.users.models import Profile
from src.users.serializers import UserSerializer, ProfileSerializer, UserRegisterSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer
from src.users.serializers.user import UserChangePasswordSerializer

User = get_user_model()


class UserDetailAPIView(UpdateModelMixin, RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('address')
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


user_detail_view = UserDetailAPIView.as_view()


class UserListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('address')
    permission_classes = ()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email', 'created_at', 'updated_at']


user_list_view = UserListAPIView.as_view()


class UserActiveAPIView(APIView):
    """
    Class update active status of user
    """

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        user_data = User.objects.get(id=user_id)
        if not user_data.is_active:
            user_data.is_active = True
        return Response(status=status.HTTP_201_CREATED)


user_active_view = UserActiveAPIView.as_view()


class UserBanAPIView(APIView):
    """
    Ban user API
    """

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        user_data = User.objects.get(id=user_id)
        if user_data.is_active:
            user_data.is_active = False
        return Response(status=status.HTTP_201_CREATED)


user_ban_view = UserBanAPIView.as_view()


# class ProfileDetailAPIView(UpdateModelMixin, DestroyAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#     permission_classes = ()
#     lookup_field = 'id'

class ProfileViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Profile view set
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = ()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = 'id'


class UserLoginAPIView(TokenObtainPairView):
    """
    Class Login API which inherits simplejwt's view
    """

    # Set schema format for Swagger UI decorator
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


user_login_view = UserLoginAPIView.as_view()


class UserLogoutAPIView(GenericAPIView):
    """
    Class logout user API
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        # logout(request)
        # TODO: process access and refresh token
        data = {
            'message': "Successfully logged out",
            'success': True
        }
        return Response(data=data, status=status.HTTP_200_OK)


user_logout_view = UserLogoutAPIView.as_view()


class AuthViewSet(GenericViewSet):
    """
    Class define auth methods relate account and password
    """
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False, serializer_class=UserRegisterSerializer)
    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: TokenObtainPairResponseSerializer,
        }
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print('USER: ', user)

        # return token pair for client
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, serializer_class=UserChangePasswordSerializer,
            permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer
        }
    )
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        data = {
            'message': "Successfully changed password",
            'success': True
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, serializer_class=ForgotPasswordSerializer)
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer
        }
    )
    def forgot_password(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode((smart_bytes(user.id)))

            # Generate token reset password
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse_lazy('verify_forgot_password', kwargs={'uidb64': uidb64, 'token': token})
            absolute_link = "http://" + current_site + relative_link
            # email_body = 'Hello, \n Use link below to reset your password  \n' + absolute_link
            # email = EmailMessage(subject='Reset password', body=email_body, to=email)
            # email.send()
            data = {
                'message': "An email is sent you to reset your password",
                'success': True,
                'verify_link': absolute_link
            }
            return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, serializer_class=ResetPasswordSerializer)
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer
        }
    )
    def reset_password(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'Password reset success',
            'success': True
        }
        return Response(data=data, status=status.HTTP_200_OK)


class VerifyForgotPasswordAPIView(GenericAPIView):
    """
    Class verify link reset password
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer
        }
    )
    def get(self, request, uidb64, token):
        try:
            # Get user id from url uidb
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            # Check user with token received
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(data={
                    'message': "Token is invalid, please request a new one",
                    'success': False
                }, status=status.HTTP_401_UNAUTHORIZED)
            data = {
                'message': "credentials valid",
                'success': True,
                'uid64': uidb64,
                'token': token
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response(data={
                'message': "Token is invalid, please request a new one",
                'success': False
            }, status=status.HTTP_401_UNAUTHORIZED)


verify_forgot_password = VerifyForgotPasswordAPIView.as_view()
