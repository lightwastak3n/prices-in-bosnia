import mysql.connector


def fix_serbian_letters(text):
    latin_chars = {
        "š": "s",
        "đ": "dj",
        "č": "c",
        "ć": "c",
        "ž": "z"
    }
    for char in text:
        if char in latin_chars:
            text = text.replace(char, latin_chars[char])
    return text


latin_characters = "šđčćž"

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="139.59.214.188",
    port="5231",
    database="prices", 
    user="cuber",
    password="pni5UnPvE8KBohB!"
)
# Define the SQL query
sql = "SELECT name FROM items"

# Execute the query
mycursor = mydb.cursor()
mycursor.execute(sql)

# Fetch the results and print them
results = mycursor.fetchall()
for result in results:
    if any(char in result[0] for char in latin_characters):
        new_name = fix_serbian_letters(result[0])
        print(new_name)
        update_sql = f"UPDATE items SET name = '{new_name}' WHERE name = '{result[0]}'"
        mycursor.execute(update_sql)
        mydb.commit()
    else:
        print(f"Good - {result[0]}")

# Close the database connection
mydb.close()
