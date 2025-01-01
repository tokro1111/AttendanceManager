import os
from supabase import create_client, Client
import uuid


class DatabaseEditor:
    def __init__(self, url, key, table_name):
        """
        Initializes the DatabaseEditor with Supabase connection and table name.

        Args:
            url (str): The Supabase project URL.
            key (str): The Supabase project API key.
            table_name (str): The name of the table to perform operations on.
        """
        self.supabase_test = create_client(url, key)
        self.table_name = table_name

    def insert_row(self, data):
        """
        Inserts a new row into the table.

        Args:
            data (dict): The data to insert, where keys represent column names
                         and values represent the corresponding values.
        """
        response = (
            self.supabase_test.table(self.table_name)
            .insert(data)
            .execute()
        )

    def delete_row(self, filter_criteria={}):
        """
        Deletes rows from the table based on filter criteria.

        Args:
            filter_criteria (dict, optional): A dictionary of column-value pairs
                                              to filter rows for deletion.
                                              Defaults to {} (deletes all rows).
        """
        resp_source = self.supabase_test.table(self.table_name).delete()
        if len(filter_criteria) == 0: # 指定のない場合はすべての行を削除
            resp_source = resp_source.neq('uuid', str(uuid.uuid4()))
        else:
            for key, value in filter_criteria.items():
                resp_source = resp_source.eq(key, value)
        response = (
            resp_source.execute()
        )


    def update_row(self, update_to_data, filter_criteria):
        """
        Updates rows in the table based on filter criteria.

        Args:
            update_to_data (dict): A dictionary representing the columns and their new values.
            filter_criteria (dict): A dictionary of column-value pairs to filter rows for updating.
        """
        resp_source = self.supabase_test.table(self.table_name).update(update_to_data)
        if len(filter_criteria) == 0: # 指定のない場合はすべての行をアップデート
            resp_source = resp_source.neq('uuid', str(uuid.uuid4()))
        for key, value in filter_criteria.items():
            resp_source = resp_source.eq(key, value)
        response = (
            resp_source.execute()
        )

    def select_row(self, filter_criteria={}):
        """
        Retrieves rows from the table based on filter criteria.

        Args:
            filter_criteria (dict, optional): A dictionary of column-value pairs
                                              to filter rows for retrieval.
                                              Defaults to {} (retrieves all rows).

        Returns:
            list: A list of rows matching the filter criteria.
        """
        resp_source = self.supabase_test.table(self.table_name).select("*")
        for key, value in filter_criteria.items():
            resp_source = resp_source.eq(key, value)
        response = (
            resp_source.execute()
        )
        return response.data
