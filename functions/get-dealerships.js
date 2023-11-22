/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      
      // If state parameter is passed
      if(params.state){
          let selector = {
                "state": params.state
        }
        
        let dealerships = await cloudant.postFind({ db: "dealerships", selector:selector});
        return {"body" : dealerships.result.docs}
      }
      //if dealer ID is passed
      else if (params.dealerId){
          console.log(typeof params.dealerId);
          let dealerId = parseInt(params.dealerId);
          let selector = {
                "id": dealerId
        }
        
        let dealerships = await cloudant.postFind({ db: "dealerships", selector:selector});
        return {"body" : dealerships.result.docs}
          
      }
      else{
      // Return all dealerships
        try {
          let dealerships = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
            });
            return {"body": dealerships.result.rows} ;
        } catch (error) {
          return { error: error.description };
        }
      }
     
}
