import pandas as pd
from application.utils.tool import *

db = get_db()

df = pd.read_excel(r'birth_death.xls')

# covert to python dict
dt = df.to_dict('records')

print(dt)

for i in dt:
    print(i)

    res = db.table("birth_death").add(i)
