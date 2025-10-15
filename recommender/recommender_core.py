from experiments import alg_v1

class RecommenderCore:
    def __init__(self, config=None, fetcher=None, tempstorage=None, parmstorage=None):
        self.config = config or {}
        # fetcherとstorageがNoneの場合でもエラーにならないようにする
        self.fetcher = fetcher
        self.tempstorage = tempstorage
        self.parmstorage = parmstorage
        self.algorithm = alg_v1.Algorithm(self.config.get('alg_params', {}))

    def recommend_for_student(self, student_id, k=5):
        # fetcherやstorageが設定されていない場合はエラーを出すか、デフォルトの動作をする
        if not self.fetcher or not self.tempstorage or not self.parmstorage:
            raise RuntimeError("Fetcher and Storage must be initialized.")

        profile = self.fetcher.get_student_profile(student_id)
        candidate_set = self.fetcher.get_candidate_problems(student_id)
        recent_events = self.tempstorage.get_recent_events(student_id)

        scored = []
        for p in candidate_set:
            score, reason = self.algorithm.score(problem=p, profile=profile, events=recent_events)
            scored.append((score, p, reason))

        scored.sort(key=lambda x: x[0], reverse=True)
        topk = scored[:k]
        
        return [{'problem_id': p['id'], 'score': s, 'reason': r} for s, p, r in topk]

    def ingest_event(self, event):
        if not self.tempstorage or not self.parmstorage:
            raise RuntimeError("Storage must be initialized.")
        self.tempstorage.push_event(event)
        self.parmstorage.log_event(event)
