from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "SimPro API Proxy is running. Use /api/simpro/job/<job_id> to fetch job data and /api/simpro/staff/<staff_id> to fetch staff data."

@app.route('/api/simpro/job/<job_id>', methods=['GET'])
def get_simpro_job(job_id):
    """
    Proxy endpoint that forwards requests to SimPro API
    Make.com calls this endpoint, and we forward to SimPro with proper auth
    """
    # SimPro API configuration
    simpro_api_url = f"https://proformelectricalptyltd.simprosuite.com/api/v1.0/companies/0/jobs/{job_id}"
    bearer_token = "da974939f51b52fa6dbc43d2c739a5a576d24672"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
    }
    
    try:
        # Forward the request to SimPro API
        response = requests.get(simpro_api_url, headers=headers)
        response.raise_for_status()
        
        # Return the SimPro response to Make.com
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch job from SimPro",
            "details": str(e)
        }), 500

@app.route('/api/simpro/staff/<staff_id>', methods=['GET'])
def get_simpro_staff(staff_id):
    """
    Proxy endpoint that fetches staff/employee data from SimPro API
    """
    # SimPro API configuration
    simpro_api_url = f"https://proformelectricalptyltd.simprosuite.com/api/v1.0/companies/0/employees/{staff_id}"
    bearer_token = "da974939f51b52fa6dbc43d2c739a5a576d24672"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
    }
    
    try:
        # Forward the request to SimPro API
        response = requests.get(simpro_api_url, headers=headers)
        response.raise_for_status()
        
        # Return the SimPro response
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch staff from SimPro",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

