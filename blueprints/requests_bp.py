from datetime import datetime
from flask import Blueprint, jsonify, request
import mysql
from mysql_connection.mysql_db import mydb

# Створюємо блупрінт
reqs_bp = Blueprint('reqs', __name__)


@reqs_bp.route('/req1', methods=['GET'])
def get_req1():
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
            query += f" AND  медогляд = {year} "
        if (gender != None):
            query += f" AND  стать = {gender} "
        if (age_min != None and age_max != None):
            query += f" AND вік between {age_min} and {age_min} "
        if (salary_min != None and salary_max != None):
            query += f" AND  зарплата between {salary_min} and {salary_max} "
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
def get_req2():
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
            query += f" AND стаж BETWEEN {
                experience_min} AND {experience_max} "
        if gender:
            query += f" AND стать = {gender} "
        if age_min is not None and age_max is not None:
            query += f" AND TIMESTAMPDIFF(YEAR,дата_народження,CURDATE()) between {
                age_min} and {age_min}"
        if children_min is not None and children_max is not None:
            query += f" AND кількість_дітей BETWEEN {
                children_min} AND {children_max} "
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


@reqs_bp.route('/req3', methods=['GET'])
def get_req3():
    arrival_time = request.args.get('arrival_time')
    min_routes = request.args.get('min_routes', type=int)

    # SQL запит з фільтрацією
    query = """
        SELECT 
            Локомотиви.id, 
            Локомотиви.серійний_номер, 
            Локомотиви.модель, 
            Локомотиви.рік_виробництва, 
            COUNT(Розклад.id) AS кількість_маршрутів
        FROM 
            Локомотиви 
        LEFT JOIN 
            Розклад ON Локомотиви.id = Розклад.маршрут_id
        WHERE 
            (%s IS NULL OR Розклад.час_прибуття <= %s)
        GROUP BY 
            Локомотиви.id
    """

    params = (arrival_time, arrival_time)

    if min_routes is not None:
        query += ' HAVING кількість_маршрутів >= %s'
        params += (min_routes,)

    # Виконання запиту до бази даних
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query, params)
        locomotives = cursor.fetchall()
        total_count = len(locomotives)

        # Закриття курсору
        cursor.close()

        # Відповідь у форматі JSON
        return jsonify({'totalCount': total_count, 'locomotives': locomotives})

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({'error': 'Server Error'}), 500


@reqs_bp.route('/req4', methods=['GET'])
def req4():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        repair_date = request.args.get('repair_time')
        repair_count = request.args.get('repair_count', 'NULL', type=int)
        min_routes = request.args.get('min_routes', 'NULL', type=int)
        min_age = request.args.get('min_age', 'NULL', type=int)

        cursor = mydb.cursor()
        print(start_date)
        if start_date != '':
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date != '':
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        if repair_date != '':
            repair_date = datetime.strptime(repair_date, "%Y-%m-%d").date()
        print([start_date, end_date, repair_date,
              min_routes, min_routes, min_age])
        query = f'''
                        SELECT Локомотиви.id, Локомотиви.серійний_номер, Локомотиви.модель, Локомотиви.рік_виробництва, COUNT(Техогляди.id) AS кількість_ремонтів
                        FROM Локомотиви
                        JOIN Техогляди ON Локомотиви.id = Техогляди.локомотив_id
                        WHERE Техогляди.дата_техогляду BETWEEN DATE('{start_date}') AND DATE('{end_date}')
                        AND (DATE('{repair_date}') IS NULL OR DATE(Техогляди.дата_техогляду) = DATE('{repair_date}'))
                        GROUP BY Локомотиви.id
                        HAVING ({repair_count} IS NULL OR COUNT(Техогляди.id) >= {repair_count})
                        AND ({min_age} IS NULL OR (YEAR(CURDATE())-Локомотиви.рік_виробництва) >= {min_age})
                    '''
        print(query)
        cursor.execute(query)

        locomotives = cursor.fetchall()
        total_count = cursor.rowcount
        cursor.close()

        return jsonify({
            "totalCount": total_count,
            "locomotives": locomotives
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@reqs_bp.route('/req5', methods=['GET'])
def get_req5():
    try:
        # Отримуємо параметри з запиту
        route_id = request.args.get('route_id')
        date = request.args.get('date')
        schedule_id = request.args.get('schedule_id')

        cursor = mydb.cursor()
        print(route_id)
        print(date)
        print(schedule_id)
        # SQL-запит на непродані та здані квитки
        query = f'''
            SELECT Квитки.id, Квитки.номер_місця, Квитки.статус_квитка
            FROM Квитки
            JOIN Розклад ON Квитки.розклад_id = Розклад.id
            WHERE Квитки.розклад_id = {schedule_id}
              AND DATE(Квитки.дата_покупки) = DATE('{date}')
              AND Розклад.маршрут_id = {route_id}
              AND Квитки.статус_квитка IN ('booked', 'returned')
        '''
        print(query)
        cursor.execute(query)
        tickets = cursor.fetchall()
        print(tickets)
        # Підрахунок непроданих та зданих квитків
        unsold_tickets = [
            ticket for ticket in tickets if ticket[2] == 'booked']
        returned_tickets = [
            ticket for ticket in tickets if ticket[2] == 'returned']

        # Формування відповіді
        response = {
            "unsold_tickets_count": len(unsold_tickets),
            "returned_tickets_count": len(returned_tickets),
            "tickets": tickets
        }

        return jsonify(response)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500


@reqs_bp.route('/req6', methods=['GET'])
def get_req6():
    departure_date = request.args.get('date')

    try:
        date_obj = datetime.strptime(departure_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    cursor = mydb.cursor()

    query = f'''
        SELECT
            Пасажири.ПІБ,
            Пасажири.стать,
            YEAR(CURDATE()) - YEAR(Пасажири.дата_народження) AS вік,
            Пасажири.багаж
        FROM
            Квитки
        JOIN
            Розклад ON Квитки.розклад_id = Розклад.id
        JOIN
            Пасажири ON Квитки.пасажир_id = Пасажири.id
        WHERE
            DATE(Розклад.час_відправлення) = DATE('{date_obj}')
            AND Розклад.маршрут_id IN (
                SELECT id FROM Маршрути WHERE тип_маршруту = 'international'
            )
    '''
    cursor.execute(query)
    passengers = cursor.fetchall()
    cursor.close()
    print(passengers)
    print(len(passengers))
    return jsonify({
        'total_passengers': len(passengers),
        'passengers': passengers
    })


@reqs_bp.route('/req7', methods=['GET'])
def get_req7():
    маршрут_id = request.args.get('маршрут_id', type=int)
    мін_ціна = request.args.get('мін_ціна', type=float)
    макс_ціна = request.args.get('макс_ціна', type=float)

    # Підключення до бази даних
    try:
        cursor = mydb.cursor()

        cursor.execute('''
            SELECT 
                Розклад.номер_поїзда,
                Розклад.час_відправлення,
                Розклад.час_прибуття,
                TIMESTAMPDIFF(MINUTE, Розклад.час_відправлення, Розклад.час_прибуття) AS тривалість,
                Розклад.ціна_квитка
            FROM 
                Розклад
            JOIN 
                Маршрути ON Розклад.маршрут_id = Маршрути.id
            WHERE 
                Маршрути.id = %s
                AND Розклад.ціна_квитка BETWEEN %s AND %s
            ORDER BY 
                тривалість;
        ''', (маршрут_id, мін_ціна, макс_ціна))

        trains = cursor.fetchall()
        total_trains = len(trains)

        return jsonify({
            'total_trains': total_trains,
            'trains': trains
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()


@reqs_bp.route('/req8', methods=['GET'])
def get_req8():
    brigade_id = request.args.get('brigade_id', type=int)

    if brigade_id is None:
        return jsonify({'error': 'Необхідно вказати id бригади'}), 400

    try:
        cursor = mydb.cursor()

        # Отримання працівників
        cursor.execute(f'''
            SELECT
                Працівники.id,
                Працівники.ПІБ,
                Працівники.стать,
                Працівники.дата_народження,
                Працівники.зарплата,
                Працівники.посада,
                Бригади.назва AS бригада
            FROM
                Працівники
            JOIN
                Бригади ON Працівники.бригада_id = Бригади.id
            WHERE
                Бригади.id = {brigade_id};
        ''')
        workers = cursor.fetchall()

        # Отримання загальної кількості та середньої зарплати
        cursor.execute(f'''
            SELECT
                COUNT(*) AS total_workers,
                AVG(зарплата) AS average_salary
            FROM
                Працівники
            WHERE
                бригада_id = {brigade_id};
        ''')
        stats = cursor.fetchone()
        print(stats)
        return jsonify({
            'total_workers': stats[0],
            'average_salary': stats[1],
            'workers': workers
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()


@reqs_bp.route('/req9', methods=['GET'])
def get_req9():
    route_id = request.args.get('route_id', type=int)
    delay_reason = request.args.get('delay_reason', type=str)

    if route_id is None:
        return jsonify({'error': 'Необхідно вказати id маршруту'}), 400

    try:
        cursor = mydb.cursor()

        # Get canceled trips for the specified route
        cursor.execute(f'''
            SELECT
                COUNT(*) AS total_canceled,
                GROUP_CONCAT(номер_поїзда) AS canceled_trains
            FROM
                Розклад
            WHERE
                маршрут_id = {route_id} AND статус = 'canceled';
        ''')
        canceled_trips = cursor.fetchone()

        # Get delayed trips for the specified route and reason
        cursor.execute(f'''
            SELECT
                COUNT(*) AS total_delayed,
                GROUP_CONCAT(номер_поїзда) AS delayed_trains,
                COUNT(Квитки.id) AS total_refunded_tickets
            FROM
                Розклад
            LEFT JOIN
                Квитки ON Розклад.id = Квитки.розклад_id
            WHERE
                маршрут_id = {route_id} AND статус = 'delayed'
                AND (причина_затримки = '{delay_reason}' OR '{delay_reason}' IS NULL);
        ''')
        delayed_trips = cursor.fetchone()

        return jsonify({
            'canceled_trips': canceled_trips,
            'delayed_trips': delayed_trips
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()


@reqs_bp.route('/req10', methods=['GET'])
def get_ticket_sales():
    try:
        # Get parameters from the query string
        start_date = request.args.get('start_date')  # Expected format: YYYY-MM-DD
        end_date = request.args.get('end_date')      # Expected format: YYYY-MM-DD
        # Route ID to filter by
        route_id = request.args.get('route_id', type=int)

        # Validate the input dates
        try:
            print(start_date)
            print(end_date)
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        cursor = mydb.cursor()

        # Query to get the list and average of tickets sold
        query = f"""
        SELECT 
            Розклад.номер_поїзда,
            COUNT(Квитки.id) AS total_sold,
            AVG(Розклад.ціна_квитка) AS average_price
        FROM 
            Квитки
        JOIN 
            Розклад ON Квитки.розклад_id = Розклад.id
        WHERE 
            Розклад.час_відправлення BETWEEN DATE('{start_date}') AND DATE('{end_date}')
            AND Розклад.маршрут_id = {route_id}
        GROUP BY 
            Розклад.номер_поїзда;
        """
        print(query)
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()

        return jsonify(results), 200
    except Exception  as ex:
        print(ex)
        return jsonify({"message": "Error"}), 400


@reqs_bp.route('/queries', methods=['GET', 'POST'])
def query():
    cursor = mydb.cursor()
    
    query_data = request.json.get('query')
    if not query_data:
        return jsonify({"error": "Query text is required"}), 400
        
    try:
        cursor.execute(query_data)
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500
    finally:
            cursor.close()