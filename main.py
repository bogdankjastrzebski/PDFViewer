import flask
import fitz


app = flask.Flask(__name__)


@app.route('/')
def render_pdf(pdf_path):

    with fitz.open(pdf_path) as pdf_document:
        page_images = [
            pdf_document[page_number].get_pixmap().tobytes('ppm')
            for page_number in range(pdf_document.page_count)
        ]

    return flask.render_template(
        'pdf_viewer.html',
        page_images=page_images
    )


if __name__ == '__main__':
    # Example usage
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input file')
    parser.add_argument('--output', type=str, help='output file')
    args = parser.parse_args()
    print('Starting servers...')
    print(args)
    app.run(debug=True)
