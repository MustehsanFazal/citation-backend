from flask import Flask, request, jsonify
from scrape_and_parse import scrape_and_parse

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def api():
    ecli = request.args.get("ecli")
    if not ecli:
        return jsonify({"error": "ECLI is required"}), 400
    try:
        data = scrape_and_parse(ecli)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
