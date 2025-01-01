import os
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid
from database_editor import DatabaseEditor
from get_attendance import get_attendance_info_from_marco
import argparse
from datetime import datetime, timedelta
import pprint
import time
from cfg.user_info import GAKUBAN_NAME_MAPPING
import re

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', '-sd', help='extraction start date', type=str, default=datetime.now().strftime("%Y/%m/%d"))
    parser.add_argument('--end_date', '-ed', help='extraction end date', type=str, default=datetime.now().strftime("%Y/%m/%d"))
    return parser.parse_args()


def get_latest_attendance_infos(attendance_infos, prev_date):
    """
    Filters and retrieves attendance information recorded after a specific date and time.

    Args:
        attendance_infos (List(dict)): A list of dictionaries containing attendance information.
        prev_date (List): A tuple containing the previous date and time as:
            - prev_date[0] (str): The date in "YYYY/MM/DD" format.
            - prev_date[1] (str): The time in "HH:MM:SS" format.

    Returns:
        latest_attendance_infos(List(dict)): A list of dictionaries containing attendance records after "prev_date".
    """
    # 最新の入室情報の取得
    is_prev = True
    latest_attendance_infos = []

    # 最新の入室情報のみを取得する場合↓
    # return attendance_infos[-1]

    # prev_date以降の情報をすべて抽出
    for attendance_info in attendance_infos:
        if is_prev:
            if attendance_info['dakokuDate'] == prev_date[0] and attendance_info['dakokuHms'] == prev_date[1]:
                is_prev = False
            continue
        else:
            latest_attendance_infos.append(attendance_info)
    return latest_attendance_infos


def update_spec_person_info(db_editor, attendance_infos):
    """
    Updates or inserts attendance information for specific individuals into the database.

    Args:
        db_editor (DatabaseEditor): An instance of the DatabaseEditor class used for database operations.
        attendance_infos (list): A list of dictionaries containing attendance information.
    """
    for attendance_info in attendance_infos:
        access_update_time = f"{attendance_info['dakokuDate'].replace('/', '-')} {attendance_info['dakokuHms']}"
        current_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {
            'created_at': current_datetime,
            'student_id': attendance_info['gakusekiNum'],
            'person_name': GAKUBAN_NAME_MAPPING[attendance_info['gakusekiNum']],
            'class_room': attendance_info['kyoshitsuName'],
            'access_update_time': access_update_time,
            'access_status': 'enter',
        }
        filter_criteria = {
            'student_id': data['student_id'],
        }
        if len(db_editor.select_row(filter_criteria)) == 0:
            db_editor.insert_row(data)
        else:
            selected_row = db_editor.select_row(filter_criteria)
            if selected_row[0]['access_status'] == 'enter' and selected_row[0]['class_room'] == data['class_room']:
                data['access_status'] = 'exit'
            db_editor.update_row(data, filter_criteria)
        time.sleep(3)


def main():
    args = get_args()

    load_dotenv('.env')
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    table_name = os.environ.get("TABLE_NAME")
    j_session_id = os.environ.get("J_SESSION_ID")
    student_id = os.environ.get("STUDENT_ID")

    db_editor = DatabaseEditor(url, key, table_name)

    start_date = datetime.strptime(args.start_date, '%Y/%m/%d')
    end_date = datetime.strptime(args.end_date, '%Y/%m/%d')

    # 抽出する日付範囲を配列に格納
    extraction_date = [(start_date + timedelta(days=i)).strftime('%Y/%m/%d') 
                for i in range((end_date - start_date).days + 1)]

    # 特定範囲の日付の打刻履歴を取得
    attendance_infos = get_attendance_info_from_marco(j_session_id, student_id, extraction_date)
    attendance_infos = sorted(attendance_infos, key=lambda x: (x["dakokuDate"], x["dakokuHms"]))

    # 最新の入室情報の取得
    filter_criteria = {
        'student_id': student_id,
    }
    selected_row = db_editor.select_row(filter_criteria)
    latest_attendance_infos = []
    if len(selected_row) == 0:
        latest_attendance_infos = attendance_infos
    else:  
        prev_date = re.split('[T+]', selected_row[0]['access_update_time'])[:-1]
        prev_date = ['2024/12/20', '19:17:21']
        prev_date[0] = prev_date[0].replace('-', '/')
        latest_attendance_infos = get_latest_attendance_infos(attendance_infos, prev_date)

    # tableへの更新
    update_spec_person_info(db_editor, latest_attendance_infos)


if __name__ == '__main__':
    main()
