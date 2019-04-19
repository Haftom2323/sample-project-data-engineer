#!/bin/sh

# the first argument to this script is the QUERY_DATE argument
# that the Lambda is looking for so that it knows the file naming
# convention for its UTF-8 encoded output files to the S3 bucket

QUERY_DATE=$1
aws lambda invoke --function-name SampleProjectFromCLI --log-type Tail \
--payload '{"query_date" : "'${QUERY_DATE}'"}' outputfile.txt

# clean up
#rm outputfile.txt