import psycopg2

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

DB_URL = "postgresql://program:test@database:5432/loyalties"



def create_loyalty_db():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
CREATE TABLE loyalty
(
    id                SERIAL PRIMARY KEY,
    username          VARCHAR(80) NOT NULL UNIQUE,
    reservation_count INT         NOT NULL DEFAULT 0,
    status            VARCHAR(80) NOT NULL DEFAULT 'BRONZE'
        CHECK (status IN ('BRONZE', 'SILVER', 'GOLD')),
    discount          INT         NOT NULL
);
""")
            conn.commit()
            cursor.execute(f"INSERT INTO loyalty (id, username, reservation_count, status, discount) "
                            f"VALUES (1, 'Test Max', 25, 'GOLD', 10);")
            conn.commit()
    return


if __name__ == '__main__':
    create_loyalty_db()
    app.run(port=8050)
