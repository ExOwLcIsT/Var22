from aifc import Error
from flask import Blueprint, jsonify, make_response, request, Response
import mysql
from mysql_connection.mysql_db import mydb

# Створюємо блупрінт
reqs_bp = Blueprint('reqs', __name__)


@reqs_bp.route('/req1', methods=['GET'])
def get_drivers():
    year = request.args.get('year', type=int)
    gender = request.args.get('gender', type=str)
    age_min = request.args.get('age_min', type=int)
    age_max = request.args.get('age_max', type=int)
    salary_min = request.args.get('salary_min', type=float)
    salary_max = request.args.get('salary_max', type=float)

    try:
        # Підключення до бази даних
        cursor = mydb.cursor(dictionary=True)

        # SQL запит для отримання даних
        query = """
        SELECT 
            ПІБ, стать, TIMESTAMPDIFF(YEAR,дата_народження,CURDATE()) as вік,
            кількість_дітей, зарплата, стаж , 
        FROM 
            працівники
        WHERE 
            посада = "Водій" """
        if (year != None):
            query+= f" AND  медогляд = {year} "
        if (gender != None):
            query+= f" AND  стать = {gender} "
        if (age_min != None and age_max!= None):
            query+= f" AND вік between {age_min} and {age_min} "
        if (salary_min != None and salary_max!= None):
            query+= f" AND  зарплата between {salary_min} and {salary_max} "
        print(query)
        cursor.execute(query)
        drivers_data = cursor.fetchall()

        results = []
        for driver in drivers_data:
            results.append(driver)

        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()


@reqs_bp.route('/req2', methods=['GET'])
def get_workers():
    experience_min = request.args.get('experience_min', type=int)
    experience_max = request.args.get('experience_max', type=int)
    gender = request.args.get('gender', type=str)
    age_min = request.args.get('age_min', type=int)
    age_max = request.args.get('age_max', type=int)
    children_min = request.args.get('children_min', type=int)
    children_max = request.args.get('children_max', type=int)
    salary_min = request.args.get('salary_min', type=float)
    salary_max = request.args.get('salary_max', type=float)

    try:
        # Підключення до бази даних
        cursor = mydb.cursor(dictionary=True)

        # SQL запит для отримання даних
        query = """
        SELECT 
            ПІБ, стать, дата_народження,
            кількість_дітей, зарплата, стаж 
        FROM 
            працівники 
        WHERE 
        ПІБ = ПІБ
        """
        if experience_min is not None and experience_max is not None:
            query += f" AND стаж BETWEEN {experience_min} AND {experience_max} "
        if gender:
            query += f" AND стать = {gender} "
        if age_min is not None and age_max is not None:
            query += f" AND TIMESTAMPDIFF(YEAR,дата_народження,CURDATE()) between {age_min} and {age_min}"
        if children_min is not None and children_max is not None:
            query += f" AND кількість_дітей BETWEEN {children_min} AND {children_max} "
        if salary_min is not None and salary_max is not None:
            query += f" AND зарплата BETWEEN {salary_min} AND {salary_max} "
        print(query)
        cursor.execute(query)
        print("yes")
        workers_data = cursor.fetchall()

        results = []
        for worker in workers_data:
            results.append(worker)

        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()