# world-cup-qatar-elt-airflow-bq

This project shows a real world use case (Football stats for Qatar World Cup) with ELT pipeline using Cloud Storage, BigQuery, Airflow and Cloud Composer

### Deploy the DAG and conf in a local Airflow from Docker 

```bash
docker run -it \
    -p 8080:8080 \
    -e GOOGLE_APPLICATION_CREDENTIALS=/root/.config/gcloud/application_default_credentials.json \
    -e GCP_PROJECT=gb-poc-373711 \
    -v $HOME/.config/gcloud/application_default_credentials.json:/root/.config/gcloud/application_default_credentials.json \
    -v $(pwd)/world_cup_qatar_elt_bq:/opt/airflow/dags/world_cup_qatar_elt_bq \
    -v $(pwd)/config:/opt/airflow/config \
    airflow-dev
```

### Deploy the Airflow DAG in Composer with Cloud Build from the local machine

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config deploy-dag.yaml \
    --substitutions _FEATURE_NAME="team_league_elt",_COMPOSER_ENVIRONMENT="dev-composer-env",_CONFIG_FOLDER_NAME="config",_ENV="dev" \
    --verbosity="debug" .
```
