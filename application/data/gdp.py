import pandas as pd
from application.utils.tool import *

db = get_db()

df = pd.read_excel(r'gdp.xls')

# covert to python dict
dt = df.to_dict('records')
print(dt)

for i in dt:
    print(i)

    year = i["year"]

    for k, v in i.items():
        if k == "year":
            continue

        res = db.table("gdp").add({
            "year": year,
            "province": k,
            "gdp": v
        })

        print(res)

        if not res:
            print(db.showError())
