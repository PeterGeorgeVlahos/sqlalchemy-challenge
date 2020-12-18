# 1. Import Flask
from flask import Flask

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
    return (
        f"Hello and welcome to my Hawaiin Vacation Home Page!<br/>"
        f"Here you will be able to inspect past the weather Honolulu, Hawaii <br/>"
        f"and decide which days are best to visit<br/>"
        f"Safe Travels<br/>"
        f"<br/>"
        f"Use the following Routes to inspect weather measurements:<br/>"
        f"<br/>"                   
        f"/api/v1.0/precipitation <br/>"     
        f"/api/v1.0/stations <br/>"
    )


@app.route("/about")
def about():
    name = "Peleke"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."


@app.route("/contact")
def contact():
    email = "peleke@example.com"

    return f"Questions? Comments? Complaints? Shoot an email to {email}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
