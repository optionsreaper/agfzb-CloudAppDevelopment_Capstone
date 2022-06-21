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


def main(dict):
    databaseName = "reviews" 
    
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])
        

        if "dealerId" in dict:
            response = client.post_find(
                db=databaseName,
                selector={"dealership":int(dict["dealerId"])}
            ).get_result()["docs"]

            if len(response) != 0:
                dealer_response = client.post_find(
                    db='dealerships',
                    selector={"id":int(dict["dealerId"])},
                    fields=['full_name']
                ).get_result()["docs"][0]["full_name"]
                final_response = {
                    "dealer_name": dealer_response,
                    "reviews": response
                }
                return {
                    "statusCode":200,
                    "headers":{ 'Content-Type': 'application/json'},
                    "body": final_response
                }

        return {
            "statusCode":404,
            "headers":{ 'Content-Type': 'text/plain'},
            "body": "dealerId does not exist"
        }

    except:
        return {
            "statusCode":500,
            "headers":{ 'Content-Type': 'text/plain'},
            "body": "Something went wrong on the server"
        }
