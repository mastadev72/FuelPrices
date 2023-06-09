$env:FLASK_APP = "manage"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1

pip install -r requirements.txt

flask db init
flask db migrate
flask db upgrade

flask digest clean
flask digest compile

flask fill_db

flask run
