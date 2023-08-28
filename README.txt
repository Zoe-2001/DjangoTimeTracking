=====================SETUP======================================

To runit on your local machine:
  1. Open console in the root directory of the project
  2. Run the following command, which installs all of the modules listed in therequirements file into our project environment.
       pip install -r requirements.txt
  3. Run the following command:
       python manage.py runserver
  4. Visit http://localhost:8000


=====================USERS======================================
There are currently 2 users in the database, you can use the following information to log in:
  1. username: Zoe     password: Zoe
  2. username: yuchendai     password: yuchendai
You can also register new users for testing or presentation


=====================RESTART DATABASE======================================
When you want to clear and recreate the database:
  1. Delete db.sqlite3 file under the root directory of the project
  2. Open the console at the project's root directory
  3. Run the following commands:
       python manage.py migrate
       python manage.py runserver
  5. Visit http://localhost:8000


=====================REFERENCES======================================
References:
https://codepen.io/jasonleewilson/pen/gPrxwX

