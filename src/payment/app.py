import psycopg2


DB_URL = "postgresql://program:test@database:5432/payments"



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