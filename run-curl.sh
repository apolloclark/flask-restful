#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
# To echo out all of the commnds used, use: set -euxo pipefail


# Test the CRUD abilities of the API
export SITE_URL="http://127.0.0.1:5001/datastore"

# reset database
echo "[INFO] Resetting the database without any data."
docker compose exec web python cli.py reset_db

echo "[INFO] 1. Verifying root URL."
curl --silent "${SITE_URL}" | jq '.hello'

# read all available data, with and without an ending slash
# this should return an HTTP 404 and a JSON error message
echo "[INFO] 2. Verifying error responses, with an empty database, without a slash."
curl --silent "${SITE_URL}" | jq '.message'

echo "[INFO] 3. Verifying error responses, with an empty database, with a slash."
curl --silent "${SITE_URL}/" | jq '.message'

# seed the database
echo "[INFO] Seeding the database with test data."
docker compose exec web python cli.py seed_db

# generic error read on an non-existent entry
echo "[INFO] 4. Verifying error response for missing entity."
curl --silent "${SITE_URL}/999" | jq '.message'

echo "[INFO] 5. Verifying response for reading existing data, with a slash."
curl --silent "${SITE_URL}/" | jq '.[0].email' | grep 'apolloclark@gmail.com'



# create new data
echo "[INFO] 6. Verifying response for creating new data."
curl --silent --request POST \
  --header 'Content-Type: application/json' \
  --data-raw '
{
  "email":"alex.murphy@gmail.com",
  "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a303",
  "bool":"false",
  "datetime":"2023-07-25T16:57:36.908339"
}
' \
    "${SITE_URL}" \
     | jq '.'

# read the new data
echo "[INFO] 7. Verifying multiple responses for reading newly created data, with a slash."
curl --silent "${SITE_URL}/" | jq '.[4].email' | grep 'alex.murphy@gmail.com'

echo "[INFO] 8. Verifying multiple responses for reading newly created data, by entity id."
curl --silent "${SITE_URL}/5" | jq '.email' | grep 'alex.murphy@gmail.com'

# verify error when creating new data, using an existing email address
echo "[INFO] 9. Verifying error response for creating new data, with an existing email address."
curl --silent --request POST \
    --header 'Content-Type: application/json' \
    --data-raw '
{
    "email":"alex.murphy@gmail.com",
    "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a333",
    "bool":"true",
    "datetime":"2023-07-25T16:57:36.908339"
}
' \
    "${SITE_URL}" \
     | jq '.message'

# verify error when creating new data, using an existing UUID
echo "[INFO] 10. Verifying error response for creating new data, with an existing UUID."
curl --silent --request POST \
    --header 'Content-Type: application/json' \
    --data-raw '
{
    "email":"alex.murphy999@gmail.com",
    "uuid":"752346e1-df66-485e-8f49-eb749d9ab666",
    "bool":"true",
    "datetime":"2023-07-25T16:57:36.908339"
}
' \
 "${SITE_URL}" \
    | jq '.message'



# update the data
echo "[INFO] 11. Verifying response for updating existing data."
curl --silent --request PUT \
    --header 'Content-Type: application/json' \
    --data-raw '
{
    "email":"alex.murphy999@gmail.com",
    "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
    "bool":"false",
    "datetime":"2023-07-25T16:57:36.999999"
}
' \
    "${SITE_URL}/5" \
    | jq '.'

# read the updated data
echo "[INFO] 12. Verifying response for reading updated data, with a slash."
curl --silent "${SITE_URL}/" | jq '.[4].email' | grep 'alex.murphy999@gmail.com'

echo "[INFO] 13. Verifying response for reading updated data, by entity id."
curl --silent "${SITE_URL}/5" | jq '.email' | grep 'alex.murphy999@gmail.com'

# verify error when updating existing data, using an existing email address
echo "[INFO] 14. Verifying response for updating existing data."
curl --silent --request PUT \
    --header 'Content-Type: application/json' \
    --data-raw '
{
     "email":"apolloclark@gmail.com",
     "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
     "bool":"false",
     "datetime":"2023-07-25T16:57:36.999999"
}
' \
    "${SITE_URL}/5" \
    | jq '.message'

# verify error when updating existing data, using an existing UUID
echo "[INFO] 15. Verifying response for updating existing data."
curl --silent --request PUT \
    --header 'Content-Type: application/json' \
    --data-raw '
{
     "email":"alex.murphy999@gmail.com",
     "uuid":"752346e1-df66-485e-8f49-eb749d9ab806",
     "bool":"false",
     "datetime":"2023-07-25T16:57:36.999999"
}
' \
    "${SITE_URL}/5" \
    | jq '.message'


echo "[INFO] 16. Verifying error response for updating missing entity."
curl --silent --request PUT \
    --header 'Content-Type: application/json' \
    --data-raw '
{
    "email":"alex.murphy999@gmail.com",
    "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
    "bool":"false",
    "datetime":"2023-07-25T16:57:36.999999"
}
' \
    "${SITE_URL}/999" \
    | jq '.'

echo "[INFO] 17. Verifying error response for updating null entity."
curl --silent --request PUT \
    --header 'Content-Type: application/json' \
    --data-raw '
{
    "email":"alex.murphy999@gmail.com",
    "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
    "bool":"false",
    "datetime":"2023-07-25T16:57:36.999999"
}
' \
    "${SITE_URL}/" \
    | jq '.'




# delete the data, it should return an HTTP 200 and an empty JSON object {}
echo "[INFO] 18. Verifying response for deleting existing entity."
curl --silent --request "DELETE" \
    "${SITE_URL}/1" \
    | jq '.'

# delete the same data again, confirm an error message
echo "[INFO] 19. Verifying error response for deleting missing entity."
curl --silent --request "DELETE" \
    "${SITE_URL}/999" \
    | jq '.message'

echo "[INFO] 20. Verifying error response for deleting null entity."
curl --silent --request "DELETE" \
    "${SITE_URL}/" \
    | jq '.'

echo "[INFO] 21. Verifying error response for reading deleted entity."
curl --silent --request "DELETE" \
    "${SITE_URL}/5" \
    | jq '.'

# confirm the data is deleted, and an HTTP 404 and an error message are returned
echo "[INFO] 22. Verifying error response for reading missing entity."
curl --silent "${SITE_URL}/1" | jq '.message'

# reinit database
echo "[INFO] Resetting the database and seeding it with data."
docker compose exec web python cli.py reinit_db

# confirm success
echo "[INFO] SUCCESS! Completed all tests."
