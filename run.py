from flask import Flask , render_template
from routes.admin import admin
from routes.login import login

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(login)



# 404 error
@app.errorhandler(404) #
def page_not_found(e):
    return render_template('error/404.html')

if __name__ == '__main__':
    app.run(debug=True)
