#!/bin/sh

# zip up the end-to-end script and its local dependencies
zip -r SampleProject.zip lambda_function.py Transform.py Load.py Extract.py numpy pandas pytz

# upload to lambda function: SampleProject
#aws lambda update-function-code --function-name SampleProject --zip-file fileb://SampleProject.zip
aws lambda create-function --function-name "SampleProjectFromCLI" --runtime "python3.7" --role "arn:aws:iam::929207060866:role/lambda-cli-role" --handler "lambda_function.lambda_handler" --timeout 30 --memory-size 256 --zip-file "fileb://SampleProject.zip"
