from django.urls import path
from rest_framework.routers import DefaultRouter,SimpleRouter
from . import views





urlpatterns = [
    
# path('admin/article/preview/<int:article_id>/', views.article_preview, name='article_preview'),
# path("success/", views.SuccessView.as_view(), name="success_page"),
# path('', views.DynamicFormView.as_view(), name='dynamic_purchase_view'),
path('enroll/', views.OrderFormView.as_view(), name='order_form'),
path("success/<int:purchase_id>/", views.SuccessPageView.as_view(), name="success_page"),
path("login/", views.LoginView.as_view(), name="login"),
path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
path("orders/", views.OrdersView.as_view(), name="orders"),
path("logout/", views.LogoutView.as_view(), name="logout"),
path("error/", views.CustomErrorPageView.as_view(), name="error_page"),
path('theme/<int:page_id>/', views.ThemeTemplateView.as_view(), name='theme_view'),
path("", views.IndexView.as_view(), name="index"),
]
