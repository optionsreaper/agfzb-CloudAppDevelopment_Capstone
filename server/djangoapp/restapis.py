import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
import urllib.parse


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'apikey' in kwargs:
            print('auth')
        #     # Basic authentication GET   
            response = request.get(url, headers={'Content-Type': 'application/json'},
                params=kwargs, auth=HTTPBasicAuth('apikey', kwargs['api_key']))
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
        reviews = json_result#["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review#["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = CarDealer(
                dealership=review_doc['dealership'],
                name=review_doc['name'],
                purchase=review_doc['purchase'],
                review=review_doc['review'],
                id=review_doc['id']
            )
            if (review_obj.purchase):
                review_obj.purchase_date=review_doc['purchase_date']
                review_obj.car_make=review_doc['car_make']
                review_obj.car_model=review_doc['car_model']
                review_obj.car_year=review_doc['car_year']

            # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    # params = dict()
    # params["text"] = kwargs["text"]
    # params["version"] = kwargs["version"]
    # params["features"] = kwargs["features"]
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = get_request(
        "url/v1/analyze",
        {
            "api_key": "api",
            "version": "2022-04-07",
            "text": urllib.parse.quote(text),
            "features": ["sentiment"]
        }
    )
    return response
    # response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
    #                                 auth=HTTPBasicAuth('apikey', api_key))


