import pandas as pd
from application.utils.tool import *

df = pd.read_excel(r'total_people.xls')

# covert to python dict
dt = df.to_dict('records')
print(dt)

for i in dt:
    print(i)

    db = get_db()

    res = db.table("people").add(i)
