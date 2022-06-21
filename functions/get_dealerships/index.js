/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let selector = (params.state) ? {st:params.state} : {}
        let output = await getStateSpecificDoc(cloudant,selector)
        if (output.length === 0) 
            return {
                statusCode:404,
                headers:{ 'Content-Type': 'text/plain'},
                body:"Database is empty"
            }

        return {
            statusCode:200,
            headers:{ 'Content-Type': 'application/json'},
            body: output
        }  
    } catch (error) {
        return {
            statusCode:500,
            headers:{ 'Content-Type': 'text/plain'},
            body:"Something went wrong on the server"
        }
    }
}

async function getAllDocs(cloudant) {
    let rows = (await cloudant.postAllDocs({db:'dealerships', includeDocs:true})).result.rows
    return rows.map(({doc}) => formatResponse(doc))
}

async function getStateSpecificDoc(cloudant, selector) {
    let rows = (await cloudant.postFind({db:'dealerships', selector})).result.docs
    return rows.map(formatResponse)
}

function formatResponse(doc) {
    return {
        id: doc.id,
        city: doc.city,
        state: doc.state,
        st: doc.st,
        address: doc.address,
        zip: doc.zip,
        lat: doc.lat,
        long: doc.long
    }
}

