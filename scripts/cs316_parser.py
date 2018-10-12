import xlrd

def parse_excel_doc():
    book = xlrd.open_workbook(filename="Sample_316_Data.xlsx")
    sheet_names = book.sheet_names()

    for i in range(1):
        curr_sheet = book.sheet_by_index(i)
        curr_sheet_name = sheet_names[i]
        parse_sheet(curr_sheet_name, curr_sheet)


def parse_sheet(name, sheet):
    titles = sheet.row(0)
    print(titles)
    for row_idx in range(1, sheet.nrows):  # Iterate through rows
        curr_row = sheet.row(row_idx)
        read_line(name, curr_row)


def read_line(sheet_name, curr_row):
    print(sheet_name, curr_row)


parse_excel_doc()
