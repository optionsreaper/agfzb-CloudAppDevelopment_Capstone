from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

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
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to index view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
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
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://service.us-east.apiconnect.ibmcloud.com/gws/apigateway/api/b73938815ec4d43668ee02ab0fcc2c453c1bda76461a933f88ec0e85eb036e0b/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context = {
            "dealership_list":dealerships
        }
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://service.us-east.apiconnect.ibmcloud.com/gws/apigateway/api/b73938815ec4d43668ee02ab0fcc2c453c1bda76461a933f88ec0e85eb036e0b/api/review"
        dealer_details = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "dealer_id": dealer_id,
            "dealer_details":dealer_details
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        cars = get_list_or_404(CarModel, dealer_id=dealer_id)
        url = "https://service.us-east.apiconnect.ibmcloud.com/gws/apigateway/api/b73938815ec4d43668ee02ab0fcc2c453c1bda76461a933f88ec0e85eb036e0b/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        selected_dealer = [d for d in dealerships if d.id in [dealer_id]][0]
        context = {
            "dealer_id": dealer_id,
            "dealer_name": selected_dealer.full_name,
            "cars":cars
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}
            review['id'] = 12345
            review['name'] = f"{request.user.first_name} {request.user.last_name}"
            review['dealership'] = dealer_id
            review['review'] = "This review is the best one out there!"
            review['purchase'] = False
            review['purchase_date'] = '01/01/2022'
            review['car_make'] = "Ford"
            review['car_model'] = "Focus"
            review['car_year'] = 2022

            response = post_request(
                "https://service.us-east.apiconnect.ibmcloud.com/gws/apigateway/api/b73938815ec4d43668ee02ab0fcc2c453c1bda76461a933f88ec0e85eb036e0b/api/review",
                json_payload=json.dumps({"review":review}),
                dealerId=dealer_id
            )
            print(response)
            return HttpResponse(response['message'])
            
        else:
            return HttpResponse("You must be logged in")

    
def filter_dealerships_by_id(dealership, dealer_id):
    return dealer_id in dealership['id']
