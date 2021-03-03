# BookStore built using Django and React
Backend : Django
FrontEnd: React

url: https://obscure-earth-33829.herokuapp.com/

# Assumptions
1. The application is secure and the API calls are authenticated
2. The logging module is in place to log all the details
3. The Auth mechanism is in place to make the application secure
4. The quantity is never negative
5. There are concourrent users using the application and the quantity is only decremented after user buys something

# Reason
1. Django rest_framework is used for creating the API's as it provides lot of features and configuration out of the box
2. React Js is used because of the ease it provides in consuming the REST API from the backend

# Instructions
Backend : ```python manage.py runserver```
Frontend : ```npm start```
