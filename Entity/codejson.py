import json
import psycopg2


# Function to encrypt JSON data and store it in the database
def encrypt_and_store_json(json_data, secret_key):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="your_database",
            user="your_user",
            password="your_password",
            host="your_host",
            port="your_port"
        )

        cursor = connection.cursor()

        # Encrypt the JSON data using pgp_sym_encrypt function
        cursor.execute("INSERT INTO encrypted_json (json_data) VALUES (pgp_sym_encrypt(%s::BYTEA, %s))",
                       (json.dumps(json_data), secret_key))

        connection.commit()

        cursor.close()
        connection.close()

        print("Data encrypted and stored successfully in the database.")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or performing encryption operations:", error)


# Define your JSON data and secret key
json_data = {"key": "value", "key2": "value2"}
secret_key = "your_secret_key"

# Call the function to encrypt and store the JSON data
encrypt_and_store_json(json_data, secret_key)
