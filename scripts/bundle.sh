#!/usr/bin/env bash

set -e

# define the directory where bundle.sh is housed; move up one directory and
# capture the ROOT_DIR with the pwd command
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${SCRIPT_DIR}"/..
ROOT_DIR=`pwd`

echo "ROOT_DIR=${ROOT_DIR}"
BUILD_DIR=$(mktemp -d)

# install myetl
pip install -r "${ROOT_DIR}/requirements.txt" --target $BUILD_DIR
cp -R "${ROOT_DIR}"/myetl $BUILD_DIR

# copy lambda_function.py from scripts to appease the AWS lambda handler
cp "${ROOT_DIR}"/scripts/lambda_function.py $BUILD_DIR

# The dependencies installed by pip are for OS X, however, AWS Lambda functions
# run on an Amazon Linux system. Copy over Linux specific pandas, numpy, pytz to
# the build dir for packaging into the myetl-lambda-function.zip file.
cp -r "${ROOT_DIR}"/lib/numpy $BUILD_DIR
cp -r "${ROOT_DIR}"/lib/pandas $BUILD_DIR
cp -r "${ROOT_DIR}"/lib/pytz $BUILD_DIR

# remove prior version of zip file
mkdir -p "${ROOT_DIR}"/dist
rm -f "${ROOT_DIR}"/dist/myetl-lambda-function.zip

# Clean Python intermediates.
find $BUILD_DIR -name '*.pyc' -delete
find $BUILD_DIR -name '__pycache__' -delete
find $BUILD_DIR -name '.pytest_cache' -delete

# zip up myetl + dependencies and place in dist; delete the temporary build directory
cd $BUILD_DIR && zip -r9 "${ROOT_DIR}"/dist/myetl-lambda-function.zip .
rm -rf $BUILD_DIR

echo "Created file: dist/myetl-lambda-function.zip"