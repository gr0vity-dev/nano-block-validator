from quart import Quart
from blockvalidator.routes.block import block_bp

app = Quart(__name__)

app.register_blueprint(block_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
