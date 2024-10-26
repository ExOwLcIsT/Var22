from flask import Blueprint, jsonify, request
import mysql
from mysql_connection.mysql_db import mydb

# Створюємо блупрінт
station_bp = Blueprint('station', __name__)


# Ендпоїнт для отримання назв таблиць (колекцій)
@station_bp.route('/get-tables', methods=['GET'])
def get_tables():
    try:
        # Підключаємось до бази даних
        mycursor = mydb.cursor()

        # Виконуємо запит для отримання назв таблиць
        mycursor.execute("SHOW TABLES")

        # Отримуємо результат та форматуємо у список
        tables = [table[0] for table in mycursor.fetchall()]

        # Закриваємо з'єднання
        mycursor.close()
        # Повертаємо результат як JSON
        return jsonify(tables)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@station_bp.route('/rename-table', methods=['PUT'])
def rename_table():
    try:
        old_name = request.json.get('old_name')
        new_name = request.json.get('new_name')

        if not old_name or not new_name:
            return jsonify({'error': 'Both old_name and new_name are required'}), 400

        # Підключаємось до бази даних
        mycursor = mydb.cursor()

        # SQL-запит для перейменування таблиці
        rename_query = f"RENAME TABLE {old_name} TO {new_name}"
        mycursor.execute(rename_query)

        mydb.commit()

        # Закриваємо з'єднання
        mycursor.close()

        return jsonify({'message': f'Table {old_name} renamed to {new_name} successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# Ендпоїнт для видалення таблиці


@station_bp.route('/delete-table', methods=['DELETE'])
def delete_table():
    try:
        table_name = request.json.get('table_name')

        if not table_name:
            return jsonify({'error': 'table_name is required'}), 400

        # Підключаємось до бази даних
        mycursor = mydb.cursor()

        # SQL-запит для видалення таблиці
        delete_query = f"DROP TABLE {table_name}"
        mycursor.execute(delete_query)

        mydb.commit()

        # Закриваємо з'єднання
        mycursor.close()

        return jsonify({'message': f'Table {table_name} deleted successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@station_bp.route('/add-table', methods=['POST'])
def add_table():
    try:
        table_name = request.json.get('table_name')

        # Формуємо SQL-запит для створення таблиці
        column_definitions = "id INT PRIMARY KEY AUTO_INCREMENT"
        create_query = f"CREATE TABLE {table_name} ({column_definitions})"

        mycursor = mydb.cursor()
        mycursor.execute(create_query)
        mydb.commit()
        mycursor.close()

        return jsonify({'message': f'Table {table_name} created successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@station_bp.route('/get-columns/<table_name>', methods=['GET'])
def get_columns(table_name):
    if not table_name:
        return jsonify({'error': 'Table name is required'}), 400

    try:
        mycursor = mydb.cursor()

        # Query to retrieve column information
        query = f"SHOW COLUMNS FROM {table_name}"
        mycursor.execute(query)
        columns = mycursor.fetchall()
        # Format result to include column name and type
        columns = [{'name': column[0], 'type': column[1]}
                   for column in columns]
        mycursor.close()
        return jsonify(columns), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# Ендпоїнт для додавання нового поля до таблиці
@station_bp.route('/add-column', methods=['POST'])
def add_column():
    try:
        table_name = request.json.get('table_name')
        column_name = request.json.get('column_name')
        column_type = request.json.get('column_type', 'VARCHAR(255)')
        not_null = request.json.get('not_null', False)

        if not table_name or not column_name:
            return jsonify({'error': 'table_name and column_name are required'}), 400

        # Формуємо SQL-запит з опцією NOT NULL, якщо вказано
        not_null_option = "NOT NULL" if not_null else ""
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN {
            column_name} {column_type} {not_null_option}"

        mycursor = mydb.cursor()
        mycursor.execute(add_column_query)
        mydb.commit()
        mycursor.close()

        return jsonify({'message': f'Column {column_name} added to table {table_name} successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# Ендпоїнт для видалення поля з таблиці
@station_bp.route('/delete-column', methods=['DELETE'])
def delete_column():
    try:
        table_name = request.json.get('table_name')
        column_name = request.json.get('column_name')

        if not table_name or not column_name:
            return jsonify({'error': 'table_name and column_name are required'}), 400

        # SQL-запит для видалення поля
        delete_column_query = f"ALTER TABLE {
            table_name} DROP COLUMN {column_name}"

        mycursor = mydb.cursor()
        mycursor.execute(delete_column_query)
        mydb.commit()
        mycursor.close()

        return jsonify({'message': f'Column {column_name} deleted from table {table_name} successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# Ендпоїнт для перейменування поля таблиці


@station_bp.route('/rename-column', methods=['PUT'])
def rename_column():
    try:
        table_name = request.json.get('table_name')
        old_column_name = request.json.get('old_name')
        new_column_name = request.json.get('new_name')
        # Specify column type, as it's required in MySQL
        column_type = request.json.get('column_type', 'VARCHAR(255)')

        if not table_name or not old_column_name or not new_column_name:
            return jsonify({'error': 'table_name, old_column_name, and new_column_name are required'}), 400

        # SQL-запит для перейменування поля
        rename_column_query = f"ALTER TABLE {table_name} CHANGE {
            old_column_name} {new_column_name} {column_type}"

        mycursor = mydb.cursor()
        mycursor.execute(rename_column_query)
        mydb.commit()
        mycursor.close()

        return jsonify({'message': f'Column {old_column_name} renamed to {new_column_name} in table {table_name} successfully'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@station_bp.route('/get-rows/<table_name>', methods=['GET'])
def getRows(table_name):
    mycursor = mydb.cursor()
    mycursor.execute("select * from " + table_name)
    myresult = mycursor.fetchall()
    mycursor.close()
    return jsonify(myresult)


@station_bp.route('/add-row/<table_name>', methods=['POST'])
def add_row(table_name):
    new_row = request.json
    columns = ', '.join(new_row.keys())
    values = list(new_row[key] for key in new_row)  # Use a list comprehension to keep values in their original types

    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({str(values)[1:-1]})"
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        mydb.commit()
        return jsonify({'message': 'Row added successfully', 'id': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        print('Error:', err)
        return jsonify({'message': 'Error adding row'}), 500
    finally:
        cursor.close()


@station_bp.route('/delete-row/<table_name>/<row_id>', methods=['DELETE'])
def delete_row(table_name, row_id):
    print(table_name, row_id)
    sql = f"DELETE FROM {table_name} WHERE id = {row_id}"

    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        mydb.commit()

        if cursor.rowcount == 1:
            return jsonify({'message': 'Row deleted successfully'}), 200
        else:
            return jsonify({'message': 'Row not found'}), 404
    except Exception as err:
        print('Error:', err)
        return jsonify({'message': 'Error deleting row'}), 500
    finally:
        cursor.close()

@station_bp.route('/update-row/<table_name>/<int:row_id>', methods=['PUT'])
def update_row(table_name, row_id):
    updated_data = request.json
    set_clause = ', '.join(
        [f"{column} = %s" for column in updated_data.keys()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"

    try:
        cursor = mydb.cursor()
        cursor.execute(sql, list(updated_data.values()) + [row_id])
        mydb.commit()

        if cursor.rowcount == 1:
            return jsonify({'message': 'Row updated successfully'}), 200
        else:
            return jsonify({'message': 'Row not found'}), 404
    except mysql.connector.Error as err:
        print('Error:', err)
        return jsonify({'message': 'Error updating row'}), 500
    finally:
        cursor.close()
