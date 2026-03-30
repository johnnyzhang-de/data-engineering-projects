import requests
import json
import psycopg2
url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

try:
    response.raise_for_status()
except Exception as e:
    print(f'connection_error:{e}')

data = response.json()

# with open("users_sample.json", "w") as f:
#     json.dump(data, f, indent=2)


def flatten_users(data):
    result = []
    for record in data:
        id = record.get('id')
        name = record.get('name')
        username = record.get('username')
        email = record.get('email')
        address = record.get('address')
        if not isinstance(address, dict):
            continue
        street = address.get('street')
        suite = address.get('suite')
        city = address.get('city')
        zipcode =address.get('zipcode')
        geo = address.get('geo')
        if isinstance(geo,dict):
            lat = geo.get('lat')
            lng = geo.get('lng')
        else:
            lat = None
            lng = None
        phone = record.get('phone')
        website = record.get('website')
        company = record.get('company')
        if isinstance(company,dict):
            company_name = company.get('name')
            catch_Phrase = company.get('catchPhrase')
            bs = company.get('bs')
        else:
            company_name = None
            catch_Phrase = None
            bs = None
        result.append({
            'id':id,
            'name':name,
            'username':username,
            'email':email,
            'street':street,
            'suite':suite,
            'city':city,
            'zipcode':zipcode,
            'lat':lat,
            'lng':lng,
            'phone':phone,
            'website':website,
            'company_name':company_name,
            'catchPhrase':catch_Phrase,
            'bs':bs
        })
    return result

def connect_database():
    conn = psycopg2.connect(
        database = 'de_project',
        host = 'localhost',
        port = 5433,
        user = 'postgres',
        password = '11111111'
    )
    cursor =conn.cursor()
    return conn, cursor
conn, cursor = connect_database()

def insert_users(records):
    conn,cursor = connect_database()
    insert_sql =  '''
                    insert into users_flat (id,name,username,email,street,suite,city,zipcode,lat,lng,phone,website,company_name,catch_phrase,bs)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
    values = []
    for record in records:  
        row = (
            record.get('id'),
            record.get('name'),
            record.get('username'),
            record.get('email'),
            record.get('street'),
            record.get('suite'),
            record.get('city'),
            record.get('zipcode'),
            record.get('lat'),
            record.get('lng'),
            record.get('phone'),
            record.get('website'),
            record.get('company_name'),
            record.get('catchPhrase'),
            record.get('bs')
        )
        values.append(row)
    try:
        cursor.executemany(insert_sql,values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'insert failed:{e}')
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    flat_records = flatten_users(data)
    insert_users(flat_records)
    # print(flat_records[0]) 
    print("pipeline finished")

