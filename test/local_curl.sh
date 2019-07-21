#!/bin/sh

curl -w "@test/curl-format.txt" -o /dev/null -s \
  --header "Content-Type: application/json" \
  --request POST  \
  -d @test/data.json \
  http://0.0.0.0:5900/api/shorten