from flask import Flask, jsonify
import json

app = Flask(__name__)

# Route for /profile
@app.route('/api/v2/linkedin', methods=['GET'])
def get_profile():
    with open('data/emeline.json', 'r') as f:
        profile_data = json.load(f)
    return jsonify(profile_data)


# Route for /company
@app.route('/api/linkedin/company', methods=['GET'])
def get_company():
    with open('./data/company.json', 'r') as f:
        company_data = json.load(f)
    return jsonify(company_data)


@app.route('/api/linkedin/school', methods=['GET'])
def get_company():
    with open('./data/school.json', 'r') as f:
        school_data = json.load(f)
    return jsonify(school_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
