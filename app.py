from flask import Flask
from rentals.logger import logging
from rentals.exception import RentalException

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        raise Exception("We are testing custom exceptions")
    except Exception as e:
        rentals = RentalException(e,sys)
        logging.info(rentals.error_message)
        logging.info("We are testing logger module")
    return "Starting Machine Learning Pipeline..."

if __name__ == "__main__":
    app.run(debug=True)
