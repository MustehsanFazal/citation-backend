from flask_cors import CORS
from flask import Flask, request, jsonify
from scrape_and_parse import scrape_and_parse

app = Flask(__name__)
CORS(app)


@app.route("/generate-citation", methods=["GET"])
def generate_citation():
    ecli = request.json.get("ecli")
    if not ecli:
        return jsonify({"error": "ECLI is required"}), 400
    try:
        data = scrape_and_parse(ecli)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
