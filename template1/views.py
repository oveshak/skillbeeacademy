from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Users  # Your custom user model
from lmsfeatures.models import Courses, EnrollCourse
from django.shortcuts import get_object_or_404
class LoginTemplateView(TemplateView):
    template_name = 'template1/login.html'


class RegisterTemplateView(TemplateView):
    template_name = 'template1/register.html'


class UserLoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

class UserRegisterView(View):
    def post(self, request):
        # Collect the data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
       
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')  # Stay on the same page with the error message

        # Check if the email or username already exists
        if Users.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

      

        # Create the user
        try:
            user = Users.objects.create_user(email=email, password=password)
            user.name = name
            user.phone_number = phone_number
            user.save()

            # Success message
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register')
        
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'template1/dashboard.html'
    login_url = 'login'



class EnrollCourseView(LoginRequiredMixin, TemplateView):
    template_name = 'template1/enrollCourse.html'
    login_url = 'login'  # Redirect to login page if not authenticated
    
    def get_context_data(self, **kwargs):
        """
        Add the enrolled courses of the current user (filtered by email) to the context data.
        """
        context = super().get_context_data(**kwargs)
        
        # Get the current user
        user = self.request.user
        
        # Fetch all the courses the user is enrolled in, filtered by email
        enrolled_courses = EnrollCourse.objects.filter(user_id__email=user.email)
        
        # Serialize the courses data
        
        print(context)
        context['enrolled_courses'] = enrolled_courses
        return context
    
class EnrollSingleCourseView(LoginRequiredMixin, TemplateView):
    template_name = 'template1/singleCourse.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        user = self.request.user
        context['enrolled_courses'] =EnrollCourse.objects.filter(user_id__email=user.email,course_id__slug=slug)
        # Get course with all related objects pre-fetched for performance
        course = get_object_or_404(
            Courses.objects.prefetch_related(
                'milestones',
                'milestones__modules',
                'milestones__modules__contents'
            ), 
            slug=slug
        )
        
        # Count the completed lessons (you might need to adjust this based on your user progress tracking)
        completed_lessons_count = 0  # This should be from user progress
        total_lessons = sum(
            module.contents.count() 
            for milestone in course.milestones.all() 
            for module in milestone.modules.all()
        )
        
        context['course'] = course
        context['completed_lessons_count'] = completed_lessons_count
        context['total_lessons'] = total_lessons
        context['progress_percentage'] = (completed_lessons_count / total_lessons * 100) if total_lessons > 0 else 0
        
        return context
    # def _convert_to_embed_url(self, url):
    #     if 'watch?v=' in url:
    #         return url.replace('watch?v=', 'embed/')
    #     elif 'youtu.be/' in url:
    #         video_id = url.split('youtu.be/')[-1]
    #         return f'https://www.youtube.com/embed/{video_id}'
    #     elif 'youtube.com/shorts/' in url:
    #         video_id = url.split('/shorts/')[-1]
    #         return f'https://www.youtube.com/embed/{video_id}'
    #     return url
