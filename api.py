from flask import Flask, request, jsonify
from Synthesizer import Synth  # Import your TTS function

app = Flask(__name__)


@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data['text']
    # Call your TTS function here
    speech = Synth(text)
    return jsonify({'speech': speech})


if __name__ == '__main__':
    app.run(debug=True)
