import mysql.connector as mc
from tabulate import tabulate


def Create_Database():
    """This Function Creates Database"""
    cursor.execute("SHOW DATABASES")
    Databases = [DataBase[0] for DataBase in cursor]
    data_base = input("Enter Database Name:- ")
    while len(data_base.split()) >= 2 or data_base in Databases:
        if len(data_base.split()) >= 2:
            print("You Cannot Make Multi-Words Database, Kindly use a Single Word Name")
            data_base = input("Enter Database Name:- ")
        elif data_base in Databases:
            print("Entered Database Already exists, Kindly chose another Name")
            data_base = input("Enter Database Name:- ")
    cursor.execute(f"CREATE DATABASE {data_base};")
    print(f"Database '{data_base}' Created")
    return data_base


def print_table_rows(Cursor, table):
    """This Function Print Table in Tabular Form"""
    Cursor.execute(f"SELECT * FROM {table}")
    rows = Cursor.fetchall()
    print("\n", tabulate(rows, headers=Cursor.column_names))


def Create_Table():
    """This Function Creates a Table & Add Column To Them Dynamically"""
    table = input("\nEnter Table Name:- ")
    columns = list(map(str, input("Enter Column Name:- ").split()))
    datatypes = list(map(str, input("Enter Datatypes Respectively:- ").split()))
    cursor.execute(f"CREATE TABLE {table} ({columns[0]} {datatypes[0]})")
    for column, datatype in zip(columns[1:], datatypes[1:]):
        cursor.execute(f"ALTER TABLE {table} ADD {column} {datatype}")
    print("Table Created Successfully!")


def get_primary_key(Cursor, table_name):
    """This Function Return Primary Key Column of a Table"""
    # Query to get information about primary key columns
    Cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
    primary_keys = Cursor.fetchall()

    if primary_keys:
        # Extract column names from the result
        column_names = [key[4] for key in primary_keys]
        return column_names
    else:
        return None


def Update_Data(data_base):
    """This Function Update Row or a Particular Cell of a Table"""
    table = choose_table()
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{data_base}' AND TABLE_NAME = '{table}'")
    columns = [column[0] for column in cursor.fetchall()]
    primary_keys = get_primary_key(cursor, table)
    Choice = int(input("Enter 1 to Update Row & 2 to Update a Particular Cell:- "))

    # When Table Have a Primary key
    if primary_keys:
        print(f"The primary key for table '{table}' is: {', '.join(primary_keys)}")
        # To Update Whole Row
        if Choice == 1:
            print_table_rows(cursor, table)
            # Logic to update an entire row
            row_id = int(input(f"Enter {primary_keys[0]} value of the row you want to update: "))
            update_values = {}
            for column in columns:
                update_values[column] = input(f"Enter new value for '{column}': ")
            update_query = f"UPDATE {table} SET "
            for column, value in update_values.items():
                update_query += f"{column} = '{value}', "
            update_query = update_query[:-2] + f" WHERE {primary_keys[0]} = {row_id};"  # Removing the last comma and space in First String
            cursor.execute(update_query)
            my_db.commit()
            print("Row updated successfully!")
        # To Update a Particular Cell
        elif Choice == 2:
            for no, column in enumerate(columns, start=1):
                print("\t", no, "Column:- ", column)
            column_choice = int(input("Enter Column no. You Want to Update:- "))
            print_table_rows(cursor, table)
            row_id = int(input(f"Enter {primary_keys[0]} value of the row you want to update: "))
            new_value = input("Enter new value: ")
            column_name = columns[column_choice - 1]
            cursor.execute(f"UPDATE {table} SET {column_name} = '{new_value}' WHERE {primary_keys[0]} = {row_id};")
            my_db.commit()
            print("Cell updated successfully!")

    # When Table Doesn't Have a Primary key
    else:
        print(f"Table '{table}' does not have a primary key.")
        print("Please provide the following information to identify the row:")
        # To Update Whole Row
        if Choice == 1:
            where_conditions = {}
            print_table_rows(cursor, table)
            for column in columns:
                value = input(f"Enter value for '{column}':- ")
                where_conditions[column] = value

            update_values = {}
            print("\nEnter new values for the row:")
            for column in columns:
                new_value = input(f"Enter new value for '{column}':- ")
                update_values[column] = new_value

            update_query = f"UPDATE {table} SET "
            for column, value in update_values.items():
                update_query += f"{column} = '{value}', "
            update_query = update_query[:-2]  # Remove the last comma and space

            where_clause = " AND ".join([f"{column} = '{value}'" for column, value in where_conditions.items()])
            update_query += f" WHERE {where_clause};"
            cursor.execute(update_query)
            my_db.commit()
            print("Row updated successfully!")
        # To Update a Particular Cell
        elif Choice == 2:
            where_conditions = {}
            print_table_rows(cursor, table)
            for column in columns:
                value = input(f"Enter value for '{column}': ")
                where_conditions[column] = value

            print("From Following Columns:- ")
            for no, column in enumerate(columns, start=1):
                print("\t", no, column)
            column_choice = int(input("Enter Column no. You Want to Update:- "))
            column_name = columns[column_choice - 1]
            new_value = input(f"Enter New value for Column '{column_name}':- ")

            where_clause = " AND ".join([f"{column} = '{value}'" for column, value in where_conditions.items()])
            update_query = f"UPDATE {table} SET {column_name} = '{new_value}' WHERE {where_clause}"
            cursor.execute(update_query)
            my_db.commit()
            print("Cell Updated Successfully")


def choose_table():
    """This Function Show Tables & Take User's Choice"""
    tables = []
    # SHOW TABLES FOR USER's CHOICE
    cursor.execute("SHOW TABLES")
    print("\nSelect Table:-")
    for number, table in enumerate(cursor, start=1):
        tables.append(list(table)[0])
        print("\t", number, list(table)[0])
    chose_table = int(input("\nEnter Table no.:- "))
    table = tables[chose_table - 1]
    print("Table:-", table)
    return table


def Add_Data(data_base):
    """This Function Add Data to Table Dynamically"""
    # SHOW COLUMNS OF TABLE & ADD VALUE TO THEM DYNAMICALLY
    columns = []
    table = choose_table()
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{data_base}' AND TABLE_NAME = '{table}'")
    for Table in cursor:
        columns.append(list(Table)[0])
        print("Column:- ", list(Table)[0])
    iterate = int(input("How Many Times you Want to Add Value:- "))
    for _ in range(iterate):  #
        Values = []  # To Stored Columns Values are
        for index in range(len(columns)):
            while True:
                user_value = input(f"Add Value To Column '{columns[index]}':- ")
                Values.append(user_value)
                cursor.execute(f"SHOW INDEX FROM {table} WHERE Non_unique = 0;")
                unique_columns = []
                for x in cursor:
                    unique_columns.extend(filter(None, map(lambda column: column if column in x else None, columns)))
                cursor.execute(f"SELECT {unique_columns[0]} from {table};")
                unique_columns_values = [value[0] for value in cursor]
                if user_value in unique_columns_values:
                    print(f"You cannot enter same value in a unique column '{columns[index]}'")
                    continue
                elif user_value not in unique_columns_values:
                    break
        cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(Values))})", Values)
        print("Data Added Successfully!")


def Retrieve_Data():
    """This Function Show Table Data in Tabular Format"""
    cursor.execute(f"SHOW TABLES FROM school_management")
    tables = []
    print("\nSelect Table: ")
    for num, table in enumerate(cursor, start=1):
        tables.append(table[0])
        print("\t", num, table[0])
    if len(tables) == 0:
        print("Sorry, There are no table to Show in the database")
    elif len(tables) > 0:
        table_choice = int(input("\nEnter Table No:- "))
        print(tables[table_choice - 1])
        print_table_rows(cursor, tables[table_choice - 1])


if __name__ == '__main__':
    Database = None
    print("Welcome to Python MySQL\nChoose Database:- ")
    # SHOWING DATABASE & GETTING USER'S INPUT
    my_db = mc.connect(host="localhost", user="root", password="nitin123", auth_plugin='mysql_native_password')
    cursor = my_db.cursor()
    choice = input("Wanna work on New Database or On Pre-Existed Database(Y/N):- ")
    if choice in ("y", "Y"):
        Database = Create_Database()
        my_db = mc.connect(host="localhost", user="root", password="nitin123", database=Database, auth_plugin='mysql_native_password')
        cursor = my_db.cursor()
    elif choice in ("n", "N"):
        cursor.execute("SHOW DATABASES")
        databases, no = [], 1
        for database in cursor:
            databases.append(database)
            print("\t", no, database[0])
            no += 1
        database_choice = int(input("\nEnter Database no:- "))
        Database = databases[database_choice - 1][0]
        my_db = mc.connect(host="localhost", user="root", password="nitin123", database=Database, auth_plugin='mysql_native_password')
        cursor = my_db.cursor()

    # MAIN PROGRAM
    while True:
        print("""ENTER:- 
    1 to Create Database
    2 to Create Table
    3 to Update Data
    4 to Add Data
    5 to Retrieve Data
    0 to Quit""")

        choice = int(input("What do you like to do: "))
        if choice == 1:
            Create_Database()
        elif choice == 2:
            Create_Table()
        elif choice == 3:
            Update_Data(Database)
        elif choice == 4 and Database is not None:
            Add_Data(Database)
        elif choice == 5:
            Retrieve_Data()
        elif choice == 0:
            break
        else:
            print("Invalid Input")
        my_db.commit()

# TODO: Refactor function Update_data & Add_data code for better readability
