from quart import Blueprint, render_template, request
from blockvalidator.deps.nanolib_helpers import BetaBlockValidator, LiveBlockValidator
import json

block_bp = Blueprint('block', __name__)


@block_bp.route('/', methods=['GET', 'POST'])
async def block():
    block_text = ''
    error_message = None
    blocks = get_default_blocks()
    if request.method == 'POST':
        try:
            form_data = await request.form
            block_text = json.dumps(json.loads(
                form_data['block_text']), indent=4)
            results = analyze_block(block_text)
            return await render_template('index.html', block_text=block_text, results=results, blocks=blocks)
        except Exception as e:
            error_message = str(e)
    return await render_template('index.html', block_text=block_text, error_message=error_message, blocks=blocks)


def get_default_blocks():
    blocks = [
        {'block_name': "Genesis Live", 'block_content': {
            "type": "open",
            "source": "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA",
            "representative": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
            "account": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
            "work": "62f05417dd3fb691",
            "signature": "9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02"
        }},
        {'block_name': "Genesis Beta", 'block_content': {
            "type": "open",
            "source": "259A438A8F9F9226130C84D902C237AF3E57C0981C7D709C288046B110D8C8AC",
            "representative": "nano_1betag7az9wk6rbis38s1d35hdsycz1bi95xg4g4j148p6afjk7embcurda4",
            "account": "nano_1betag7az9wk6rbis38s1d35hdsycz1bi95xg4g4j148p6afjk7embcurda4",
            "work": "e87a3ce39b43b84c",
            "signature": "BC588273AC689726D129D3137653FB319B6EE6DB178F97421D11D075B46FD52B6748223C8FF4179399D35CB1A8DF36F759325BD2D3D4504904321FAFB71D7602"
        }},
        {'block_name': "Genesis Test", 'block_content': {
            "type": "open",
            "source": "45C6FF9D1706D61F0821327752671BDA9F9ED2DA40326B01935AB566FB9E08ED",
            "representative": "nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
            "account": "nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
            "work": "bc1ef279c1a34eb1",
            "signature": "15049467CAEE3EC768639E8E35792399B6078DA763DA4EBA8ECAD33B0EDC4AF2E7403893A5A602EB89B978DABEF1D6606BB00F3C0EE11449232B143B6E07170E"
        }}
    ]
    return blocks


def analyze_block(block_text):

    beta = BetaBlockValidator(block_text)
    live = LiveBlockValidator(block_text)

    beta_validation = beta.validate()
    live_validation = live.validate()

    result = {
        'block_hash': live.get_block_hash(),
        'is_pow_valid_live_base': live_validation["is_work_valid_base"],
        'is_pow_valid_live_receive': live_validation["is_work_valid_receive"],
        'is_pow_valid_live_epoch1': live_validation["is_work_valid_epoch1"],

        'is_pow_valid_beta_base': beta_validation["is_work_valid_base"],
        'is_pow_valid_beta_receive': beta_validation["is_work_valid_receive"],
        'is_pow_valid_beta_epoch1': beta_validation["is_work_valid_epoch1"],

        'is_signature_valid': live_validation["is_signature_valid"],
        'work_value': live_validation["difficulty"],

        'work_threshold_beta_base': beta_validation["base_difficulty"],
        'work_threshold_beta_receive': beta_validation["receive_difficulty"],
        'work_threshold_beta_epoch1': beta_validation["epoch1_difficulty"],

        'work_threshold_live_base': live_validation["base_difficulty"],
        'work_threshold_live_receive': live_validation["receive_difficulty"],
        'work_threshold_live_epoch1': live_validation["epoch1_difficulty"],

        'multiplier_beta_base': "{:.2f}".format(beta_validation["base_multiplier"]),
        'multiplier_beta_receive': "{:.2f}".format(beta_validation["receive_multiplier"]),
        'multiplier_beta_epoch1': "{:.2f}".format(beta_validation["epoch1_multiplier"]),

        'multiplier_live_base': "{:.2f}".format(live_validation["base_multiplier"]),
        'multiplier_live_receive': "{:.2f}".format(live_validation["receive_multiplier"]),
        'multiplier_live_epoch1': "{:.2f}".format(live_validation["epoch1_multiplier"])
    }
    return result
