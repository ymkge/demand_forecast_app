from pathlib import Path

# このファイルの親ディレクトリ（つまり、プロジェクトのルート）を取得
BASE_DIR = Path(__file__).resolve().parent

# データファイルへのパス
DATA_PATH = BASE_DIR / "sample_data.csv"

# 学習済みモデルを保存するパス
MODEL_PATH = BASE_DIR / "model.pkl"

# フロントエンドの静的ファイルが格納されているディレクトリへのパス
STATIC_DIR = BASE_DIR / "static"
