import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    if "api_key" in kwargs:
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                            auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
            json_data = json.loads(response.text)
            return json_data
        except Exception as error:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
        # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
            json_data = json.loads(response.text)
            return json_data
        except:
            # If any error occurs
            print("Network exception occurred")

def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    if len(kwargs) > 0:
        if "dealerId" in kwargs :
            json_result = get_request(url, dealerId=kwargs["dealerId"])
        elif "state" in kwargs :
            json_result = get_request(url, state=kwargs["state"])

        if json_result:
            # For each dealer object
            for dealer in json_result:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"],
                                    st=dealer["st"], state= dealer["state"], zip=dealer["zip"])
            # Returning a single CarDealer Object
            return dealer_obj   

    else:
        # Call get_request with a URL parameter
        json_result = get_request(url)
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], state= dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
        return results

def get_dealer_reviews_from_cf(url, dealerId):
    reviews = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # For each review object
        for review in json_result:
            review_obj = DealerReview(id=review["id"], dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"], 
                                car_model=review["car_model"], car_year=review["car_year"], sentiment="")
            review_obj.sentiment = analyze_review_statements(review["review"])
            reviews.append(review_obj)
    return reviews

def analyze_review_statements(review_text):

    API_KEY = "Snn2o9a2LBWoNgFHFFLHjb6MS-tkskIrX-9onDmE2mfd"
    NLU_URL = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/339c2dc5-f671-4511-9e5d-18ec888ca73b"
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)

    natural_language_understanding.set_service_url(NLU_URL)

    response = natural_language_understanding.analyze(text=review_text, features=Features(
        sentiment=SentimentOptions(targets=[review_text])), language="en").get_result()

    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)
