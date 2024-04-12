# gcp-dataproc-serveless

#### Create Artifact Registry repo
gcloud artifacts repositories create ${AF_REPO_NAME} --repository-format=docker --location=${REGION}

#### Build Image
gcloud builds submit --config cloudbuild.yaml --substitutions _PROJECT_ID=${PROJECT_ID},_REPO_NAME=${AF_REPO_NAME},_IMAGE_NAME=${IMAGE_NAME},_COMMIT_SHA=${COMMIT_SHA}

### Open network firewall rules so workers can talk to each other & master node, or it won't work
gcloud compute firewall-rules create allow-internal-ingress \
--network="default" \
--source-ranges="0.0.0.0/0" \
--direction="ingress" \
--action="allow" \
--rules="all"

### Submit the job via gcloud
#### enable subnetwork to put Private Google Access=ON in region eu-west2 because i use this region to run dataproc serveless
gcloud dataproc batches submit pyspark gs://input-code/wordcount.py \
--batch wordcount-$(date +"%Y%m%d-%H%M%S") \
--project ${PROJECT_ID} \
--region ${REGION} \
--container-image "europe-west2-docker.pkg.dev/${PROJECT_ID}/${AF_REPO_NAME}/${IMAGE_NAME}:${IMAGE_VERSION}" \
--deps-bucket ${PROCESS_BUCKET} \
--service-account ${SPARK_SA} \
--version 2.0 \
--properties spark.dynamicAllocation.executorAllocationRatio=1.0,spark.dynamicAllocation.initialExecutors=3,spark.dynamicAllocation.minExecutors=3,spark.dynamicAllocation.maxExecutors=50 \
-- gs://input-bucket-gcp-etl / gs://output-bucket-gcp-etl 

### Submit the job via python
env/bin/python dataproc_submit.py "gs://input-code/wordcount.py" \
    "gs://input-bucket-gcp-etl/" \
    "gs://output-bucket-gcp-etl"