from quart import Blueprint, render_template, request
from blockvalidator.deps.nanolib_helpers import BetaBlockValidator, LiveBlockValidator, nl_block_from_json, nl_get_block_hash

block_bp = Blueprint('block', __name__)


@block_bp.route('/', methods=['GET', 'POST'])
async def block():
    block_text = ''
    error_message = None
    if request.method == 'POST':
        try:
            form_data = await request.form
            block_text = form_data['block_text']
            results = analyze_block(block_text)
            return await render_template('index.html', block_text=block_text, results=results)
        except Exception as e:
            error_message = str(e)
    return await render_template('index.html', block_text=block_text, error_message=error_message)


def analyze_block(block_text):

    block = nl_block_from_json(block_text)

    beta = BetaBlockValidator(block)
    live = LiveBlockValidator(block)

    beta_validation = beta.validate()
    live_validation = live.validate()

    return {
        'block_hash': nl_get_block_hash(block),
        'is_pow_valid_live_base': live_validation["is_work_valid_base"],
        'is_pow_valid_live_receive': live_validation["is_work_valid_receive"],
        'is_pow_valid_beta_base': beta_validation["is_work_valid_base"],
        'is_pow_valid_beta_receive': beta_validation["is_work_valid_receive"],
        'is_signature_valid': live_validation["is_signature_valid"],
        'work_value': live_validation["difficulty"],
        'work_threshold_beta_base': beta_validation["base_difficulty"],
        'work_threshold_beta_receive': beta_validation["receive_difficulty"],
        'work_threshold_live_base': live_validation["base_difficulty"],
        'work_threshold_live_receive': live_validation["receive_difficulty"],
        'multiplier_beta_base': "{:.2f}".format(beta_validation["base_multiplier"]),
        'multiplier_beta_receive': "{:.2f}".format(beta_validation["receive_multiplier"]),
        'multiplier_live_base': "{:.2f}".format(live_validation["base_multiplier"]),
        'multiplier_live_receive': "{:.2f}".format(live_validation["receive_multiplier"])
    }
