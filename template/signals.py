from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from landingpage.models import Purchase
from lmsfeatures.models import EnrollCourse
from users.models import Users  # change if you're using a custom User model


@receiver(post_save, sender=Purchase)
def create_user_from_purchase(sender, instance, created, **kwargs):
    if created and instance.email and instance.phone_number:
        if not Users.objects.filter(username=instance.email).exists():
            Users.objects.create_user(
                email=instance.email,
                password=instance.phone_number
            )


@receiver(post_save, sender=Purchase)
def handle_purchase_save(sender, instance, created, **kwargs):
    email = instance.email
    phone = instance.phone_number

    # Step 1: Create user if doesn't exist
    if email and phone:
        user, user_created = Users.objects.get_or_create(
            email=email,
            defaults={'password': phone}
        )
        if user_created:
            user.set_password(phone)
            user.save()

    # Step 2: Enroll course if payment_status is "PURCHASE"
    if instance.payment_status == 'PURCHASE' and instance.products.exists():
        course = instance.products.first().course  # Assuming product is your course
        try:
            EnrollCourse.objects.create(
                course_id=course,
                user_id=user,
                payment_type=EnrollCourse.Full,
                amount=float(instance.amount)
            )
        except ValidationError:
            pass  # Course already enrolled; you can log or notify here