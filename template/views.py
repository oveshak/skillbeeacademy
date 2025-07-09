from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from cms.models import Banner
from landingpage.models import BkashConfiguration, ExtraCharges, Product, Purchase
from landingpage.views import hash_data
from lmsfeatures.models import Courses


from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from globalapp.models import SoftwareAsset
# from .models import BkashConfiguration, BkashSettings, ExtraCharges, Templates, Theme
import requests
from django.shortcuts import render
# from .models import Product
# from .forms import PurchaseForm
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
# from .models import Product, ExtraCharges, Purchase
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .models import Product, ExtraCharges, Purchase, Templates
import json
import requests
from django.views import View
#test code
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db import transaction
# from .models import Product, ExtraCharges, Purchase
import requests
from django.urls import reverse
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.contrib.auth import authenticate, login
from django.contrib import messages
import time
import uuid


FACEBOOK_PIXEL_ID = '24064524669838168'
FACEBOOK_ACCESS_TOKEN = "EAAN1sTGQn7YBO1PD8qA0ehP8J1tdyH1Ap3zdp9XEBnVOIa7g8didOnCMgNlZCGyiBkSSKCNMjnkz5p7CO5fxvCmNSpWLuu2VUahrZC3WRZAngsiZAj24kj8awLF08Ah85st3jFoAWqjQteUaX3m5UL1hvavIJOWhknB9msKWENpgYAZBwZA4k5fAziZC9KskIFuKgZDZD"


class IndexView(TemplateView):
    template_name = "template/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_banner = Banner.objects.prefetch_related('items').first()
        context['banner'] = first_banner
        context['courses']=Courses.objects.all()
        return context
    
class AllcoursView(TemplateView):
    template_name = "template/allcourse.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_banner = Banner.objects.prefetch_related('items').first()
        context['courses']=Courses.objects.all()
        return context
    
class CourseDetailView(TemplateView):
    template_name = "template/single2.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        course = get_object_or_404(Courses, slug=slug)

        context["course"] = course
        context["topics"] = course.course_topics.all()
        context["faqs"] = course.course_faqs.all()
        context["audiences"] = course.course_audiences.all()
        context["prerequisites"] = course.prerequisites.all()
        context["milestones"] = course.milestones.all()
        # Extract tracking parameters
        last_purchase = Purchase.objects.last()
        purchase_id = last_purchase.id if last_purchase else None
        conversion_api(last_purchase, f"Page View - {slug}", browser_id=None, click_id=None)
        return context
    

class OrderFormView(TemplateView):
    template_name = "template/base3.html"

    # Load bKash Configuration
    bkash = BkashConfiguration.objects.get(pk=1)
    BKASH_BASE_URL = (
        "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout"
        if bkash.sandbox
        else "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout"
    )
    
    BKASH_APP_KEY = bkash.app_key
    BKASH_APP_SECRET = bkash.app_secret
    BKASH_USERNAME = bkash.username
    BKASH_PASS = bkash.password

    def get_bkash_token(self):
        """
        Retrieve the bKash token.
        """
        url = f"{self.BKASH_BASE_URL}/token/grant"
        headers = {
            "accept": "application/json",
            "username": self.BKASH_USERNAME,
            "password": self.BKASH_PASS,
            "content-type": "application/json"
        }
        data = {
            "app_key": self.BKASH_APP_KEY,
            "app_secret": self.BKASH_APP_SECRET,
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print("bKash Token Response:", response_data)

        if response.status_code == 200:
            return response_data.get("id_token")
        raise Exception("Failed to authenticate with bKash")

    def create_bkash_payment(self, amount, merchant_invoice):
        """
        Create a bKash payment request.
        """
        url = f"{self.BKASH_BASE_URL}/create"
        headers = {
            "accept": "application/json",
            "Authorization": self.get_bkash_token(),
            "X-APP-Key": self.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }
        data = {
            "mode": "0011",
            "callbackURL": "https://skillbeeacademy.com/enroll/japanese-language-course/",
            "amount": str(amount),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": merchant_invoice,
            "payerReference": "Skill Bee"
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print("bKash Create Payment Response:", response_data)

        if response.status_code == 200 and response_data.get("statusCode") == "0000":
            return response_data.get("bkashURL"), response_data.get("paymentID")
        return None, None

    def execute_bkash_payment(self, payment_id):
        print("Function hit")
        """
        Execute the bKash payment to finalize the transaction.
        """
        url = f"{self.BKASH_BASE_URL}/execute"
        headers = {
            "accept": "application/json",
            "Authorization": self.get_bkash_token(),
            "X-APP-Key": self.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }
        data = {"paymentID": payment_id}

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print("bKash Execute Payment Response:", response_data)

        if response.status_code == 200 and response_data.get("transactionStatus") == "Completed":
            return "Completed"
        return "Failed"

    def get(self, request, *args, **kwargs):
        """
        Handle the GET request for payment confirmation.
        """
        # Extract tracking parameters
        browser_id = request.COOKIES.get("_fbp") or None  # Facebook Browser ID
        click_id = request.GET.get("fbclid") or None  # Facebook Click ID (if coming from an ad)

        status = request.GET.get("status")
        payment_id = request.GET.get("paymentID")  # Get paymentID from bKash
        last_purchase = Purchase.objects.last()
        purchase_id = last_purchase.id if last_purchase else None
        conversion_api(last_purchase, "Initiate Checkout", browser_id, click_id)
        if status == "success" and purchase_id and payment_id:
            execute_status = self.execute_bkash_payment(payment_id)  # Call execute API
            print(execute_status)
            if execute_status == "Completed":
                conversion_api(last_purchase, "Purchase", browser_id, click_id)
                return redirect(reverse("success_page", kwargs={"purchase_id": purchase_id}))
            else:
                return redirect("error_page")  # Handle failed execution

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        extra_charges = ExtraCharges.objects.all()
        slug = self.kwargs.get("slug")
        # theme_id = SystemSettings.objects.get(pk=1).theme
        
        # theme = Theme.objects.get(pk=theme_id.id)
        total_price = sum(product.price * product.quantity for product in products)
        extra_charges_total = sum(charge.amount for charge in extra_charges)
        grand_total = total_price + extra_charges_total
        pay_status = ExtraCharges.objects.filter(advance_payable=True).exists()
        print(pay_status)
        context.update({
            "products": products,
            "extra_charges": extra_charges,
            "total_price": total_price,
            "extra_charges_total": extra_charges_total,
            "grand_total": grand_total,
            "pay_status": pay_status,
            "slug":slug,
            
        })
        # Add the theme data to context
        # context['theme'] = theme
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for order submission.
        """
        # Retrieve form data
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        selected_extra_charges = request.POST.getlist("extra_charges")
        payment_method = request.POST.get("payment_method")
        email = request.POST.get("email")
        selected_product_id = request.POST.get('selected_product')
        print(selected_product_id)
        print("Payment Method:", payment_method)

        # Fetch products and extra charges
        products = Product.objects.filter(pk=selected_product_id)
        extra_charges = ExtraCharges.objects.filter(id__in=selected_extra_charges)

        # Calculate totals
        total_price = sum(product.price * product.quantity for product in products)
        extra_charges_total = sum(charge.amount for charge in extra_charges)
        grand_total = total_price + extra_charges_total

        # Save to Purchase model
        with transaction.atomic():
            purchase = Purchase.objects.create(
                name=name,
                address=address,
                phone_number=phone_number,
                email = email,
                total_amount=grand_total,
            )
            purchase.products.set(products)
            purchase.extra_charges.set(extra_charges)
            purchase.save()

        conversion_api(purchase, "Initiate Checkout")
        

        # Handle payment method
        if payment_method in ["advance_delivery_charge", "advance_full_payment"]:
            merchant_invoice = f"INV-{purchase.id}-{phone_number}"
            payment_amount = extra_charges_total if payment_method == "advance_delivery_charge" else grand_total
            bkash_url, payment_id = self.create_bkash_payment(payment_amount, merchant_invoice)
            purchase.payment_id = payment_id
            purchase.amount_paid = payment_amount
            purchase.save()
            

            if bkash_url and payment_id:
                request.session["purchase_id"] = purchase.id
                request.session["payment_id"] = payment_id  # Store payment ID for execution

                return redirect(bkash_url)

            return redirect("error_page")  # Handle bKash payment failure
        else:
            # Cash on Delivery
            purchase.payment_status = "PENDING"
            purchase.save()
            return redirect(reverse("success_page", kwargs={"purchase_id": purchase.id}))
        
class SuccessPageView(View):
    template_name = "template/success.html"

    def get(self, request, purchase_id):
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase.payment_status = "PURCHASE"
        purchase.save()
        conversion_api(purchase, "Purchase")
        context = {
            "purchase": purchase,
            "products": purchase.products.all(),
            "extra_charges": purchase.extra_charges.all(),
        }
        return render(request, self.template_name, context)
def conversion_api(purchase, name, browser_id=None, click_id=None, event_source_url=None, test_event_code=None):
    """
    Sends conversion event data to Facebook Conversion API.

    Args:
        purchase (object): Purchase object with attributes `name`, `email`, `phone_number`, `total_amount`, etc.
        name (str): Event name (e.g., 'Purchase', 'Lead').
        browser_id (str, optional): Facebook browser ID (fbp).
        click_id (str, optional): Facebook click ID (fbc).
        event_source_url (str, optional): Source URL (default is Vitasoft Solutions' website).
        test_event_code (str, optional): Test event code for debugging.

    Returns:
        dict: Facebook API response.
    """
    
    # Default event source URL
    event_source_url = event_source_url or "https://skillbeeacademy.com/"

    # Extract first name and last name from `purchase.name`
    first_name, last_name = "", ""
    if purchase.name:
        name_parts = purchase.name.strip().split(" ", 1)  # Split at first space
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

    # Construct user_data with proper handling of empty values
    user_data = {
        "fn": [hash_data(first_name)] if first_name else [],
        "ln": [hash_data(last_name)] if last_name else [],
        "em": [hash_data("example@gmail.com")],
        "ph": [hash_data(purchase.phone_number)] if purchase.phone_number else [],
        "fbp": browser_id or "",  
        "fbc": click_id or "",   
    }

    # Remove empty fields from user_data
    user_data = {key: value for key, value in user_data.items() if value}

    payload = {
        "data": [
            {
                "event_name": name,
                "event_time": int(time.time()),
                "event_id": str(uuid.uuid4()),
                "action_source": "website",
                "event_source_url": event_source_url,
                "user_data": user_data,
                "custom_data": {
                    "currency": "BDT",
                    "value": str(float(purchase.total_amount)) if purchase.total_amount else "0",
                    "purchase_id": str(purchase.order_id) if hasattr(purchase, "purchase_id") else "unknown_order",
                    "content_type": "product",
                    "content_ids": [str(purchase.product_id)] if hasattr(purchase, "product_id") else ["1"]
                }
            }
        ]
    }

    # Add test event code if provided
    if test_event_code:
        payload["test_event_code"] = test_event_code

    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PIXEL_ID}/events"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, params={"access_token": FACEBOOK_ACCESS_TOKEN})
        return response.json()  # Return response for debugging
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@csrf_exempt
def facebook_conversion_api(request):
    print("data hited")
    if request.method == "GET":  # Allow GET requests for testing
        # data = json.loads(request.body)
        payload = {
            "data": [
                {
                "action_source": "website",
                "event_id": 12345,
                "event_name": "TestEvent",
                "event_time": 1738419388,
                "user_data": {
                    "client_ip_address": "254.254.254.254",
                    "client_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
                    "em": "f660ab912ec121d1b1e928a0bb4bc61b15f5ad44d5efdc4e1c92a25e99b8e44a"
                }
                }
            ],
            "test_event_code": "TEST87806"
            }

        url = f"https://graph.facebook.com/v22.0/{FACEBOOK_PIXEL_ID}/events"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, params={"access_token": FACEBOOK_ACCESS_TOKEN})

        return JsonResponse(response.json(), safe=False)

    elif request.method == "POST":  # For actual event submission
        data = json.loads(request.body)
        payload = {
            "data": [{
                "event_name": data.get("event_name", "Purchase"),
                "event_time": data.get("event_time"),
                "action_source": "website",
                "event_source_url": request.build_absolute_uri(),
                "user_data": {
                    "em": [data.get("email_hash")],  # Hashed email
                    "ph": [data.get("phone_hash")],  # Hashed phone
                },
                "custom_data": {
                    "currency": "BDT",
                    "value": data.get("amount"),
                },
                "test_event_code": "TEST70246"  # Facebook Test Event Code
            }]
        }

        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PIXEL_ID}/events"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, params={"access_token": FACEBOOK_ACCESS_TOKEN})

        return JsonResponse(response.json(), safe=False)