# USERS API 

### Foydalanuvchilar bilan ishlashda kerak bo'lgan metodlar
## Asosiy ENDPOINT: [https://pitak001.herokuapp.com/api/users](https://pitak001.herokuapp.com/api/users) 


## SMS yuborish
### POST /send-otp/
```json
{
    "phone": "998901234567" // Telefon raqam
}
```

### Natija
![Send-otp](../readme_src/users/send-otp.png)


## SMSni tekshirish
### POST /validate-otp/
```json
{
    "phone": "998901234567", // Telefon raqam
    "otp": "1234" // SMS kodi
}
```
### Natija:
![Validate-otp](../readme_src/users/validate-otp.png)


## GET /api/users
### Foydalanuvchilarni qaytaradi. So'rov yuborayotgan foydalanuvchi login qilingan bo'lishi kerak. Ya'ni GET so'rovi yuborayotganda so'rovga qo'shib access token yuborish kerak.
```json
{
    "headers": {
        "Authorization": "Bearer <access_token>" // Access token
        }
}
```
### Natija:
![Users list](../readme_src/users/users_list2.png)

## GET /api/users/user/ 
### Foydalanuvchi haqida ma'lumot qaytaradi. So'rov yuborayotgan foydalanuvchi login qilingan bo'lishi kerak. Ya'ni GET so'rovi yuborayotganda so'rovga qo'shib access token yuborish kerak.
```json
{
    "headers": {
        "Authorization": "Bearer <access_token>" // Access token
        }
}
```
### Natija:
![User info](../readme_src/users/user_info.png)

## Ro'yxatdan o'tish 
### POST /api/users/register/
Ro'yxatdan o'tishdan oldin sms yuboriladi. Smsni tekshirishdan keyin ro'yxatdan o'tish mumkin.

Request: 
```json
    {
        "phone": "998901234567", //required
        "password": "1234", //required
        "phone2": "998901234567", //not required
        "is_driver": false, // not required
    }
```
### Natija:
![Register](../readme_src/users/register.png)


## Tizimga kirish. Login 
### POST /api/users/login/
LOGIN qilishdan oldin sms yuboriladi. Smsni tekshirishdan keyin login mumkin.
```json
    {
        "phone": "998901234567", //required
        "password": "1234", //required
    }
```
### Natija:
![Login](../readme_src/users/login_postman.png)


## Logout
### POST /api/users/logout/
```json
    {
        "headers": {
            "Authorization": "Bearer <access_token>" // Access token
        }
    }
```
Natija:
![Logout](../readme_src/users/logout.png)