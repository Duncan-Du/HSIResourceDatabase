import sqlite3
from sqlite3 import Error

import pandas as pd

DB_PATH = 'hsidatabase.db'
TSV_DATABASE = 'notion_database.tsv'

resources_query = "INSERT INTO Resources (Name, URL, UsabilityDescription) VALUES (?, ?, ?)"

# Category Table Queries
check_category_exists_query = "SELECT CategoryID FROM Categories WHERE CategoryName = ?"
category_query = "INSERT INTO Categories (CategoryName) VALUES (?)"
resource_categories_query = "INSERT INTO ResourceCategories (ResourceID, CategoryID) VALUES (?, ?)"

# DataType Table Queries
check_datatype_exists_query = "SELECT DataTypeID FROM DataTypes WHERE TypeName = ?"
datatype_query = "INSERT INTO DataTypes (TypeName) VALUES (?)"
resource_datatypes_query = "INSERT INTO ResourceDataTypes (ResourceID, DataTypeID) VALUES (?, ?)"

# Languages Table Queries
check_language_exists_query = "SELECT LanguageID FROM Languages WHERE LanguageName = ?"
language_query = "INSERT INTO Languages (LanguageName) VALUES (?)"
resource_languages_query = "INSERT INTO ResourceLanguages (ResourceID, LanguageID) VALUES (?, ?)"

# DataFormats Table Queries
check_dataformat_exists_query = "SELECT DataFormatID FROM DataFormats WHERE FormatName = ?"
dataformat_query = "INSERT INTO DataFormats (FormatName) VALUES (?)"
resource_dataformats_query = "INSERT INTO ResourceDataFormats (ResourceID, DataFormatID) VALUES (?, ?)"


def connect_to_db(path):
    """
    Connect to the SQLite database
    :param path: path to the database
    :return: connection to the database
    """
    try:
        connection = sqlite3.connect(path)
        print('Connected to SQLite database')
        return connection
    except Error as e:
        print(f"Error: {e}")


def delete_all_rows(connection):
    """
    Delete all rows from all tables in the SQLite database
    :param connection: SQLite connection
    """
    try:
        cursor = connection.cursor()

        tables = ['Categories', 'DataTypes', 'Languages', 'DataFormats', 'Resources', 'ResourceDataTypes',
                  'ResourceLanguages', 'ResourceDataFormats', 'Applications', 'ResourceApplications']

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")

        connection.commit()
        print("All rows deleted from all tables.")
    except Error as e:
        print(f"Error: {e}")


def insert_data(connection, query, data):
    """
    Insert data into the database
    :param connection: SQLite connection
    :param query: SQL query to execute
    :param data: data to insert
    :return: the last inserted ID
    """
    try:
        cursor = connection.cursor()

        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error: {e}")


def check_exists(connection, query, data):
    """
    Check if a record exists in the database
    :param connection: SQLite connection
    :param query: SQL query to execute
    :param data: data to check
    :return: the ID of the record if it exists. None otherwise
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        return cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # Read the TSV data
    data = pd.read_csv(TSV_DATABASE, delimiter='\t')

    # Connect to the database
    db_connection = connect_to_db(DB_PATH)

    # exists = check_exists(db_connection, check_category_exists_query, ('BABC',))
    # print(exists)

    # delete all rows from database
    print("Deleting all rows from all tables")
    delete_all_rows(db_connection)

    for index, row in data.iterrows():
        print("Processing row: ", index, ". Content: ")
        print(row)
        # Insert into Resources table

        resource_data = (row['Name'], row['URL'], row['Usability'])
        resource_id = insert_data(db_connection, resources_query, resource_data)

        # Categories
        if not pd.isna(row['Category']):
            categories = row['Category'].split(',')
            for category in categories:
                category_exists = check_exists(db_connection, check_category_exists_query, (category,))
                if category_exists is not None:
                    category_id = category_exists[0]
                    print(category, " category exists: category_id = ", category_id)
                else:
                    category_id = insert_data(db_connection, category_query, (category,))
                insert_data(db_connection, resource_categories_query, (resource_id, category_id))

        # DataTypes
        if not pd.isna(row['Types of Data']):
            data_types = row['Types of Data'].split(',')
            for data_type in data_types:
                data_type_exists = check_exists(db_connection, check_datatype_exists_query, (data_type,))
                if data_type_exists is not None:
                    data_type_id = data_type_exists[0]
                    print(data_type, " data type exists: data_type_id = ", data_type_id)
                else:
                    data_type_id = insert_data(db_connection, datatype_query, (data_type,))
                insert_data(db_connection, resource_datatypes_query, (resource_id, data_type_id))

        # Languages
        if not pd.isna(row['Languages']):
            languages = row['Languages'].split(',')
            for language in languages:
                language_exists = check_exists(db_connection, check_language_exists_query, (language,))
                if language_exists is not None:
                    language_id = language_exists[0]
                    print(language, " language exists: language_id = ", language_id)
                else:
                    language_id = insert_data(db_connection, language_query, (language,))
                insert_data(db_connection, resource_languages_query, (resource_id, language_id))

        # DataFormats
        if not pd.isna(row['DataFormats']):
            data_formats = row['DataFormats'].split(',')
            for data_format in data_formats:
                data_format_exists = check_exists(db_connection, check_dataformat_exists_query, (data_format,))
                if data_format_exists is not None:
                    data_format_id = data_format_exists[0]
                    print(data_format, " data format exists: data_format_id = ", data_format_id)
                else:
                    data_format_id = insert_data(db_connection, dataformat_query, (data_format,))
                insert_data(db_connection, resource_dataformats_query, (resource_id, data_format_id))

    # Close connection
    db_connection.close()
    print("SQLite connection is closed")
