#!/bin/sh

aws lambda invoke --function-name SampleProject --log-type Tail outputfile.txt