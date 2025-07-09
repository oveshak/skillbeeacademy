from django.urls import path
from .views import AllcoursView, CourseDetailView, IndexView, OrderFormView,SuccessPageView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('allcourse/', AllcoursView.as_view(), name='allcourse'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('enroll/<slug:slug>/', OrderFormView.as_view(), name='enroll_form'),
    path("success/<int:purchase_id>/", SuccessPageView.as_view(), name="success_page"),
]