import flask
import fitz
import base64
import argparse
import numpy as np
import cv2


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
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                arr = pix_to_numpy(pix)
                arr = 207 - (arr - 3 * (arr // 8))
                buffer = numpy_to_buffer(arr)
                image_data = base64.b64encode(buffer).decode('utf-8')
            else:
                image_data = None

        return flask.jsonify(
            {'content': image_data}
            if image_data else
            {'error': 'Invalid page number'}
        )

        # return flask.render_template(
        #    'pdf_viewer.html',
        #    image_data=image_data,
        # )

    return app


if __name__ == '__main__':
    # Example usage
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input file')
    args = parser.parse_args()

    app = create_app(args)
    app.run(debug=True)
