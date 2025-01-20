import requests
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Send POST request to PHP API
        response = requests.post('http://localhost/login-signup/login.php', data={
            'email': username,
            'password': password,
        })

        return JsonResponse(response.json())  # Return PHP API response to the frontend

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hash = md5( rand(0,1000) )

        # Send POST request to PHP API
        response = requests.post('http://localhost/login-signup/signup.php', data={
            'firstname' : first_name,
            'lastname' : last_name,
            'email': email,
            'password': password,
            'hash' : hash,
        })

        return JsonResponse(response.json())  # Return PHP API response to the frontend
