/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'altaeb.eu', // the auth0 domain prefix
    audience: 'CoffeeShop', // the audience set for the auth0 app
    clientId: 'U1O4J6Nn7Njp1bkS5VmLkPiZ6yLo8hYD', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running React application. 
  }
};
