INSTALL httpfs;
LOAD httpfs;

SET s3_endpoint='172.25.0.3:9000';
SET s3_access_key_id='minio';
SET s3_secret_access_key='minio123';
SET s3_use_ssl=false;
SET s3_url_style='path';

SELECT DISTINCT   snippet.channelId as id_canal,  snippet.videoId as id_video , nome_canal, titulo_video
            FROM read_json_auto('s3://youtube/bronze/comentarios/id_canal=*/id_video=*/id_comentario=*/comentario*.json');


SELECT *
FROM read_json_auto('s3://youtube/bronze/comentarios/id_canal=*/id_video=*/id_comentario=*/comentario*.json');


INSTALL httpfs;
LOAD httpfs;

SET s3_endpoint='172.25.0.3:9000';
SET s3_access_key_id='minio';
SET s3_secret_access_key='minio123';
SET s3_use_ssl=false;
SET s3_url_style='path';

SELECT *
FROM read_json_auto(
    's3://youtube/bronze/resposta_comentarios/id_canal=*/id_video=*/id_comentario=*/id_resposta_comentario=*/*.json'
);



