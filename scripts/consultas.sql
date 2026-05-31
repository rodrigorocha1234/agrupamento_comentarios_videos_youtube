INSTALL httpfs;
LOAD httpfs;

SET s3_endpoint='172.25.0.3:9000';
SET s3_access_key_id='minio';
SET s3_secret_access_key='minio123';
SET s3_use_ssl=false;
SET s3_url_style='path';


SELECT DISTINCT STINCT snippet.videoId
FROM read_json_auto('s3://youtube/bronze/comentarios/id_canal=*/id_video=*/comentario*.json');