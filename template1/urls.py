from django.urls import path
from template1.views import (
    EnrollCourseView,
    EnrollSingleCourseView,
    LoginTemplateView,
    ProfileView,
    RegisterTemplateView,
    TransactionView,
    UserLoginView,
    UserRegisterView,
    UserLogoutView,
    DashboardView,
    ResultView,
)

urlpatterns = [
    path('user/login/', LoginTemplateView.as_view(), name='login'),
    path('user/login/submit/', UserLoginView.as_view(), name='login_submit'),

    path('user/register/', RegisterTemplateView.as_view(), name='register'),
    path('user/register/submit/', UserRegisterView.as_view(), name='register_submit'),

    path('user/logout/', UserLogoutView.as_view(), name='logout'),
    path('user/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('user/dashboard/transaction/',TransactionView.as_view(), name='transaction'),

    path('user/dashboard/profile/',ProfileView.as_view(), name='profile'),
    path('user/dashboard/result/',ResultView.as_view(), name='result'),
    path('user/dashboard/transaction/',TransactionView.as_view(), name='transaction'),
    path('user/dashboard/courses/enroll/', EnrollCourseView.as_view(), name='enroll_course'),
    path('user/dashboard/courses/single/<slug:slug>/', EnrollSingleCourseView.as_view(), name='enroll_course'),


]
