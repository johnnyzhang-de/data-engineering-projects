import requests
import json

# url = "https://jsonplaceholder.typicode.com/users"

# response = requests.get(url)
# data = response.json()
# # print(type(data))
# # print(data[0].get('name'))
# # print(data[0].get('address').get('city'))

# result = json.dumps(data[0])
# print(type(result))
# result = json.loads(result)
# print(type(result))

# import requests

# url = "https://jsonplaceholder.typicode.com/posts"

# payload = {
#     "title": "Johnny post",
#     "body": "practice api",
#     "userId": 1
# }

# response = requests.post(url, json=payload)
# data = response.json()

# print(data)
# print(data.get("title"))
# print(data.get("body"))
# print(data.get("userId"))

# import requests

# url = "https://httpbin.org/post"

# payload = {
#     "name": "Johnny",
#     "skill": "Python",
#     "level": "practice"
# }

# response = requests.post(url, json=payload)
# print(response.status_code)
# print(response.json())

# import requests
# url = 'https://jsonplaceholder.typicode.com/users'
# response = requests.get(url)

# data = response.json()
# print(type(data))


payload = {
    "name": "Johnny",
    "skill": "Python",
    "level": "practice"
}

# import requests
# url = ''
# response = requests.get(url)
# data = response.json()

# import json
# result = json.dumps(payload)
# print(type(result))
# result = json.loads(result)
# print(type(result))
# print(result)

file = 'file.json'
with open(file) as f:
    data = json.loads(f)
    