import suggestions
import create_csv
from flask import Flask, request, jsonify
from flask_cors import CORS
from meta_handler import MetaHandler
from suggestions import Suggestions


meta_handler = MetaHandler()
sugg = Suggestions(meta_handler)
app = Flask(__name__)
CORS(app)

# create & load csv
create_csv.aggregate_csv_data(meta_handler, overwrite=False)
results = create_csv.load_csv()


# --- define routes ---

@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    res = sugg.get_suggestions(results, request.form)

    if res == -1:
        return {'error': 'No data'}

    return jsonify(res)


@app.route('/languages', methods=['GET'])
def get_programming_languages():
    return jsonify({'languages': meta_handler.get_programming_languages()})


@app.route('/countries', methods=['GET'])
def get_countries():
    return jsonify({'countries': meta_handler.get_countries()})


@app.route('/top', methods=['GET'])
def get_top_users():
    return jsonify(sugg.get_top_users(results))


# --- start server ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)

