import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.blackjacks import initBlackjack
from model.unos import initUno
from model.wars import initWar
from model.memories import initMemory

# setup APIs
from api.blackjack import blackjack_api # Blueprint import api definition
from api.uno import uno_api
from api.war import war_api
from api.memory import memory_api

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# initialize db object
db.init_app(app)

# register URIs
app.register_blueprint(blackjack_api) # register api routes
app.register_blueprint(uno_api)
app.register_blueprint(war_api)
app.register_blueprint(memory_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.before_first_request
def activate_job():  # activate these items 
    initBlackjack()
    initUno()
    initWar()
    initMemory()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8086")
