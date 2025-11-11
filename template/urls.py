from django.urls import path
from .views import AllcoursView, CourseDetailView, DownloadresourcesView, FreeeventView, FreetestView, IndexView, LivecoursView, OrderFormView, ResourseCourseDetailView, SingleTestView,SuccessPageView, TestCourseDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('allcourse/', AllcoursView.as_view(), name='allcourse'),
    path('livecourse/', LivecoursView.as_view(), name='livecourse'),
    path('freetest/', FreetestView.as_view(), name='freetest'),
    path('downloadresources/', DownloadresourcesView.as_view(), name='downloadresources'),
    path('freeevent/',FreeeventView.as_view(), name='freeevent'),
    path('testcourse/<slug:slug>/', TestCourseDetailView.as_view(), name='testcourse_detail'),
    path('resoursecourse/<slug:slug>/', ResourseCourseDetailView.as_view(), name='resoursecoursecourse_detail'),
    path('singletest/',SingleTestView.as_view(), name='singletest'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('enroll/<slug:slug>/', OrderFormView.as_view(), name='enroll_form'),
    path("success/<int:purchase_id>/", SuccessPageView.as_view(), name="success_page"),
]