import os
import pandas as pd
from flask import session, redirect, current_app
from flask import Blueprint
from flask import request
from ..utils.tool import *

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    if request.path.startswith('/api'):
        if request.path not in ['/api/login', '/api/register']:
            if 'user' not in session:
                return jsonResponse(401, 'Unauthorized', None)
    return None


@api.route('/')
@api.route('/index')
def index():
    return redirect('./index.html')


@api.route('/api/login', methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = db.table('user').where({"username|email": username, "password": password}).find()

    if user is None:
        return jsonResponse(500, 'account or password error', None)

    db.close()
    session['user'] = user  # save user session
    return jsonResponse(200, 'success', user)


@api.route('/api/register', methods=["POST"])
def register():
    db = get_db()
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    user = db.table('user').where({"username": username, "password": password}).find()

    if user:
        return jsonResponse(500, 'User already exists', None)

    # create user
    res = db.table('user').add({
        "username": username,
        "password": password,
        "email": email
    })

    db.close()
    if res:
        return jsonResponse(200, 'Register success', None)
    return jsonResponse(500, 'Register failed', user)


@api.route('/api/upload', methods=["POST"])
def upload():
    if not request.files['file'] or request.files['file'] == '':
        return jsonResponse(500, "Not found file")
    file = request.files['file']

    if "." not in file.filename:
        return jsonResponse(500, "Not found file type")

    file_type = file.filename.split(".")[-1]
    save_name = md5(file.filename + str(time.time())) + '.' + file_type
    save_path = '/static/uploads/files/' + save_name

    if not os.path.exists(current_app.root_path + '/static/uploads/files/'):
        os.makedirs(current_app.root_path + '/static/uploads/files/')

    file.save(current_app.root_path + save_path)
    return jsonResponse(200, "upload success", '/uploads/files/' + save_name)


@api.post('/api/import')
def _import():
    data = request.form.to_dict()
    if not data:
        return jsonResponse(500, "Not found data")

    table = data.get("data")
    file = data.get("file")

    db = get_db()

    df = pd.read_excel(current_app.root_path + "/static" + file)
    data = df.to_dict(orient='records')

    count = db.table(table).count()

    if count > 0:
        # delete all data from database
        res = db.table(table).where("id > 0").delete()

        if not res:
            print(db.showError())
            return jsonResponse(500, "import failed,Initialization Data failed")

    res = db.table(table).addAll(data)

    if not res:
        print(db.showError())
        return jsonResponse(500, "import failed")

    db.close()

    return jsonResponse(200, "Import success")


@api.get('/api/export')
def export():
    data = request.args.to_dict()
    if not data:
        return jsonResponse(500, "Not found data")

    table = data.get("data")
    db = get_db()
    data = db.table(table).select()

    df = pd.DataFrame(data)
    save_name = table + "_" + md5(str(time.time())) + '.xlsx'
    save_path = '/static/uploads/files/' + save_name
    df.to_excel(current_app.root_path + save_path, index=False)
    return jsonResponse(200, "export success", '/uploads/files/' + save_name)


@api.route('/api/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return jsonResponse(200, 'success', None)


@api.route('/api/chart1', methods=['GET'])
def chart1():
    year = request.args.get("year", 2022)
    db = get_db()
    data = db.table('province').where({"year": year}).select()
    db.close()
    if data:
        data = list(map(lambda x: {
            "name": x["province"],
            "value": x["total"]
        }, data))
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart2', methods=['GET'])
def chart2():
    db = get_db()

    data = db.table("people").order("year asc").select()

    db.close()

    if data:
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart3', methods=['GET'])
def chart3():
    db = get_db()

    data = db.table("people").order("year asc").select()

    db.close()

    if data:
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart4', methods=['GET'])
def chart4():
    db = get_db()

    data = db.table("age").where({"year": 2022}).find()

    db.close()

    if data:
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart5', methods=['GET'])
def chart5():
    db = get_db()

    gdp = db.table("gdp").where({"year": 2022}).select()

    # 转为字典
    gdp = dict(map(lambda x: (x["province"], x["gdp"]), gdp))

    people = db.table("province").where({"year": 2022}).select()

    db.close()

    data = []
    for p in people:
        avg = gdp.get(p["province"], 0) / p["total"]
        row = [gdp[p["province"]], p['total'], avg, p["province"], 2022]
        # print(row)
        data.append(row)

    if data:
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart6', methods=['GET'])
def chart6():
    db = get_db()
    sql = """
    select t.year,GROUP_CONCAT(province order by province asc) as name,GROUP_CONCAT(total order by province asc) as value from (SELECT year,
	province,
	total 
FROM
	province p 
WHERE
	( SELECT COUNT( * ) FROM province p2 WHERE p2.YEAR = p.YEAR AND p2.total >= p.total ) <= 5 
ORDER BY
	YEAR,
	total DESC) t GROUP BY year;
    """

    res = db.query(sql)
    db.close()
    if res:
        return jsonResponse(200, 'success', res)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart7', methods=['GET'])
def chart7():
    db = get_db()
    res = db.table("province").where({"year": 2022}).select()
    db.close()
    if res:
        return jsonResponse(200, 'success', res)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart10', methods=['GET'])
def chart10():
    db = get_db()
    res = db.table("province").order("year asc").select()
    db.close()
    if res:
        return jsonResponse(200, 'success', res)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart12', methods=['GET'])
def chart12():
    db = get_db()
    res = db.table("birth").order("year desc").limit(10).select()
    db.close()
    if res:
        return jsonResponse(200, 'success', res)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart13', methods=['GET'])
def chart13():
    db = get_db()

    gdp = db.table("gdp").select()
    people = db.table("province").select()

    db.close()

    if gdp and people:
        data = []
        for year in range(2004, 2023):
            year_data = []
            cur_year_people = list(filter(lambda x: x['year'] == year, people))
            cur_year_gdp = list(filter(lambda x: x['year'] == year, gdp))
            province_dict = dict(map(lambda x: (x["province"], x["total"]), cur_year_people))
            gdp_dict = dict(map(lambda x: (x["province"], x["gdp"]), cur_year_gdp))

            keys = list(province_dict)
            for province in keys:
                # avg = gdp_dict[province] / province_dict[province]
                row = [province_dict[province] / 100, gdp_dict[province] / 100, province, year]
                year_data.append(row)
            data.append(year_data)
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.route('/api/chart14', methods=['GET'])
def chart14():
    db = get_db()

    data = db.table("age").order("year asc").select()

    db.close()

    if data:
        return jsonResponse(200, 'success', data)
    return jsonResponse(500, 'fail', None)


@api.get('/api/data/age')
def get_age():
    """
    lookup age data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    data = db.table("age").where(condition).page(page, limit).select()

    return jsonResponse(200, 'success', data)


@api.get('/api/data/birth')
def get_birth():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    data = db.table("birth").where(condition).page(page, limit).select()

    return jsonResponse(200, 'success', data)


@api.get('/api/data/gdg')
def get_gdp():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    gdp = request.args.get('gdp')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    if gdp:
        condition["gdp"] = gdp

    data = db.table("gdp").where(condition).page(page, limit).select()

    return jsonResponse(200, 'success', data)


@api.get('/api/data/people')
def get_people():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    data = db.table("people").where(condition).page(page, limit).select()

    return jsonResponse(200, 'success', data)


@api.get('/api/data/province')
def get_province():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    province = request.args.get('province')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    if province:
        condition["province"] = province

    data = db.table("province").where(condition).page(page, limit).select()

    return jsonResponse(200, 'success', data)


@api.get("/api/user/star")
def get_chart_name():
    """
    lookup star data
    :return:
    """
    db = get_db()

    user_id = request.args.get('user_id')

    data = db.table("star").where({"user_id": user_id}).select()

    print(data)

    return jsonResponse(200, 'success', data)


@api.post('/api/user/star')
def add_chart_name():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()
    user_id = data.get('user_id')
    chart_name = data.get('chart_name')

    res = db.table("star").add({
        "user_id": user_id,
        "chart_name": chart_name
    })

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/user/star')
def delete_chart_name():
    """
    delete star data
    :return:
    """
    db = get_db()
    data = request.get_json()
    user_id = data.get('user_id')
    chart_name = data.get('chart_name')

    res = db.table("star").where({
        "user_id": user_id,
        "chart_name": chart_name
    }).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/user')
def get_user():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    name = request.args.get('username')
    email = request.args.get('email')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if name:
        condition["username"] = ["LIKE", f"%{name}%", "", "e"]

    if email:
        condition["email"] = ["LIKE", f"%{email}%", "", "e"]

    # total
    total = db.table('user').where(condition).count()

    # list
    list = db.table('user').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/user')
def add_user():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    res = db.table("user").add({
        "username": username,
        "password": password,
        "email": email
    })

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/user')
def put_user():
    """
    put user
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("user").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/user')
def delete_user():
    """
    delete star data
    :return:
    """
    db = get_db()
    id = request.args.get("id")

    res = db.table("user").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/age')
def get_age_data():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    # total
    total = db.table('age').where(condition).count()

    # list
    list = db.table('age').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/age')
def add_age_data():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("age").add(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/age')
def put_age_data():
    """
    put age data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("age").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/age')
def delete_age():
    """
    delete age data
    :return:
    """
    db = get_db()
    id = request.args.get("id")

    res = db.table("age").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/birth')
def get_birth_data():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    # total
    total = db.table('birth').where(condition).count()

    # list
    list = db.table('birth').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/birth')
def add_birth_data():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("birth").add(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/birth')
def put_birth_data():
    """
    put birth data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("birth").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/birth')
def delete_birth():
    """
    delete birth data
    :return:
    """
    db = get_db()
    id = request.args.get("id")

    res = db.table("birth").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/gdp')
def get_gdp_data():
    """
    lookup birth data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    province = request.args.get('province')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    if province:
        condition["province"] = province

    # total
    total = db.table('gdp').where(condition).count()

    # list
    list = db.table('gdp').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/gdp')
def add_gdp_data():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("gdp").add(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/gdp')
def put_gdp_data():
    """
    put birth data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("gdp").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/gdp')
def delete_gdp():
    """
    delete gdp data
    :return:
    """
    db = get_db()
    id = request.args.get("id")

    res = db.table("gdp").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/people')
def get_people_data():
    """
    lookup people data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    # total
    total = db.table('people').where(condition).count()

    # list
    list = db.table('people').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/people')
def add_people_data():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("people").add(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/people')
def put_people_data():
    """
    put birth data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("people").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/people')
def delete_people():
    """
    delete people data
    :return:
    """
    db = get_db()
    id = request.args.get("id")

    res = db.table("people").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)


@api.get('/api/province')
def get_province_data():
    """
    lookup province data
    :return:
    """
    db = get_db()
    year = request.args.get('year')
    province = request.args.get('province')
    page = request.args.get('pageNo')
    limit = request.args.get('pageSize')

    condition = {
        "id": ["EGT", 1, "", "e"]
    }

    if year:
        condition["year"] = year

    if province:
        condition["province"] = province

    # total
    total = db.table('province').where(condition).count()

    # list
    list = db.table('province').where(condition).order("id desc").page(page, limit).select()

    db.close()

    result = {"total": total, "list": list}

    return jsonResponse(200, 'success', result)


@api.post('/api/province')
def add_province_data():
    """
    add star data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("province").add(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.put('/api/province')
def put_province_data():
    """
    put province data
    :return:
    """
    db = get_db()
    data = request.get_json()

    res = db.table("province").where({"id": data["id"]}).save(data)

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success')


@api.delete('/api/province')
def delete_province():
    """
    delete province data
    :return:
    """
    db = get_db()
    id = request.args.get("id")
    res = db.table("province").where({"id": id}).delete()

    if not res:
        return jsonResponse(500, 'fail', None)

    return jsonResponse(200, 'success', None)
