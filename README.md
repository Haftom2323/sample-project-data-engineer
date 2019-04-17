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

* All source code is located in the `myetl` directory
  * Every function in the .py files within `myetl` contains docstrings so you can use help() to learn how they work
  * `scripts/lambda_function.py` is the run-script used for deployment to AWS. It takes the place of `scripts/call_cli_handler.py` for running the code locally.
    * Each run-script imports only the functions marked as `public API` in their docstrings. These functions are `extract.extract_function`, `transform.transform_function`, and `load.load_function`. The helper functions within transform are not imported by the run-scripts.
  * Build the package by typing `pip install -r requirements.txt` from the root directory to run `setup.py` and install to your local machine.

## Running Locally

* `scripts` contains an end-to-end run-script named `call_cli_handler.py`
  * typing `python3 call_cli_handler.py -h` will display a help message that describes the arguments needed such as QUERY_DATE which is passed in as `-d YYYY-MM-DD`. I've also provided options to point to a local directory to store temporary files and delete it when the Lambda completes.

## Testing with pytest

* From the root directory, type `pytest myetl`
  * It is necessary to pass `myetl` because of all the code stored in `lib` that's needed for deployment to AWS. Amazon linux compatible pandas, numpy, and pytz have a few files with 'test' in their names and/or functions; pytest tries to test them and it goes rather poorly.
  * Pytest will test the two helper functions in `myetl/transform.py` using `myetl/test_transform.py`
    * email to email_address is a direct mapping so no helper function was needed
  
## Deploying to AWS Lambda

* In `scripts` there are two shell scripts
  * `bundle.sh` zips up all necessary code and creates the Lambda using the AWS CLI
  * `invoke_lambda.sh` will invoke the Lambda provided the user passes it one CL arg - date in YYYY-MM-DD as follows `invoke_lambda.sh YYYY-MM-DD`
  * Go check out `s3://mybucket1219` to view the output
* UPDATE: code doesn't run in the Lambda anymore
  * `bundle.sh` uses `pip install -r ` to install all dependencies of `myetl` which unfortunately installs a bunch of Mac specific packages; these break on the Lambda. I reverted back to using `scripts/push2lambda.sh` but because AWS Lambda doesn't recognize `myetl` as a package, all import statements of the form `from myetl import ` break.
  * If you want to try my code in a Lambda, revert back to (any) prior commit in my repo and `push2lambda.sh` + `invoke_lambda.sh` will work.