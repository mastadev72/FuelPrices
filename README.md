<div align="center">
	<img src="./app/src/static/img/logo.png" width="140" title="Logo">
    <h1>Fuel Prices</h1>
</div>

### 🗃 About Project

FuelPrices is an Open Source project that allows people to monitor Georgia's fuel prices. With this web app people can
monitor, compare fuel prices, and use API to access current prices

### 📋 Docs

1. Clone the repository

    ```git
    git clone https://github.com/NickNaskida/FuelPrices.git
    ```

2. Create a copy of .env.example file in /app with name .env.dev

3. Edit just created .env.dev file content

4. Create virtual environment
   ```
   # Windows
   
   # Install virtualenv
   pip install virtualenv
   
   # Create environment
   virtualenv virtualenv_name
   
   # Activate
   myenv\Scripts\activate
   
   
   # Linux
   
   # Install virtualenv
   pip install virtualenv
   
   # Create environment
   virtualenv -p /usr/bin/python3 virtualenv_name
   
   # Activate
   source virtualenv_name/bin/activate
   ```

5. Install requirements
   ```
   cd app
   pip install -r requirements/dev.txt
   ```

6. Run commands in app/scripts to start local development server
    ```
    # Windows
   
    cd app
   
   ./scripts/windows/init.ps1
   ./scripts/windows/migrate.ps1
   ./scripts/windows/digest.ps1
   ./scripts/windows/fill_db.ps1
   ./scripts/windows/run.ps1
   
   
    # Linux
   
    cd app
   
    sudo bash ./scripts/linux/init.sh
    sudo bash ./scripts/linux/migrate.sh
    sudo bash ./scripts/linux/digest.sh
    sudo bash ./scripts/linux/fill_db.sh
    sudo bash ./scripts/linux/run.sh
    ```

7. Go to http://127.0.0.1:5000/
8. Enjoy 💫

### 👨🏼‍🔬 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks in advance!

In general, we follow the "fork-and-pull" Git workflow

#### How to submit a Pull Request

- Search our repository for open or closed Pull Requests that relate to your submission. You don't want to duplicate effort.
- Fork the project on GitHub.
- Create your feature branch
- Do your work. Read the docs to this project.
- Commit your changes (Please use semantic commit messages: [Semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716))
- Push to the branch
- Open a Pull Request and wait for feedback.

🎉 Thank you for your contribution!

Feel free to add yourself to the AUTHORS if your change(s) are significant (e.g new feature, critical bug fix ...).
