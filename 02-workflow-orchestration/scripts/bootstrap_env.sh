#!/usr/bin/env bash
# push terraform output values automatically into kestra's kv
# by trigerring 00_environment_setup flows
# requires: jq, curl

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

NAMESPACE="zoomcamp"
FLOW_ID="00_environment_setup"
MAX_RETRIES=30
RETRY_DELAY=3                   # 30 * 3s = 90s ceiling on the API wait

# check if .env file is exist
if [ ! -f .env ]; then
  echo "Missing .env. Copy .env.example to .env and fill in your values first." >&2
  exit 1
fi

# read .env file and extract
set -a; source .env; set +a

KESTRA_URL="http://localhost:${KESTRA_UI_PORT:-18081}"

TF_JSON=$(cd terraform && terraform output -json)
PROJECT_ID=$(echo "$TF_JSON" | jq -r '.project_id.value')
REGION=$(echo "$TF_JSON" | jq -r '.region.value')
BUCKET_NAME=$(echo "$TF_JSON" | jq -r '.bucket_name.value')
DATASET_ID=$(echo "$TF_JSON" | jq -r '.dataset_id.value')

# guard for null value
for pair in "project_id:$PROJECT_ID" "region:$REGION" "bucket_name:$BUCKET_NAME" "dataset_id:$DATASET_ID"; do
  name="${pair%%:*}"
  value="${pair#*:}"
  if [ "$value" = "null" ] || [ -z "$value" ]; then
    echo "Terraform output '${name}' is missing or null - check terraform/outputs.tf" >&2
    exit 1
  fi
done

# check if kestra is active
echo "Using Kestra at ${KESTRA_URL} (from KESTRA_UI_PORT in .env)"
echo "Waiting for Kestra's API to come up..."
attempt=0
until [ "$(curl -s -o /dev/null -w '%{http_code}' "${KESTRA_URL}/api/v1/main/flows/search" 2>/dev/null)" != "000" ]; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge "$MAX_RETRIES" ]; then
    echo "Kestra never came up after $((MAX_RETRIES * RETRY_DELAY))s at ${KESTRA_URL} - check 'docker compose ps' and the KESTRA_UI_PORT value" >&2
    exit 1
  fi
  sleep "$RETRY_DELAY"
done

# check if there is 00_environment_setup flows
echo "Confirming ${FLOW_ID} was picked up by local sync..."
attempt=0
until curl -sf -u "${KESTRA_BASIC_AUTH_USERNAME}:${KESTRA_BASIC_AUTH_PASSWORD}" \
  "${KESTRA_URL}/api/v1/main/flows/${NAMESPACE}/${FLOW_ID}" >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge "$MAX_RETRIES" ]; then
    echo "${FLOW_ID} never appeared in namespace ${NAMESPACE} - check that flows/main_${NAMESPACE}_${FLOW_ID}.yaml exists and local sync is enabled" >&2
    exit 1
  fi
  echo "  not found yet, retrying..."
  sleep 2
done

# trigger the flow
echo "Triggering ${FLOW_ID} with values from terraform output..."
HTTP_CODE=$(curl -s -o /tmp/kestra_response.json -w '%{http_code}' \
  -u "${KESTRA_BASIC_AUTH_USERNAME}:${KESTRA_BASIC_AUTH_PASSWORD}" \
  -X POST "${KESTRA_URL}/api/v1/main/executions/${NAMESPACE}/${FLOW_ID}?wait=true" \
  -F "gcp_project_id=${PROJECT_ID}" \
  -F "gcp_region=${REGION}" \
  -F "gcp_bucket_name=${BUCKET_NAME}" \
  -F "gcp_dataset=${DATASET_ID}")

# check if done
if [ "$HTTP_CODE" != "200" ]; then
  echo "Failed (HTTP $HTTP_CODE):" >&2
  cat /tmp/kestra_response.json >&2
  exit 1
fi

echo "Done. Check Kestra UI (${KESTRA_URL}) > Namespaces > zoomcamp > KV to confirm."