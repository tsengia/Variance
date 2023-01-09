# Variance React App
This directory holds the React Single Page Application for interacting with the Variance server.  


## Generating Open API Boilerplate
The `openapi-generator-cli` is included as a dependency in the `package.json`, so if you do an `npm install`, it will be downloaded for you.

First, you will need to generate the OpenAPI Specification file for Variance using Flask Smorest.  
In the toplevel directory of this repo, run the following command:  
```
FLASK_APP=variance.create_app
flask openapi write --format=json variance-openapi.json
```

Next, `cd` into the `variance-react` directory and generate the TypeScript boilerplate using the following command:
```
openapi-generator-cli generate -i ../variance-openapi.json -g typescript-axios -o generated
```
