from sql_server import Server

server = Server()

missing_ids_query = """select t4.id, t4.link from rs_links t4 left join houses t1 on t4.id = t1.id left join flats t2 on t4.id = t2.id left join land t3 on t4.id = t3.id where t1.id is 
null and t2.id is null and t3.id is null;"""


def do_query(query):
    server.create_connection()
    with server.connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    server.connection.commit()
    server.close_connection()
    return result


missing_ids = do_query(missing_ids_query)

ids_to_null = [listing[0] for listing in missing_ids if len(listing[1]) < 35]
ids_to_null = [str(i) for i in ids_to_null]

set_scraped_zero = """update rs_links set scraped = 0 where id in ({});""".format(
    ",".join(ids_to_null)
)

test = do_query(set_scraped_zero)
print(test)
