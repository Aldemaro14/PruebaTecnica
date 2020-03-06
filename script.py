import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Database Connected!!!')

    except Error as e:
        print(e)

    return conn

def update_vendor(conn):

    vend_comp_A_to_B = conn.execute("""
            Select * FROM ventasA.vendedor
            WHERE cod_vendedor NOT IN
            (SELECT cod_vendedor from ventasB.vendedor)
        """).fetchall()

    vend_comp_B_to_A = conn.execute("""
            Select * FROM ventasB.vendedor
            WHERE cod_vendedor NOT IN
            (SELECT cod_vendedor from ventasA.vendedor)
        """).fetchall()

    vend_to_be_updated = []
    if(len(vend_comp_A_to_B) > 0):
        for i in vend_comp_A_to_B:
            vend_to_be_updated.append(i)
        
    if(len(vend_comp_B_to_A) > 0):
        for i in vend_comp_B_to_A:
            vend_to_be_updated.append(i)
          
          
    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasA.vendedor
            VALUES (?, ?, ?, ?)
        """,  vend_to_be_updated)

    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasB.vendedor
            VALUES (?, ?, ?, ?)
        """,  vend_to_be_updated)   

def update_product(conn):

    prod_comp_A_to_B = conn.execute("""
            Select * FROM ventasA.producto
            WHERE cod_producto NOT IN
            (SELECT cod_producto from ventasB.producto)
        """).fetchall()

    prod_comp_B_to_A = conn.execute("""
        Select * FROM ventasB.producto
        WHERE cod_producto NOT IN
        (SELECT cod_producto from ventasA.producto)
    """).fetchall()

    prod_to_be_updated = []
    if(len(prod_comp_A_to_B) > 0):
        for i in prod_comp_A_to_B:
            prod_to_be_updated.append(i)
        
    if(len(prod_comp_B_to_A) > 0):
        for i in prod_comp_B_to_A:
            prod_to_be_updated.append(i)
          
          
    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasA.producto
            VALUES (?, ?, ?)
        """,  prod_to_be_updated)

    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasB.producto
            VALUES (?, ?, ?)
        """,  prod_to_be_updated)

def update_sales(conn):

    sale_comp_A_to_B = conn.execute("""
            Select * FROM ventasA.venta
            WHERE cod_venta NOT IN
            (SELECT cod_venta from ventasB.venta)
        """).fetchall()

    sale_comp_B_toA = conn.execute("""
        Select * FROM ventasB.venta
        WHERE cod_venta NOT IN
        (SELECT cod_venta from ventasA.venta)
    """).fetchall()

    vent_to_be_updated = []
    if(len(sale_comp_A_to_B) > 0):
        for i in sale_comp_A_to_B:
            vent_to_be_updated.append(i)
        
    if(len(sale_comp_B_toA) > 0):
        for i in sale_comp_B_toA:
            vent_to_be_updated.append(i)
          
          
    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasA.producto
            VALUES (?, ?, ?, ?, ?)
        """,  vent_to_be_updated)

    conn.executemany(""" 
            INSERT OR IGNORE INTO ventasB.producto
            VALUES (?, ?, ?, ?, ?)
        """,  vent_to_be_updated)

def update(conn):

    update_vendor(conn)
    update_product(conn)
    update_sales(conn)

    print('compared!!!!')

    checkUp = conn.execute("""  
            SELECT * FROM ventasA.vendedor;
        """).fetchall()
    checkUp2 = conn.execute("""  
            SELECT * FROM ventasB.vendedor;
        """).fetchall()
    print('updated!!!!')
    print(checkUp)
    print(checkUp2)



def main():

    #Open database Connection
    db = create_connection("ventas.db")
    cursor_object = db.cursor()

    #Attach Databases
    try:
        attach_ventas_a = "ATTACH DATABASE ? AS ventasA;"
        attach_ventas_b = "ATTACH DATABASE ? AS ventasB;"

        database_a_file = ("ventas_a.db",)
        database_b_file = ("ventas_b.db",)

        cursor_object.execute(attach_ventas_a, database_a_file)
        cursor_object.execute(attach_ventas_b, database_b_file)


        print("Databases Attached!!!")

    except Error as e:
        print(e)
    

    #Check data
    update(cursor_object)
    db.commit()

    #Detach DB
    detachDatabase = "DETACH DATABASE ventasA"
    detachDatabase2 = "DETACH DATABASE ventasB"

    cursor_object.execute(detachDatabase)
    cursor_object.execute(detachDatabase2)

    

    #Close Database Connection
    db.close()
    print("Connection Closed")



if __name__ == '__main__':
    main()