#!/bin/sh

minio server ~/minio --address "10.5.0.2:9000" --console-address "10.5.0.2:9001" &

MINIO_PID=$!

is_minio_ready() {
  curl -s http://10.5.0.2:9000/minio/health/live > /dev/null
}

setup_minio_alias() {
  mc alias set myminio http://10.5.0.2:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
}

create_bucket() {
  BUCKET=$1
  if ! mc ls myminio/$BUCKET > /dev/null 2>&1; then
    echo "Creating bucket: $BUCKET"
    mc mb myminio/$BUCKET
  else
    echo "Bucket $BUCKET already exists"
  fi
}

until setup_minio_alias; do
  echo "Waiting for MinIO server to be ready..."
  sleep 5
done

BUCKETS=("users" "posts" "groups")

for BUCKET in "${BUCKETS[@]}"; do
  create_bucket $BUCKET
done

kill $MINIO_PID

exec minio server ~/minio --address "10.5.0.2:9000" --console-address "10.5.0.2:9001"