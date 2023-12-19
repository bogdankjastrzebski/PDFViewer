import flask
import fitz
import argparse
import numpy as np
import cv2
import flask_cors


def clip(a, b, c):
    return b if a < b else a if a < c else c


def pix_to_numpy(pix):
    return np.frombuffer(
        pix.samples,
        dtype=np.uint8,
    ).reshape((pix.h, pix.w, 3))


def numpy_to_buffer(arr):
    return cv2.imencode(
        '.png',
        cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA),
    )[1]


def create_app(config):

    app = flask.Flask(__name__)
    flask_cors.CORS(app)

    @app.route('/')
    def index():
        return flask.render_template('index.html')

    @app.route('/info')
    def info():
        with fitz.open(config.input) as pdf_document:
            info = {
                'pageCount': pdf_document.page_count
            }
        return flask.jsonify(info)

    @app.route('/content/<int:page_number>')  # /<float:scale>')
    def content(page_number):  # , scale):

        with fitz.open(config.input) as pdf_document:
            if page_number < pdf_document.page_count:
                page = pdf_document.load_page(page_number)
                svg = page.get_svg_image(fitz.Matrix(2, 2))
            else:
                svg = None

        return flask.Response(svg, content_type='image/svg+xml')

    return app


if __name__ == '__main__':
    # Example usage
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input file')
    args = parser.parse_args()

    app = create_app(args)
    app.run(debug=True)
