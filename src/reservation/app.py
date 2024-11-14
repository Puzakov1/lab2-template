import psycopg2

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

DB_URL = "postgresql://program:test@database:5432/reservations"
# DB_URL = "postgresql://postgres:postgres@database:5432/postgres"


@app.route('/manage/health', methods=['GET'])
def health_check():
    return 200


@app.route('/api/v1/hotels', methods=['GET'])
def get_hotels():
    page = request.args["page"]
    size = request.args["size"]
    create_reservation_db()
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
select id, hotel_uid, name, country, city, address, stars, price from hotels
""")
            hotels = cursor.fetchall()
    hotel_list=[]
    for i, hotel in enumerate(hotels):
        if i < (page-1)*size:
            continue
        if i > page*size:
            break
        hotel_list.append(
            {
                "id":hotel[0],
                "hotel_uid":hotel[1],
                "name":hotel[2],
                "country":hotel[3],
                "city":hotel[4],
                "address":hotel[5],
                "stars":hotel[6],
                "price":hotel[7]
            }
        )
    return hotel_list, 200


def create_reservation_db():
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
CREATE TABLE if not exists reservation
(
    id              SERIAL PRIMARY KEY,
    reservation_uid uuid UNIQUE NOT NULL,
    username        VARCHAR(80) NOT NULL,
    payment_uid     uuid        NOT NULL,
    hotel_id        INT REFERENCES hotels (id),
    status          VARCHAR(20) NOT NULL
        CHECK (status IN ('PAID', 'CANCELED')),
    start_date      TIMESTAMP WITH TIME ZONE,
    end_data        TIMESTAMP WITH TIME ZONE
);

CREATE TABLE if not exists hotels
(
    id        SERIAL PRIMARY KEY,
    hotel_uid uuid         NOT NULL UNIQUE,
    name      VARCHAR(255) NOT NULL,
    country   VARCHAR(80)  NOT NULL,
    city      VARCHAR(80)  NOT NULL,
    address   VARCHAR(255) NOT NULL,
    stars     INT,
    price     INT          NOT NULL
);
""")
            conn.commit()
            cursor.execute(f"INSERT INTO hotels (id, hotel_uid, name, country, city, address, stars, price) "
                            f"VALUES (1, '049161bb-badd-4fa8-9d90-87c9a82b0668', 'Ararat Park Hyatt Moscow', 'Россия', 'Москва', 'Неглинная ул., 4', 5, 10000) on conflict do nothing;")
            conn.commit()
    return


if __name__ == '__main__':
    app.run(port=8070)
