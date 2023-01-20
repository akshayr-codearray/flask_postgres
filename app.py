import psycopg2
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='mysecretpassword')
    return conn


class Emp(Resource):

    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM emp;')
        emp = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"employees": emp})

    def post(self):
        if request.is_json:
            data = request.get_json()
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO emp (name, email, salary, feedback)'
                        'VALUES (%s, %s, %s, %s)',
                        (data['name'], data['email'], data['sal'], data['feed'])
                        )

            conn.commit()
            cur.close()
            conn.close()


class OneEmp(Resource):

    def get(self, e_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM emp WHERE id = %s', (e_id,))
        emp_details = cur.fetchall()
        print(bool(emp_details))
        if not emp_details:
            return make_response({"message": f"emp with id {e_id} does not exist "}, 400)

        cur.close()
        conn.close()
        return jsonify({"emp": emp_details})

    def put(self, e_id):
        if request.is_json:
            user = request.get_json()
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('SELECT * FROM emp WHERE id = %s', (e_id,))
            emp_details = cur.fetchall()
            if not emp_details:
                return make_response({"message": f"emp with id {e_id} does not exist "}, 400)

            query = "UPDATE emp SET name=%s , email=%s , salary=%s , feedback=%s WHERE id=%s "
            cur.execute(query, (user['name'], user['email'], user['sal'], user['feed'], e_id))

            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": f'employee updated with id {e_id}'})

    def delete(self, e_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM emp WHERE id = %s', (e_id,))
        emp_details = cur.fetchall()
        if not emp_details:
            return make_response({"message": f"emp with id {e_id} does not exist "}, 400)

        del_query = "DELETE FROM emp WHERE id=%s "
        cur.execute(del_query, (e_id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": f'employee deleted with id {e_id}'})


api.add_resource(Emp, '/emp')
api.add_resource(OneEmp, '/one/<int:e_id>')

if __name__ == '__main__':
    app.run(debug=True)
