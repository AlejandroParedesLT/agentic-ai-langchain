from flask import Flask, request, jsonify
import json
import sys
import os
from code.lambda_agenticai.researchAgent_handler import lambda_handler
import code.models.researchAgent as DeepSeekResearcherAgent
app = Flask(__name__)

@app.route('/researchAgent', methods=['POST'])
def api_gateway_proxy():
    """
    This mimics the API Gateway's behavior when calling a Lambda function.
    It takes the request body, wraps it in the expected format, and passes it to the Lambda handler.
    """
    try:
        # Format the request as API Gateway would
        api_gateway_event = {
            'body': json.dumps(request.json),
            'headers': dict(request.headers),
            'requestContext': {
                'requestId': '123456789'
            }
        }
        
        # Call the Lambda handler with the API Gateway event
        lambda_response = lambda_handler(api_gateway_event, None)
        
        # Extract the response body
        if 'body' in lambda_response:
            if isinstance(lambda_response['body'], str):
                response_body = json.loads(lambda_response['body'])
            else:
                response_body = lambda_response['body']
            return jsonify({"body": response_body})
        else:
            return jsonify(lambda_response)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server to emulate API Gateway + Lambda...")
    app.run(host='0.0.0.0', port=8000, debug=True)