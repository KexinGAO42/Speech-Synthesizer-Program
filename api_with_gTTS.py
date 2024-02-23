from flask import Flask, request, send_file, render_template
from flask_restful import Resource, Api

from gtts import gTTS
from Synthesizer import Synth, Utterance  # Import your TTS function

app = Flask(__name__)
api = Api(app)

class TextToSpeech(Resource):
    def post(self):
        data = request.get_json()
        text = data.get('text')

        if not text:
            return {'error': 'Text parameter is required'}, 400

        tts = gTTS(text)
        tts.save('tmp.wav')

        # utt = Utterance(text)
        # phone_seq = utt.get_phone_seq()
        # diphone_synth = Synth(phone_seq, wav_folder="./diphones")
        # diphone_synth.save_output("tmp.wav")

        # Play audio in the browser
        return send_file('tmp.wav', mimetype="audio/wav", as_attachment=True, download_name='audio.wav')
@app.route('/')
def index():
    return render_template('index.html')
api.add_resource(TextToSpeech, '/text-to-speech')

if __name__ == '__main__':
    app.run(debug=True)
