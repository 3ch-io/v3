# 掲示板管理 (Board Management)

3ch-v3システムにおける掲示板（板）の作成、設定、および基本構造に関する仕様。

## 1. 掲示板の作成 (`main.cgi`)

掲示板の新規作成時、以下のバリデーションと初期化が行われる。

### バリデーション
- **ディレクトリ名**: 
  - 2文字以上16文字以下の半角英数小文字。
  - 予約語（`test`, `tmp`, `admin`, `join`, `menu`, `images`, `hashtag`）は使用不可。
- **必須項目**: 掲示板名、管理人メールアドレス、パスワード、ルールへの同意。

### 初期化処理
- 指定されたディレクトリを作成（パーミッション `0755`）。
- `SETTING.TXT` の生成: UIスタイル（`simple` または `2ch`）に応じた初期設定を書き込む。
- `pass.cgi`: 管理パスワードを保存。
- `subject.txt`: スレッド一覧ファイルを空で作成。
- `log.cgi`: 作成者のIP、ポート、UAを記録。
- カテゴリ一覧（`USER_COMMUNITY.cgi`）への追記。

## 2. 設定管理 (`SETTING.TXT`, `setting.cgi`)

掲示板の動作を制御する多数のパラメータが `SETTING.TXT` に保存される。

### 主要な設定項目
- **基本情報**: `BBS_TITLE`, `ADMIN_MAIL`, `BBS_NONAME_NAME`（デフォルト名）。
- **表示制限**: 
  - `BBS_THREAD_NUMBER`: 1ページあたりのスレッド数。
  - `BBS_CONTENTS_NUMBER`: スレッドトップで表示するレス数。
  - `BBS_LINE_NUMBER`: 投稿行数制限。
- **容量・期間制限**:
  - `MAX_RES`: 最大レス数（300～2000）。
  - `BBS_THREAD_QUANTITY`: 現行スレッド保持数。
  - `TIME_TO_LIVE`, `BBS_TH_LINE`: 過去ログ化判定（レス数が少ないスレッドの寿命）。
  - `BBS_MAX_MODIFIED`: スレッド継続最低秒数（突然死判定）。
  - `BBS_THREAD_LIFETIME`: スレッドの絶対寿命。
- **規制・セキュリティ**:
  - `BBS_FR_LEVEL`: 連投規制レベル（0:短時間, 1:連続, 2:マルチポスト, 4:広域, 8:新規）。
  - `BBS_UNICODE`: 絵文字等の扱い（許可/拒否/変換）。
  - `BBS_PROXY_CHECK`, `BBS_JP_CHECK`, `BBS_FOREIGN_PASS`: プロキシや海外ホストの制限。
  - `BBS_SLIP`: ID表示方式（feature, Korokoro, IP表示など）。

## 3. スレッド一覧編集 (`subject.cgi`)

- `subject.txt` を直接編集し、スレッドの表示/非表示や過去ログ化を管理する。
- 1行につき1スレッドの形式。
- 特定のキーワード（`hide` など）を含む行や、行の削除によってスレッドを一覧から除外（過去ログ扱い）する。
