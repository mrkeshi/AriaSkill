from django.urls import path

from projects.views.admin_views import (
    SkillListCreateView,
    SkillRetrieveUpdateDestroyView,
    AdminProjectListView,
    AdminProjectDetailView,
    AdminProjectStatusView,
    AdminCommentListView,
    AdminCommentModerationView,
)
from projects.views.comment_views import CommentListCreateView, CommentDetailView, MyProjectCommentsView
from projects.views.dashboard_views import DashboardChartView, DashboardStatsView
from projects.views.project_views import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectLikeView,
    ProjectDownloadView,
    ProjectUnlikeView,
    PublicProjectListView,
    ProjectYearsView,
)

urlpatterns_projects = [
    path('', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/public/', PublicProjectListView.as_view(), name='public-project-list'),
    path('projects/years/', ProjectYearsView.as_view(), name='public-project-years'),
    path('<str:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<str:slug>/like/', ProjectLikeView.as_view(), name='project-like'),
    path('<str:slug>/unlike/', ProjectUnlikeView.as_view(), name='project-unlike'),
    path('<str:slug>/download/', ProjectDownloadView.as_view(), name='project-download'),
]

urlpatterns_admin = [
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:id>/', SkillRetrieveUpdateDestroyView.as_view(), name='skill-detail'),
    path('admin/projects/', AdminProjectListView.as_view(), name='admin-project-list'),
    path('admin/projects/<str:slug>/', AdminProjectDetailView.as_view(), name='admin-project-detail'),
    path('admin/projects/<str:slug>/status/', AdminProjectStatusView.as_view(), name='admin-project-status'),
]

urlpatterns_comment = [
    path('<int:project_id>/comments/', CommentListCreateView.as_view(), name='project-comments'),
    path('admin/comments/', AdminCommentListView.as_view(), name='admin-comment-list'),
    path('admin/comments/<int:pk>/', AdminCommentModerationView.as_view(), name='admin-comment-moderation'),
    path('comments/my-projects/', MyProjectCommentsView.as_view(), name='my-project-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

urlpatterns_dashboard = [
    path('dashboard/chart/', DashboardChartView.as_view(), name='dashboard-chart'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]

urlpatterns = [] + urlpatterns_admin + urlpatterns_comment + urlpatterns_dashboard + urlpatterns_projects