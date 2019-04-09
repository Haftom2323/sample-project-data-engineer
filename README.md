# Data Engineer sample project

## Instructions 

* Fork this repo
* Create an S3 bucket for storing the ETL output, with a `sample-project` folder
* In `sample-project`, create the following folders:
  * `extract`
  * `transform`
  * `load`
* Create a Python 3.7 ETL job 
  * Use the Pandas DataFrame library wherever appropriate.
* Create an end-to-end script that that takes a query date parameter in the format YYYY-MM-DD
  * The code for each phase should write output to the appropriate subfolder
     * For extract, for example: `sample-project/extract/$QUERY_DATE`
* Use the single responsibility principle to organize your code
   * Create a Python module corresponding to each phase of the job (Extract, Transform, Load).
   * Each module should have a clearly documented "public API" set of functions
   * The end-to-end script should import only those public API functions
   * Each module’s contract should be to read an input file and produce an output file usable by the module for next phase.
   * All output files should be UTF-8 encoded CSV files.
   * Files should be read from and written to S3.
* Extract
  * Create `s3://$BUCKET/sample-project/extract/$QUERY_DATE`
  * Write `sample-extract-output.csv` to `s3://$BUCKET/sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv`
* Transform 
  * Implement a function for each transform operation in the provided target spec.
  * Create a test for each transform operation using pytest.  
  * Once you have the transform functions tested, update the end-to-end script to:
    * Read `s3://$BUCKET/sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv` into memory
    * Run the transformations
    * Write the transform output to `s3://$BUCKET/sample-project/transform/$QUERY_DATE/${QUERY_DATE}-transform-output.csv`
* Load 
  * Update the end-to-end script to copy `s3://sample-project/extract/$QUERY_DATE/${QUERY_DATE}-transform-output.csv` to `s3://sample-project/load/$QUERY_DATE/${QUERY_DATE}.EMP.REC.LRF.csv`
* All tests for the project should be runnable from the project root-level via pytest.
* Use the AWS CLI to create an AWS Lambda that runs the job.
* Create a simple but clear and complete README that documents:
  * How to build and run the job locally
  * How to run tests
  * How to deploy the job to AWS as a Lambda
  
## Transform Spec

| Source Columns | Transformation | Target Column |
|----------------|----------------|---------------|
| full_name      | Split on space, reverse, uppercase last name, join with a comma | employee_name
| email          | Direct map | email_address 
| address        | Replace commas with spaces | home_address
  
## Building

TBD

## Running Locally

TBD

## Deploying to AWS Lambda

TBD
