import psycopg2 as db
import xlrd

conn = db.connect(dbname='health')
cur = conn.cursor

book = xlrd.open_workbook(filename="Sample_316_Data.xlsx")
sheet_names = book.sheet_names()

for i in range(1):
    sheet = book.sheet_by_index(i)
    name = sheet_names[i]
    titles = sheet.row(0)
    print(titles)
    for row_idx in range(1, sheet.nrows):  # Iterate through rows
        curr_row = sheet.row(row_idx)
        read_line(name, curr_row)
        sql_code = 'INSERT INTO ' + name + ' VALUES '+ str(curr_row).replace('[', '(').replace(']', ')') + ';'
        cur.execute(sql_code)

conn.close()


