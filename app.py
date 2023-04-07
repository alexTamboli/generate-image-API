from flask import Flask, request, make_response, render_template
from PIL import Image
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # Get parameters from the request
    width = request.form.get('width')
    height = request.form.get('height')
    color = request.form.get('color')
    image_format = request.form.get('format')

    # Check if parameters are valid
    if not all([width, height, color, image_format]):
        return make_response('Invalid parameters', 400)

    try:
        width = int(width)
        height = int(height)
    except ValueError:
        return make_response('Invalid parameters', 400)

    if color not in ['red', 'green', 'blue']:
        return make_response('Invalid parameters', 400)

    if image_format not in ['jpeg', 'png', 'gif']:
        return make_response('Invalid parameters', 400)

    # Generate the image using Pillow
    color_map = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}
    image = Image.new('RGB', (width, height), color_map[color])
    buffer = BytesIO()
    try:
        image.save(buffer, format=image_format.upper())
    except ValueError:
        return make_response('Invalid parameters', 400)

    # Set the filename with the appropriate extension
    filename = f'image.{image_format}'

    # Return the image as a response with the appropriate headers
    response = make_response(buffer.getvalue())
    response.headers.set('Content-Type', f'image/{image_format}')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response

@app.errorhandler(Exception)
def handle_error(e):
    # Handle all exceptions and return a JSON response with the error message
    response = {
        'status': 403,
        'message': str(e),
    }
    return make_response(response, 403)

if __name__ == '__main__':
    app.run()
