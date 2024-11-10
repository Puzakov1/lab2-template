import psycopg2

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

DB_URL = "postgresql://program:test@database:5432/payments"


@app.route('/manage/health', methods=['GET'])
def health_check():
    return 200


def create_payment_db():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
CREATE TABLE payment
(
    id          SERIAL PRIMARY KEY,
    payment_uid uuid        NOT NULL,
    status      VARCHAR(20) NOT NULL
        CHECK (status IN ('PAID', 'CANCELED')),
    price       INT         NOT NULL
);
""")
            conn.commit()
    return


if __name__ == '__main__':
    create_payment_db()
    app.run(port=8060)
