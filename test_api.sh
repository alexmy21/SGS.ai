#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing connection..."
curl -X GET "$BASE_URL/" -H "Content-Type: application/json" -w "\nStatus: %{http_code}\n\n"

echo "Testing HDF5 processor..."
curl -X POST "$BASE_URL/process" \
     -H "Content-Type: application/json" \
     -d '{"transformer":"C","processor":"meta_hdf5.call_hdf5","input_sha_id":"input_sha_id_123","processor_sha_id":"processor_sha_id_456","output_sha_id":"output_sha_id_789"}' \
     -w "\nStatus: %{http_code}\n\n"

echo "Testing Redis processor..."
curl -X POST "$BASE_URL/process" \
     -H "Content-Type: application/json" \
     -d '{"transformer":"C","processor":"meta_redis.ping_redis","input_sha_id":"input_sha_id_123","processor_sha_id":"processor_sha_id_456","output_sha_id":"output_sha_id_789"}' \
     -w "\nStatus: %{http_code}\n"