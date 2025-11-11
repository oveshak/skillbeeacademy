from django.db import models
from solo.models import SingletonModel
# Create your models here.
from django.utils.text import slugify
from globalapp.models import Common
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from users.models import Users
class CourseType(Common):
    type_name = models.CharField(max_length=200)
    def __str__(self):
        return self.type_name
    
class CourseLevel(Common):
    level_name = models.CharField(max_length=200)
    def __str__(self):
        return self.level_name
    

    
class CourseTopics(Common):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class CourseFaqs(Common):
    questions = models.CharField(max_length=200)
    answear = RichTextField()
    def __str__(self):
        return self.questions
    
class CoursePrerequisit(Common):
    title = models.CharField(max_length=200)
    icon = models.ImageField()
    def __str__(self):
        return self.title
    
class CourseAudience(Common):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
class InstallationStatus(Common):
    title = models.CharField(max_length=200)
    percentage = models.FloatField(default=0)
    def __str__(self):
        return self.title
 
class MCQQuestion(Common):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    right_answer = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ],
        help_text="Select the correct option letter (A/B/C/D)"
    )

    def __str__(self):
        return self.question[:80]

class CourseContents(Common):
    VIDEO = 'video'
    QUIZ = 'quiz'
    RESOURCES = 'resources'

    CONTENT_TYPE_CHOICES = [
        (VIDEO, 'Video'),
        (QUIZ, 'Quiz'),
        (RESOURCES, 'Resources'),
    ]

    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=True, blank=True)
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default=VIDEO,
    )
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    # If exam time is only for QUIZ, make it optional at DB level,
    # and validate in form/clean().
    examtime = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1)],
        help_text="Minutes (only required for quiz contents)"
    )
    preview = models.BooleanField(default=False)
    # `source` might not exist for QUIZ/RESOURCES; make it optional
    source = models.URLField()

    mcq = models.ManyToManyField(MCQQuestion, blank=True, related_name='course_contents')
    # default has no effect on M2M; remove it
    installment_status = models.ManyToManyField(InstallationStatus, blank=True)

    def __str__(self):
        return self.title

class CourseModules(Common):
    title = models.CharField(max_length=200)
    contents = models.ManyToManyField(CourseContents)
    def __str__(self):
        return self.title
    
class CourseMilestones(Common):
    title = models.CharField(max_length=200)
    modules = models.ManyToManyField(CourseModules)
    def __str__(self):
        return self.title





class Courses(Common):

    
    # Define course types as choices
    TEST_EXAM = 'test_exam'
    LIVE_COURSE = 'live_course'
    RECOURSE = 'recourse'
    FULL_COURSES = 'full_courses'

    COURSECONTENT_TYPE_CHOICES = [
        (TEST_EXAM, 'Test Exam'),
        (LIVE_COURSE, 'Live Course'),
        (RECOURSE, 'Recourse'),
        (FULL_COURSES, 'Full Courses'),
    ]
    course_content_type = models.CharField(
        max_length=15,
        choices=COURSECONTENT_TYPE_CHOICES,
        default=FULL_COURSES,
    )
    extra_description = RichTextField(default=None,null=True,blank=True)
    title = models.CharField(max_length=200)
    course_type = models.ForeignKey(CourseType,on_delete=models.CASCADE)
    course_level = models.ForeignKey(CourseLevel,on_delete=models.CASCADE)
    description = RichTextField(default=None,null=True,blank=True)
    student_amount = models.IntegerField(null=True,blank=True)
    course_thumbnail = models.ImageField()
    live_projects = models.IntegerField(null=True,blank=True)
    course_topics = models.ManyToManyField(CourseTopics)
    course_faqs = models.ManyToManyField(CourseFaqs)
    course_audiences = models.ManyToManyField(CourseAudience)
    prerequisites =models.ManyToManyField(CoursePrerequisit)
    intro_title = models.CharField(max_length=200)
    intro_video_url = models.URLField()
    total_students = models.IntegerField(null=True,blank=True)
    remaining_students = models.IntegerField(null=True,blank=True)
    price = models.FloatField()
    offer_price = models.FloatField()
    milestone_count = models.IntegerField()
    module_count = models.IntegerField()
    video_count = models.IntegerField()
    quiz_count = models.IntegerField()
    milestones = models.ManyToManyField(CourseMilestones)
    slug = models.SlugField(unique=True, blank=True,null=True)  # Add slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate slug from title
        super().save(*args, **kwargs) 
    def __str__(self):
        return self.title
    


###### Course Enroll and payment ##############

class PaymentMethods(Common):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    qr_image = models.ImageField(upload_to="qr/",null=True,blank=True)
    text = RichTextField(null=True,blank=True)
    logo = models.ImageField(upload_to="logo/",null=True,blank=True)
    def __str__(self):
        return self.name
    
class EnrollCourse(Common):
    Full = 'full'
    Installment = 'installment'

    PAYMENT_TYPE_CHOICES = [
        (Full, 'Full'),
        (Installment, 'Installment'),
    ]
    course_id = models.ForeignKey(Courses,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    payment_type = models.CharField(
        max_length=15,
        choices=PAYMENT_TYPE_CHOICES,
        default=Full,
    )
    amount = models.FloatField(blank=True,null=True)
    installation_status = models.ManyToManyField(InstallationStatus,blank=True)

    def __str__(self):
        return f"{self.course_id.title} enrolled by {self.user_id.email}"
    def save(self, *args, **kwargs):
        if EnrollCourse.objects.filter(course_id=self.course_id, user_id=self.user_id).exists():
            raise ValidationError({"message": "Course Already Purchased"})
        super(EnrollCourse, self).save(*args, **kwargs)
    
class Payment(Common):
    # Payment Status Choices
    PENDING = 'pending'
    CONFIRM = 'confirm'
    DUE = 'due'
    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRM, 'Confirm'),
        (DUE, 'Due'),
    ]
    Full = 'full'
    Installment = 'installment'
    payment_method = models.ForeignKey(PaymentMethods,on_delete=models.SET_NULL,null=True)
    PAYMENT_TYPE_CHOICES = [
        (Full, 'Full'),
        (Installment, 'Installment'),
    ]
    course_id = models.ForeignKey(Courses,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    payment_status = models.CharField(
        max_length=15,
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING,  # Default status is 'pending'
    )
    payment_type = models.CharField(
        max_length=15,
        choices=PAYMENT_TYPE_CHOICES,
        default=Full,
    )
    installation_status = models.ManyToManyField(InstallationStatus,blank=True)
    amount = models.FloatField()
    number= models.CharField(max_length=25)
    transaction_id = models.CharField(max_length=25,null=True,blank=True)

    def __str__(self):
        return self.user_id.email
class SSLcommerceSettings(SingletonModel):
    store_id= models.CharField(max_length=100)
    store_pass= models.CharField(max_length=100)
    active_status = models.BooleanField(default=True)
    sandbox_status = models.BooleanField(default=True)
    
