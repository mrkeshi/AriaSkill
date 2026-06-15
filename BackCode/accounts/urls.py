from django.urls import path

from accounts.views import UserRegistrationAPIView, CustomTokenObtainPairView, ActivateAccountView, \
    RequestPasswordResetView, PasswordResetConfirmView, ChangePasswordView, UserProfileView, UserProfileUpdateView, \
    GoogleAuthView, AdminUserListView, AdminUserDetailView, AdminUserStatusView, AdminUserPasswordView, \
    PublicUserProfileView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('register/activate/', ActivateAccountView.as_view(), name='activate'),

    path('password_reset/request/', RequestPasswordResetView.as_view(), name='password_reset_request'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change_password/', ChangePasswordView.as_view(), name='user_change_password'),

    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('google/', GoogleAuthView.as_view(), name='google_auth'),

    path('profile/', UserProfileView.as_view(), name="fetch_user"),
    path('profile/edit/', UserProfileUpdateView.as_view(), name="edit_user_profile"),

    path('admin/users/', AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/users/<int:pk>/status/', AdminUserStatusView.as_view(), name='admin_user_status'),
    path('admin/users/<int:pk>/password/', AdminUserPasswordView.as_view(), name='admin_user_password'),

    path('users/<str:username>/', PublicUserProfileView.as_view(), name='public_user_profile'),
]
