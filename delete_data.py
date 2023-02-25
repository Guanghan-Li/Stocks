from src.stock.repos.price_database import PricesDatabase
from src.stock.repos.report_database import ReportDatabase

#pd = PricesDatabase(log=True)
rd = ReportDatabase(log=True)
#pd.deleteAll()
rd.deleteAll()
print("DONE")