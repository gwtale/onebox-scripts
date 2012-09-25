
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    result=[
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    return result
    
