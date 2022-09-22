$env:FLASK_APP = "manage"
$env:FLASK_ENV = "development"
flask digest clean
flask digest compile
