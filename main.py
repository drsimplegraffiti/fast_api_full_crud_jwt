# Import packages
from fastapi import FastAPI

# Instantiate app
app = FastAPI()

# Route handler
@app.route("/", methods=['GET'])
def index():
    return "working"