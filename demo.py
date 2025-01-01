import os
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid
from database_editor import DatabaseEditor
import argparse



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table_name", "-tn")
    
    return True

def main():
    get_args()
    load_dotenv('.env')
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    table_name = "daily_attendance"

    exit()
    data = {
        "uuid": str(uuid.uuid4()),
        "created_at": "2024-12-27",
        "enter_time": "2024-12-27",
        "student_id": "test_3",
        "class_room": "test_3",
        "is_posted": True,
    }
    DBeditor = DatabaseEditor(url, key, table_name)
    # DBeditor.delete_row(filter_criteria={"student_id": "test_2"})
    DBeditor.update_row(update_to_data={"student_id": "test_2"}, filter_criteria={})
    # DBeditor.insert_row(data)
    # print(DBeditor.select_row(filter_criteria={"student_id": "test_2"}))
    # print(DBeditor.select_row())
    exit()


if __name__ == "__main__":
    main()