from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)

# Create a `contact` view to return a static contact page
def get_review(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/add_review.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')

        else:
            # If not, return to login page again
            return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name ,password=password)
            login(request, user)
            return redirect('djangoapp:index')

        else:
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/8d4b882f-3997-4997-bd2c-d98f5cf74667/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8d4b882f-3997-4997-bd2c-d98f5cf74667/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"] = reviews
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8d4b882f-3997-4997-bd2c-d98f5cf74667/api/dealership"
        dealer = get_dealers_from_cf(dealer_url, dealerId=dealer_id)
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method =="GET":
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8d4b882f-3997-4997-bd2c-d98f5cf74667/api/dealership"
        dealer = get_dealers_from_cf(dealer_url, dealerId=dealer_id)
        context["dealer"] = dealer
        cars = CarModel.objects.filter(dealerId=dealer_id)
        print(cars)
        context["cars"] = cars        
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        print("POST add_review")

        response = ""
        json_payload={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/8d4b882f-3997-4997-bd2c-d98f5cf74667/api/post-review"

        if request.method == "POST":
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.POST['name']
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase"] = False
            review["purchase_date"] = request.POST['purchasedate']
            review["car_make"] = review_car.make.name
            review["car_model"] = review_car.name
            review["car_year"] = review_car.year.strftime("%Y")
            json_payload["review"] = review
            response = post_request(url, json_payload=json_payload)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)




