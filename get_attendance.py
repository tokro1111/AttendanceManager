import os
from dotenv import load_dotenv
import argparse
import json
import time
import pprint
from cfg.data_info import CLASSROOMS_INFO

from datetime import datetime, timedelta
import subprocess


def get_attendance_info_from_marco(j_session_id, student_id, extraction_date=[]):
    """
    Fetches attendance information from the MARCO system.

    Args:
        j_session_id (str): The session ID (JSESSIONID) required for authentication with the MARCO system.
        student_id (str): The student's ID used to fetch attendance data.
        extraction_date (List(str)): A list of dates (as strings, e.g., "YYYY/MM/DD") to filter the attendance data.
                                          Defaults to an empty list, meaning no filtering by date.

    Returns:
        outputs: A list of dictionaries containing attendance information that matches the `extraction_date`
    """
    command = [
        "curl", "https://marco-s.ms.dendai.ac.jp/start/student/search/searchDetail/dakokuInfo" ,
        "-H", "Accept: application/json, text/javascript, */*; q=0.01",
        "-H", "Accept-Language: en-US,en;q=0.9,ja;q=0.8",
        "-H", "Cache-Control: no-cache",
        "-H", "Connection: keep-alive",
        "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
        "-H", f"Cookie: JSESSIONID={j_session_id}",
        "-H", "Origin: https://marco-s.ms.dendai.ac.jp",
        "-H", "Pragma: no-cache",
        "-H", "Referer: https://marco-s.ms.dendai.ac.jp/start/student/search/searchTimestamp",
        "-H", "Sec-Fetch-Dest: empty",
        "-H", "Sec-Fetch-Mode: cors",
        "-H", "Sec-Fetch-Site: same-origin",
        "-H", "X-Requested-With: XMLHttpRequest",
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", 'sec-ch-ua-platform: ""',
        "--data-raw", f"gakusekiNum={student_id}&selectNendo="
    ]

    results = []
    outputs = []
    shisetsu_cds = list(CLASSROOMS_INFO.keys())
    while True:
        try:
            response = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            results = json.loads(response.stdout.strip())
            break
        except Exception as e:
            print(e, "Error executing command")
            time.sleep(5)
    
    for result in results["dakokuDataList"]:
        if result["dakokuDate"] in extraction_date and result['shisetsuCd'] in shisetsu_cds:
            outputs.append(result)
    return outputs


def main():
    load_dotenv('.env')
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    j_session_id = os.environ.get("J_SESSION_ID")
    student_id = os.environ.get("STUDENT_ID")

    start_date = datetime.strptime('2024/12/20', '%Y/%m/%d')
    end_date = datetime.strptime('2024/12/21', '%Y/%m/%d')

    # 抽出する日付範囲を配列に格納
    extraction_date = [(start_date + timedelta(days=i)).strftime('%Y/%m/%d') 
                for i in range((end_date - start_date).days + 1)]

    # 特定範囲の日付の打刻履歴を取得
    outputs = get_attendance_info_from_marco(j_session_id, student_id, extraction_date)
    pprint.pprint(outputs)


if __name__ == "__main__":
    main()


