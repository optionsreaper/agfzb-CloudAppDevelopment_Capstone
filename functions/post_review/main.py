#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests
import json


def main(dict):
    databaseName = "reviews" 
    
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])

        print(dict)
        body = json.loads(dict['__ow_body'])

        new_review = {
            "id":body['review']['id'],
            "name":body['review']['name'],
            "dealership":body['review']['dealership'],
            "review":body['review']['review'],
            "purchase":body['review']['purchase'],
            "purchase_date":body['review']['purchase_date'],
            "car_make":body['review']['car_make'],
            "car_model":body['review']['car_model'],
            "car_year":body['review']['car_year']
        }

        print(new_review)
        response = client.post_document(db='reviews', document=new_review).get_result()

        return {
            "statusCode":200,
            "headers":{ 'Content-Type': 'application/json'},
            "body": {"message":"Successfully added"}
        }

    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])

    except:
        return {
            "statusCode":500,
            "headers":{ 'Content-Type': 'application/json'},
            "body": {"message":"Something went wrong on the server"}
        }
