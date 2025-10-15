from flask import Flask, request, jsonify
import os
from recommender_core import RecommenderCore
from mock_dependancies import MockFetcher
# from mock_dependancies import MockStorage
from storage import RedisStorage, PostgresStorage

app = Flask(__name__)

mock_fetcher = MockFetcher()

redis_url = os.getenv('REDIS_URL')
database_url = os.getenv('DATABASE_URL')

redis_storage = RedisStorage(redis_url=redis_url)
postgres_storage = PostgresStorage(db_url=database_url)

core = RecommenderCore(
    config={
        'oklm_manager_url': os.getenv('URI_OKLM_MANAGER', 'http://oklm_manager:5000'),
        'redis_url': os.getenv('REDIS_URL')
    },
    fetcher = mock_fetcher,
    tempstorage = redis_storage,
    parmstorage = postgres_storage
)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({'error': 'student_id required'}), 400
    k = int(request.args.get('k', 10))
    recs = core.recommend_for_student(student_id, k=k)
    return jsonify({'recommended_problems': recs})

@app.route('/event', methods=['POST'])
def ingest_event():
    # vis_ml からのクリック等のイベントを受け取る
    event = request.json
    core.ingest_event(event)
    return jsonify({'status': 'ok'}), 201



