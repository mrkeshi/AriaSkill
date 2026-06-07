from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ActivationSerializer, \
    RequestPasswordResetSerializer, PasswordResetConfirmSerializer, ChangePasswordSerializer, UserProfileSerializer, \
    UserProfileUpdateSerializer, GoogleAuthSerializer, AdminUserSerializer, AdminUserStatusSerializer, \
    AdminUserPasswordSerializer, PublicUserProfileSerializer
from accounts.services.activation_service import send_activation_register_email, send_activation_change_pass_email
from activity.events import password_changed as password_changed_signal

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                send_activation_register_email(user)

                return Response({
                    'message': 'registration successful and sent activation link',
                    'user': serializer.data,
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'message': 'registration failed',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class GoogleAuthView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_200_OK)


class ActivateAccountView(generics.GenericAPIView):
    serializer_class = ActivationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            uid64 = serializer.validated_data['uid']
            token = serializer.validated_data['token']

            try:
                uid = urlsafe_base64_decode(uid64).decode()
                user = User.objects.get(pk=uid)

            except (ValueError, TypeError, User.DoesNotExist):
                return Response({'error': 'Invalid UID or user does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)

            if user.is_active:
                return Response({'message': 'Account already active'},
                                status=status.HTTP_200_OK)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated successfully'},
                                status=status.HTTP_200_OK)
            return Response({'error': 'Invalid or expired token'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        if not email:
            return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user:
            uid, token = send_activation_change_pass_email(user)
            print(f"{uid} \n {token}")

        return Response({'message': 'If an account exists, Password reset email sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        uid64 = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        password_confirm = serializer.validated_data['password_confirm']

        if password != password_confirm:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({'error': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        password_changed_signal.send(
            sender=user.__class__,
            user=user,
            request=request,
            method='reset',
        )

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        password_changed_signal.send(
            sender=user.__class__,
            user=user,
            request=request,
            method='account',
        )

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user


class AdminUserListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'job_title']

    def get_queryset(self):
        return User.objects.all().order_by('-id')


class AdminUserDetailView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.pk == request.user.pk:
            return Response({'detail': 'You cannot delete your own account'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class AdminUserStatusView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminUserStatusSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_active = serializer.validated_data['is_active']
        if user.pk == request.user.pk and not is_active:
            return Response({'detail': 'You cannot deactivate your own account'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = is_active
        user.save(update_fields=['is_active'])
        return Response(AdminUserSerializer(user).data, status=status.HTTP_200_OK)


class AdminUserPasswordView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminUserPasswordSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])

        password_changed_signal.send(
            sender=user.__class__,
            user=user,
            request=request,
            related_user=request.user,
            method='admin',
        )

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


class PublicUserProfileView(generics.RetrieveAPIView):
    """
    GET /api/account/users/<username>/
    Public profile — no authentication required.
    Returns user info + their approved projects with total likes.
    """
    permission_classes = (AllowAny,)
    serializer_class = PublicUserProfileSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    queryset = User.objects.filter(is_active=True)