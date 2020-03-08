import pyodbc
# загоняем файл в MS SQL Server в виде таблицы
conn = pyodbc.connect(
    "DRIVER={SQL Server Native Client 11.0};"
    "Server=PASHOK-ПК\SQLEXPRESS;"
    "Database=Primer;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute("select TOP(5) column2, count(*) from hits group by column2 order by count(*) desc")
for row in cursor:
    print(row)

conn.close()