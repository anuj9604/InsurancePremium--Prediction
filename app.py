from flask import Flask
import os, sys
from premium.logger import logging
from premium.exception import PremiumException

app=Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    try:
        raise Exception("Testing a custom Exception")
    except Exception as e:
        prem=PremiumException(e, sys)
        logging.info(prem.error_message)

    return "Setting up the structure!"

if __name__=="__main__":
    app.run(debug=True)