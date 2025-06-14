from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)
CORS(app)

data_store = {}

def generate_random_data(cnf):
    def random_digits(n): return ''.join(random.choices(string.digits, k=n))
    def random_name(): return random.choice(["Alice", "Bob", "Charlie", "Diana"]) + " " + random.choice(["Smith", "Johnson", "Lee"])
    def random_address(): return f"{random.randint(100, 999)} {random.choice(['Main St', 'Oak St', 'Maple Ave'])}"
    def random_postcode(): return random_digits(5)
    def random_expiry(): return f"{random.randint(1, 12):02d}/{random.randint(2025, 2030)}"
    def random_card(): return ' '.join([random_digits(4) for _ in range(4)])

    return {
        "cnf": cnf,
        "cardNumber": random_card(),
        "name": random_name(),
        "expiry": random_expiry(),
        "address": random_address(),
        "postcode": random_postcode()
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    cnf = request.args.get("cnf")

    if cnf:
        if cnf in data_store:
            return jsonify(data_store[cnf])
        else:
            return jsonify({"error": "Invalid CNF. Not found."}), 404
    else:
        cnf = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        data_store[cnf] = generate_random_data(cnf)
        return jsonify(data_store[cnf])

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
