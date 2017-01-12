import csv
import sys

def AddDecimal(i):
  str_i = str(i)
  return str_i[:-2] + '.' + str_i[-2:]

if __name__ == "__main__":
  total_cents = None
  total_cash_cents = None
  symbol_to_cents = {}
  with open(sys.argv[1]) as csv_file:
    parsing_symbols = False
    market_value_index = None
    for row in csv.reader(csv_file):
      if parsing_symbols:
        symbol_to_cents[row[0]] = int(row[market_value_index].replace('.', ''))
      elif len(row) > 0:
        if row[0] == "Total Value":
          total_cents = int(row[1].replace('.', ''))
        elif row[0] == "Cash":
          total_cash_cents = int(row[1].replace('.', ''))
        elif row[0] == "Symbol":
          parsing_symbols = True
          for i in range(len(row)):
            if row[i] == 'Market Value':
              market_value_index = i
  total_cents_per_symbol = int(total_cents / len(symbol_to_cents))
  symbol_to_amount_to_add = {symbol: total_cents_per_symbol - cents for symbol, cents in symbol_to_cents.items()}
  print "TOTAL: %s" % (AddDecimal(total_cents))
  print "TOTAL CASH: %s" % (AddDecimal(total_cash_cents))
  total_new_investment_cents = sum(symbol_to_amount_to_add.values())
  print "TOTAL NEW INVESTMENT: %s" % (AddDecimal(total_new_investment_cents))
  if total_new_investment_cents > total_cash_cents:
    print "WARNING: investing too much!!!!"
    sys.exit(0)
  for symbol in sorted(symbol_to_cents.keys()):
    print "%s: %s" % (symbol, AddDecimal(symbol_to_amount_to_add[symbol]))
