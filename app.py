from flask import Flask
from routes.AuthorRoutes import route1
from routes.DataImporter import route2

app = Flask(__name__)
app.register_blueprint(route1, url_prefix="/api/v1/authors")
app.register_blueprint(route2, url_prefix="/api/v1/dataimporter")

if __name__ == '__main__':
    app.run(port=5000)
