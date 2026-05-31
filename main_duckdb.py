import duckdb

from src.contexto.video_youtube import VideoYoutube

con = duckdb.connect()

con.execute("""
INSTALL httpfs;
LOAD httpfs;

SET s3_endpoint='172.25.0.3:9000';
SET s3_access_key_id='minio';
SET s3_secret_access_key='minio123';
SET s3_use_ssl=false;
SET s3_url_style='path';
""")

df = con.execute("""
SELECT DISTINCT snippet.channelId as id_canal,  snippet.videoId as id_video
FROM read_json_auto('s3://youtube/bronze/comentarios/id_canal=*/id_video=*/id_comentario=*/comentario*.json');
""").fetchdf()
for linha in df.itertuples(index=False, name=None):
    video = VideoYoutube(*linha)

    print(video.id_video)
    print(video.id_canal)