import xlwings as xw

#wb = workbook
#s = sheet

smif_wb = xw.Book("SMIF Portfolio Tracker.xlsx")

portfolio_s = smif_wb.sheets["Portfolio"]

#data_range = portfolio_s.range('A1:I34')
data_range = portfolio_s.range('B6:I6')

data = data_range.value #understand why this is needed, how does data_range store data normally if I didn't have this?

print(data)