## 1. 概要
- 研究室の入退室をデジタルで管理するために、supabaseを使用した入退室情報の可視化を実施
- 今後時間が空き次第、随時修正予定

## 2. 実行環境
### 確認済み環境
- python3.11.3

### 使用ツール
- [supabase](https://supabase.com/)

## 2. 機能
supabaseのテーブルを更新し、登録者の入退室情報を下記のように可視化する。
|uuid|created_at|student_id|person_name|class_room|access_status|access_update_time|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|d5df...|2025-01-01 20:42:41|gakuseki_bango_1|Name_1|0号館  0階 テスト教室 入室リーダ|exit|2025-01-01 20:30:15|
|8lKm...|2025-01-01 19:00:40|gakuseki_bango_2|Name_2|0号館  0階 テスト教室 入室リーダ|enter|2025-01-01 18:55:15|
- created_at: tableに追加された日時
- student_id: 学籍番号
- person_name: 名前
- class_room: 入退室場所
- access_status: enter(入室)とexit(退室)のどちらか
- access_update_time: 入退室のどちらかが発生した時間帯

## 3. 実行方法
1. supabaseでtable(「2. 機能」記載)を作成
2. `cfg/sample/user_info.py`を参考に、ユーザ情報を記入した`cfg/user_info.py`を作成
3. `cfg/sample/data_info.py`を参考に、教室コードをkey、教室名をvalueとするdictを記入した`cfg/data_info.py`を作成
4. .env.exampleを参考に、環境変数を設定
5. `update_table.py`の実行


## 4. 追加・修正予定一覧
- user_infoを別の形式で管理
- dockerfileを構築し、コンテナ内で10分ごとに更新し続ける処理を追加
- 複数人対応処理の追加
- （他の人ので試す前に）supabaseのpolicyを適切なものに設定（RLS）

