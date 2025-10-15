class Algorithm:
    """ダミーのアルゴリズムクラス"""
    def __init__(self, params=None):
        self.params = params

    def score(self, problem, profile, events):
        # とりあえず固定のスコアと理由を返す
        return 0.9, "This is a dummy reason."