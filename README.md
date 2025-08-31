# 需要予測API
<img width="517" height="670" alt="スクリーンショット 2025-08-31 23 30 51" src="https://github.com/user-attachments/assets/cd3f42c6-1234-4285-b9e5-ca5f1ca8fbf1" />

これは、FastAPIとscikit-learnを使用して構築されたシンプルな需要予測アプリケーションです。過去の販売データに基づいて、将来の販売数を予測します。

## 主な機能

- **Web UI**: ブラウザから簡単に予測を実行できるインターフェース (`/`).
- **`/predict`**: 広告費、気温、曜日などの入力特徴量に基づいて販売数を予測します。
- **`/train`**: `sample_data.csv`を使用して機械学習モデルを再学習します。
- **`/health`**: アプリケーションのヘルスチェックを行います。

## 技術スタック

- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **ML/Data**: scikit-learn, pandas, numpy
- **Server**: Uvicorn, Gunicorn

---

## プロジェクト構成

主要なファイルとその役割は以下の通りです。

```
demand_forecast_app/
├── static/           # フロントエンドファイル (HTML, CSS, JS)
├── app.py            # FastAPIアプリケーション本体 (APIエンドポイント定義)
├── train.py          # モデルを学習するためのスクリプト
├── config.py         # ファイルパスなど、プロジェクト全体の設定を管理
├── sample_data.csv   # モデル学習用のサンプルデータ
├── model.pkl         # train.pyによって生成される学習済みモデル
├── requirements.txt  # 依存ライブラリ
└── README.md         # このファイル
```

---

## セットアップと実行方法

### 1. 準備

まず、プロジェクトファイルをダウンロードまたはクローンし、そのディレクトリに移動します。

```bash
cd demand_forecast_app
```

### 2. 仮想環境の作成と有効化（推奨）

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化 (macOS / Linux)
source venv/bin/activate
```

### 3. 依存関係のインストール

`requirements.txt`を使用して、必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

### 4. アプリケーションの起動

`uvicorn`を使用して、開発サーバーを起動します。

```bash
uvicorn app:app --reload
```

サーバーが `http://127.0.0.1:8000` で起動します。
ブラウザで `http://127.0.0.1:8000` にアクセスすると、Web UIが表示されます。
APIドキュメントは `http://127.0.0.1:8000/docs` で確認できます。

---

## APIエンドポイントの使い方

Web UIのほか、`curl`コマンドなどを使って直接APIを呼び出すことも可能です。

### ヘルスチェック

```bash
curl http://127.0.0.1:8000/health
```

### モデルの学習

```bash
curl -X POST http://127.0.0.1:8000/train
```

### 販売数の予測

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "ad_spend": 180,
  "temperature": 17,
  "day_of_week": "Thursday"
}'
```

**応答例 (v2):**
```json
{
  "predicted_sales": 229.08510575340713
}
```

---

## モデルの変更方法

このアプリケーションでは、予測に使用する機械学習モデルを簡単に入れ替えることができます。
ここでは例として、デフォルトの線形回帰（`LinearRegression`）からランダムフォレスト（`RandomForestRegressor`）に変更する手順を説明します。

### ステップ1: `train.py`を編集する

モデルの定義は `train.py` ファイル内にあります。このファイルを編集して、使用するモデルを変更します。

1.  **新しいモデルをインポート**: `sklearn`から使用したいモデル（例: `RandomForestRegressor`）をインポートします。
2.  **モデルのインスタンス化部分を変更**: `model = ...` の行を、新しいモデルのインスタンスを作成するように書き換えます。

**ファイル:** `demand_forecast_app/train.py`

**【変更前】**
```python
from sklearn.linear_model import LinearRegression

# ...
model = LinearRegression()
# ...
```

**【変更後】**
```python
from sklearn.ensemble import RandomForestRegressor

# ...
# n_estimatorsなどのハイパーパラメータは自由に調整してください
model = RandomForestRegressor(n_estimators=100, random_state=42)
# ...
```

### ステップ2: 新しいモデルで再学習する

`train.py` を保存したら、変更を反映させるためにモデルを再学習し、`model.pkl` を更新します。

- **方法A: ターミナルでスクリプトを実行**
  ```bash
  python3 train.py
  ```
- **方法B: APIエンドポイントを呼び出す**
  アプリケーションの実行中に、以下のコマンドを実行します。
  ```bash
  curl -X POST http://127.0.0.1:8000/train
  ```

### ステップ3: 確認

`uvicorn app:app --reload` コマンドで開発サーバーを起動している場合、`.py`ファイルを保存するとサーバーが自動で再起動し、新しいモデルが読み込まれます。

Web UI (`http://127.0.0.1:8000`) を開き、以前と同じ値を入力して予測結果が変わることを確認してください。

> **ポイント**: scikit-learnに準拠した（`.fit()`と`.predict()`メソッドを持つ）モデルであれば、`app.py`を一切変更することなく、この手順で簡単に入れ替えることが可能です。

---

## Renderでのデプロイ

[Render.com](https://render.com/)で新しいWebサービスを作成する際に、以下の設定を使用します。

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app`
