**Simple e-commerce website with paypal payment method.**

![bookstore](https://user-images.githubusercontent.com/64534303/164705792-09dcc35f-9209-49d1-8b4e-c9a6255596a3.png)


Bookstore website with rating system.



## Quickstart
Create a virtual environment to store your projects dependencies separately.

` pip install virtualenv `

` virtualenv venv `

This will create a new directory called ` venv `.

Clone or download this repository.

` git clone https://github.com/lukitoziomal/bookstore.git `

Activate your virtual environment.

` path-to-venv\venv\Scripts\activate `

Install project dependencies.

` pip install -r requirements.txt `


Run migrations:

` python manage.py migrate `


Add books to database. Run script"

` python manage.py runscript addbooks `

Run server.

` python manage.py runserver `

Paypal configuration. (optional)
------

Configure your paypal business address ` PAYPAL_RECEIVER_EMAIL ` in ` bookstore\settings.py `. For testing use paypal sandbox account.

Paypal signals handler needs this website to go live. To do so you can use ngrok.

-----
