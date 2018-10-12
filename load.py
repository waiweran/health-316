import psycopg2 as db
import xlrd

conn = db.connect(dbname='health')
cur = conn.cursor

book = xlrd.open_workbook(filename="Sample_316_Data.xlsx")
sheet_names = book.sheet_names()

for i in range(len(sheet_names)):
    sheet = book.sheet_by_index(i)
    name = sheet_names[i]
    titles = sheet.row(0)
    for row_idx in range(1, sheet.nrows):  # Iterate through rows
        curr_row = sheet.row(row_idx)
        write_row = [str(value)[str(value).index(':')+1:(str(value)+'.').index('.')] for value in curr_row]
        sql_code = 'INSERT INTO ' + name + ' VALUES '+ str(write_row).replace('[', '(').replace(']', ')').replace("'", "").replace('"', "'").replace('\\', '').lower() + ';'
        print(sql_code)
        #cur.execute(sql_code)

conn.close()


