#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests


def main(dict):
    databaseName = "reviews" 
    
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])
        
        new_review = Document(
            id=str(dict['review']['id']),
            name=dict['review']['name'],
            dealership=dict['review']['dealership'],
            review=dict['review']['review'],
            purchase=dict['review']['purchase'],
            another=dict['review']['another'],
            purchase_date=dict['review']['purchase_date'],
            car_make=dict['review']['car_make'],
            car_model=dict['review']['car_model'],
            car_year=dict['review']['car_year']
        )

        response = client.post_document(db='reviews', document=new_review).get_result()

        return {
            "statusCode":200,
            "headers":{ 'Content-Type': 'application/json'},
            "body": "Successfully added"
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
            "headers":{ 'Content-Type': 'text/plain'},
            "body": "Something went wrong on the server"
        }
