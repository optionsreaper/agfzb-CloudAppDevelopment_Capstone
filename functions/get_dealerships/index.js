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
    let output = []
    if (params.state) {
        let selector = (params.state) ? {st:params.state} : {}
        output = await getStateSpecificDoc(cloudant,selector).catch(respondWithError)
        if (output.length === 0) 
            return {
                statusCode:404,
                headers:{ 'Content-Type': 'text/plain'},
                body:"The state does not exist"
            }
    } else {
        output = await getAllDocs(cloudant).catch(respondWithError)
        if (output.length === 0) 
            return {
                statusCode:404,
                headers:{ 'Content-Type': 'text/plain'},
                body:"Database is empty"
            }
    }

    return {
        statusCode:200,
        headers:{ 'Content-Type': 'application/json'},
        body: output
    }  
}

async function getAllDocs(cloudant) {
    let rows = (
        await cloudant.postAllDocs({db:'dealerships', includeDocs:true}).catch(respondWithError)
    ).result.rows
    return rows.map(({doc}) => formatResponse(doc))
}

async function getStateSpecificDoc(cloudant, selector) {
    let rows = (
        await cloudant.postFind({db:'dealerships', selector}).catch(respondWithError)
    ).result.docs
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
        long: doc.long,
        full_name: doc.full_name,
        short_name: doc.short_name
    }
}

function respondWithError() {
    return {
        statusCode:500,
        headers:{ 'Content-Type': 'text/plain'},
        body:"Something went wrong on the server"
    }
}