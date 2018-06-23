
from flask import Flask, render_template, request


app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SECRET_KEY='James Bond',
)


@app.route('/create', methods=['POST'])
def index():
    data = request.form.to_dict()
    return 'ok'


if __name__ == '__main__':
    app.run()
