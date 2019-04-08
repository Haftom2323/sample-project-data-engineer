# Data Engineer sample project

## Instructions 

* Fork this repo
* Create an S3 bucket for storing the ETL output
* Create a Python 3.7 ETL job.
  * Use the Pandas DataFrame library wherever appropriate.
* Use the single responsibility principle to organize your code
   * Create a Python module corresponding to each phase of the job (Extract, Transform, Load).
   * Each module’s contract should be to read an input file and produce an output file usable by the module for next phase.
   * All output files should be UTF-8 encoded CSV files.
   * Files should be read from and written to S3.
* To keep things simple, focus on the Transform and Load modules (don't worry about the Extract module)
   * Use the provided `sample-extract-output.csv` as a stand-in for the Extract module
* Implement the Transform module per the provided target spec.
* Write a test for each transform operation using pytest.  All tests for the project should be runnable from the project root-level via pytest.
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
