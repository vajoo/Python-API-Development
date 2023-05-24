import requests
import time


bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxOSwiZXhwIjoxNjg0NDk2MzU1fQ.B2mzwgmg5KA0mUhh-9t3PPvEwaTsBHTLjPQXJ5QeaAU"

# Login request to get the Bearer token
login_url = 'http://127.0.0.1:8000/login'
login_data = {
    "username": "laurin@gmail.com",
    "password": "12345"
}

start_time_login = time.time()

login_response = requests.post(login_url, data=login_data)
login_data = login_response.json()
bearer_token = login_data['access_token']

start_time = time.time()

# POST request to /posts with the Bearer token and body
posts_url = 'http://127.0.0.1:8000/posts'
post_body = {
    "title": "TITLE",
    "content": "CONTENT",
    "published": "true"
}

headers = {
    'Authorization': f'Bearer {bearer}'
}

post_response = requests.post(posts_url, json=post_body, headers=headers)

# End the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
elapsed_time_login = end_time - start_time_login
# Print the response status code and any returned data
print('Response status code:', post_response.status_code)
print('Response data:', post_response.json())

print(f"Elapsed time: {elapsed_time} seconds")
print(f"Elapsed time with login: {elapsed_time_login} seconds")