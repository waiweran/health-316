import psycopg2 as db
import xlrd

conn = db.connect(dbname='health')
cur = conn.cursor

def read_line(sheetName, line):
	sql_code = 'INSERT INTO ' + sheetName + ' VALUES '+ str(line).replace('[', '(').replace(']', ')') + ';'
	cur.execute(sql_code)

def parse_sheet(name, sheet):
    titles = sheet.row(0)
    print(titles)
    for row_idx in range(1, sheet.nrows):  # Iterate through rows
        curr_row = sheet.row(row_idx)
        read_line(name, curr_row)


book = xlrd.open_workbook(filename="Sample_316_Data.xlsx")
sheet_names = book.sheet_names()

for i in range(1):
    curr_sheet = book.sheet_by_index(i)
    curr_sheet_name = sheet_names[i]
    parse_sheet(curr_sheet_name, curr_sheet)
conn.close()


