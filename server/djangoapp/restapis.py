import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import urllib.parse
import os


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'apikey' in kwargs:
            # Basic authentication GET   
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', kwargs['apikey']))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(f"body {json_payload}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Failed")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
    


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer#["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review#["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review_doc['dealership'],
                name=review_doc['name'],
                purchase=review_doc['purchase'],
                review=review_doc['review'],
                id=review_doc['id']
            )
            if 'car_make' in review_doc:
                review_obj.car_make=review_doc['car_make']
            if 'car_model' in review_doc:
                review_obj.car_model=review_doc['car_model']
            if 'car_year' in review_doc:
                review_obj.car_year=review_doc['car_year']
            if 'purchase_date' in review_doc:
                review_obj.purchase_date=review_doc['purchase_date']
                
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
            results.append(review_obj)
        return {
            "dealer_name": json_result["dealer_name"],
            "reviews": results
        }
    return {
        "dealer_name": "Not Found",
        "reviews": results
    }
    


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    response = get_request(
        f"{os.getenv('NLU_URL')}/v1/analyze",
        apikey=os.getenv('NLU_API_KEY'),
        version="2022-04-07",
        text=urllib.parse.quote(text),
        features="sentiment"
    )
    print(response['sentiment']['document']['label'])
    return response['sentiment']['document']['label']