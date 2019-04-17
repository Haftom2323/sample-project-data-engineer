#!/bin/sh

# note that this script needs to be run from the scripts directory to
# zip up the end-to-end script and its local dependencies.
# I could have listed a machine specific absolute path for the first
# cd command but I wanted to give this a chance to work on yours without editing;
# therefore I went with relative paths assuming I only have root and below to work from.

# temporarily copy Amazon linux compatible libraries to the source code directory
# before zipping everything up. When I don't do this, the libraries wind up in their own
# folder in the zip archive which doesn't work well when uploaded to a Lambda. 
libs="numpy pandas pytz"
cd ../lib
cp -r ${libs} ../myetl

# create the zip file of source code for my Lambda
cd ../myetl
cp ../scripts/lambda_function.py .
zip -r SampleProject.zip lambda_function.py __init__.py \
transform.py load.py extract.py ${libs}

# create lambda function: SampleProjectFromCLI
# I played with the timeout and memory-size parameters a bit and
# think what I've gone with is close to optimal
aws lambda create-function --function-name "SampleProjectFromCLI" --runtime "python3.7" \
--role "arn:aws:iam::929207060866:role/lambda-cli-role" \
--handler "lambda_function.lambda_handler" --timeout 30 --memory-size 256 \
--zip-file "fileb://SampleProject.zip"

# clean up: no need for the zip once the Lambda exists, ditto for copied libraries
rm SampleProject.zip lambda_function.py
rm -r ${libs}

# return to run directory
cd ../scripts