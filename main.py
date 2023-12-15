import flask
import fitz
import base64
import argparse
import numpy as np
import cv2


def clip(a, b, c):
    return b if a < b else a if a < c else c


def create_app(config):

    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return 'Home Page'

    @app.route('/<int:page_number>/<float:scale>')
    def render_pdf(page_number, scale):
        with fitz.open(config.input) as pdf_document:
            page_number = clip(page_number, 0, pdf_document.page_count-1)
            print("page_number: ", page_number)

            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))

            img_array = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape((pix.h, pix.w, 3))

            img_array = 224 - (img_array - img_array // 4)

            _, buffer = cv2.imencode(
                '.png',
                cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)
            )

            page_images = [
                base64.b64encode(
                    buffer
                ).decode('utf-8')
            ]

        print(type(page_images[0]))

        return flask.render_template(
            'pdf_viewer.html',
#            page_images=page_images
        )

    return app


if __name__ == '__main__':
    # Example usage
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input file')
    args = parser.parse_args()

    app = create_app(args)
    app.run(debug=True)
