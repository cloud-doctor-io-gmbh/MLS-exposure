from flask import Flask, request, jsonify
import cv2
import numpy as np
from io import BytesIO

def create_app():
    app = Flask(__name__)

    underexposed_threshold = 50
    overexposed_threshold = 200

    @app.route('/analyze_exposure', methods=['POST'])
    def analyze_exposure():
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        image_stream = file.read()
        image_array = np.frombuffer(image_stream, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Unable to read image'}), 404

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        black_threshold = 0.1
        mask = gray_image > (black_threshold * 255)
        if np.sum(mask) == 0:
            return jsonify({'error': 'Image is too dark to analyze'}), 422

        average_brightness = np.mean(gray_image[mask])

        if average_brightness < underexposed_threshold:
            exposure = 'Underexposed'
        elif average_brightness > overexposed_threshold:
            exposure = 'Overexposed'
        else:
            exposure = 'Correctly Exposed'

        return jsonify({'average_brightness': average_brightness, 'exposure': exposure}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
