import airflow
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from jinja2 import Template

from world_cup_qatar_elt_bq.dag.settings import Settings

settings = Settings()


def get_jinja_template(file_path: str) -> Template:
    with open(f'{settings.queries_path}/{file_path}') as fp:
        return Template(fp.read())


def execute_bq_job(query_path: str,
                   bq_job_task_id: str):
    query = get_jinja_template(query_path).render(
        project_id=settings.project_id,
        dataset=settings.dataset
    )

    return BigQueryInsertJobOperator(
        task_id=bq_job_task_id,
        configuration={
            "query": {
                "query": query,
                "useLegacySql": False
            }
        },
        location='EU'
    )


with airflow.DAG(
        "team_league_elt",
        default_args=settings.dag_default_args,
        schedule_interval=None) as dag:
    load_team_stats_raw_to_bq = GCSToBigQueryOperator(
        task_id='load_team_stats_raw_to_bq',
        bucket=settings.variables['team_players_stat_input_bucket'],
        source_objects=[settings.variables['team_players_stat_source_object']],
        destination_project_dataset_table=f'{settings.project_id}.{settings.dataset}.{settings.team_players_stat_raw_table}',
        source_format='NEWLINE_DELIMITED_JSON',
        compression='NONE',
        create_disposition=settings.variables['team_players_stats_raw_create_disposition'],
        write_disposition=settings.variables['team_players_stats_raw_write_disposition'],
        autodetect=True
    )

    build_players_stats_udf = execute_bq_job(
        query_path='udfs/build_players_stats.sql',
        bq_job_task_id='build_players_stats_udf'
    )

    build_players_stats_raw_cleaned = execute_bq_job(
        query_path='staging/team_players_stat_raw_cleaned.sql',
        bq_job_task_id='build_players_stats_raw_cleaned'
    )

    build_players_stats_mart = execute_bq_job(
        query_path='marts/team_players_stat.sql',
        bq_job_task_id='build_players_stats_mart'
    )

    (
            load_team_stats_raw_to_bq >>
            build_players_stats_udf >>
            build_players_stats_raw_cleaned >>
            build_players_stats_mart
    )
