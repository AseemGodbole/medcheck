import os
import sys
from flask import Flask, render_template, request, jsonify

app_dir   = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(app_dir)
sys.path.insert(0, parent_dir)

from med_checker import get_structured_results
import time
import subprocess

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    asset_version = os.environ.get('ASSET_VERSION')
    if not asset_version:
        try:
            asset_version = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'], cwd=parent_dir
            ).decode().strip()
        except Exception:
            asset_version = str(int(time.time()))
    return render_template('index.html', asset_version=asset_version)


@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.json or {}
    drugs_text      = data.get('drugs', '').strip()
    conditions_text = data.get('conditions', '').strip()

    if not drugs_text:
        return jsonify({'error': 'Please enter at least one medicine'}), 400

    drugs      = [d.strip() for d in drugs_text.split(',')      if d.strip()]
    conditions = [c.strip() for c in conditions_text.split(',') if c.strip()]

    try:
        result = get_structured_results(drugs, conditions)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
