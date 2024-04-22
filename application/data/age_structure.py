import pandas as pd
from application.utils.tool import *

db = get_db()

df = pd.read_excel(r'age_structure.xls')

# covert to python dict
dt = df.to_dict('records')

print(dt)

for i in dt:
    print(i)

    res = db.table("age").add(i)

    if not res:
        print(db.showError())
