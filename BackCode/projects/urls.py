from django.urls import path

from projects.admin_views import (
    SkillListCreateView,
    SkillRetrieveUpdateDestroyView,
    AdminProjectListView,
    AdminProjectDetailView,
    AdminProjectStatusView,
    AdminCommentListView,
    AdminCommentModerationView,
)
from projects.views import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectLikeView,
    ProjectDownloadView,
    ProjectUnlikeView,
    CommentListCreateView,
    CommentDetailView,
    PublicProjectListView,
    MyProjectCommentsView, DashboardChartView,
    ProjectYearsView, DashboardStatsView,
)

urlpatterns = [
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:id>/', SkillRetrieveUpdateDestroyView.as_view(), name='skill-detail'),

    path('admin/projects/', AdminProjectListView.as_view(), name='admin-project-list'),
    path('admin/projects/<str:slug>/', AdminProjectDetailView.as_view(), name='admin-project-detail'),
    path('admin/projects/<str:slug>/status/', AdminProjectStatusView.as_view(), name='admin-project-status'),
    path('admin/comments/', AdminCommentListView.as_view(), name='admin-comment-list'),
    path('admin/comments/<int:pk>/', AdminCommentModerationView.as_view(), name='admin-comment-moderation'),

    path('dashboard/chart/', DashboardChartView.as_view(), name='dashboard-chart'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),

    path('', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/public/', PublicProjectListView.as_view(), name='public-project-list'),
    path('projects/years/', ProjectYearsView.as_view(), name='public-project-years'),
    path('comments/my-projects/', MyProjectCommentsView.as_view(), name='my-project-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:project_id>/comments/', CommentListCreateView.as_view(), name='project-comments'),
    path('<str:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<str:slug>/like/', ProjectLikeView.as_view(), name='project-like'),
    path('<str:slug>/unlike/', ProjectUnlikeView.as_view(), name='project-unlike'),
    path('<str:slug>/download/', ProjectDownloadView.as_view(), name='project-download'),
]