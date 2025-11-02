# world-cup-qatar-elt-airflow-bq

This project shows a real world use case (Football stats for Qatar World Cup) with ELT pipeline using Cloud Storage, BigQuery, Airflow and Cloud Composer

### Deploy the Airflow DAG in Composer with Cloud Build from the local machine

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config deploy-dag.yaml \
    --substitutions _FEATURE_NAME="team_league_elt",_COMPOSER_ENVIRONMENT="dev-composer-env",_CONFIG_FOLDER_NAME="config",_ENV="dev" \
    --verbosity="debug" .
```
