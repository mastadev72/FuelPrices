from src.modules.main.views import main_blueprint

from src.modules.api.views import HelloWorld


# Flask blueprints
blueprints = [main_blueprint]

# API resourses
resources = {
	HelloWorld: "/hello"
}
