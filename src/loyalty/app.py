import psycopg2

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

DB_URL = "postgresql://program:test@database:5432/loyalties"
# DB_URL = "postgresql://postgres:postgres@database:5432/postgres"

@app.route('/manage/health', methods=['GET'])
def health_check():
    return 200


@app.route('/api/v1/loyalty/<user>', methods=['POST'])
def add_loyalty(user:str):
    create_loyalty_db()
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select max(id) from loyalty")
            max_id = cursor.fetchone()
            cursor.execute(f"""
insert into loyalty (id, username, reservation_count, status, discount) values ({max_id[0] + 1}, '{user}', 0, 'BRONZE', 5)
""")
            conn.commit()
    return {
        "status":"BRONZE",
        "discount":5,
        "reservation_count":0
    }, 200


@app.route('/api/v1/loyalty/<user>', methods=['GET'])
def get_loyalty(user:str):
    create_loyalty_db()
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
select status, discount, reservation_count from loyalty loy where loy.username = '{user}'
""")
            loyalty = cursor.fetchone()
    if loyalty is None:
        return {}, 404
    loyalty = {
        "status":loyalty[0],
        "discount":loyalty[1],
        "reservation_count":loyalty[2]
    }
    return loyalty, 200


def create_loyalty_db():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
CREATE TABLE if not exists loyalty
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
                            f"VALUES (1, 'Test Max', 25, 'GOLD', 10) on conflict do nothing;")
            conn.commit()
    return


if __name__ == '__main__':
    app.run(port=8050)
