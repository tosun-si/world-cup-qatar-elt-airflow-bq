CREATE OR REPLACE AGGREGATE FUNCTION `{{project_id}}.{{dataset}}.build_player_stats`(
    stat_indicator FLOAT64,
    appearances INT64,
    brandSponsorAndUsed STRING,
    club STRING,
    position STRING,
    playerDob STRING,
    playerName STRING
)
RETURNS STRUCT<
   stat_value FLOAT64,
   players STRUCT<
      appearances INT64,
      brandSponsorAndUsed STRING,
      club STRING,
      position STRING,
      playerDob STRING,
      playerName STRING
   >
>
AS (
  STRUCT(
    MAX(stat_indicator) AS stat_value,
    ARRAY_AGG(
      IF(
        stat_indicator IS NOT NULL AND stat_indicator > 0,
        STRUCT(appearances, brandSponsorAndUsed, club, position, playerDob, playerName),
        NULL
      )
    )[OFFSET(0)] AS players
  )
);
