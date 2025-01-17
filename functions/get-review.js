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
      // Get Review
      if(params.dealerId){
          
          let selector = {"dealership": parseInt(params.dealerId)};
          
          let reviews = await cloudant.postFind({
              db: "reviews",
              selector: selector,
          });
          
          return {"body": reviews.result.docs}
      }
      else if (params.review){
      // Insert Review
        try {
          let review = await cloudant.postDocument({
            db: 'reviews',
            document: params.review
            });
            
            return {"body": params.review} ;
            
        } catch (error) {
          return { error: error.description };
        }
      }
      else{
          return {"body":""}
      }
  }
