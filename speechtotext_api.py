from flask import Flask, request, jsonify
import speech_recognition as sr
from googletrans import Translator
import os

app = Flask(__name__)
translator = Translator()

def speech_to_text(audio_file, chosen_language):
   
    
    recognizer = sr.Recognizer()
    # recognizer.pause_threshold = 0.8

    
    chosen_language_=chosen_language.strip("'")
   
    # chosen_language='mr'
    if chosen_language==chosen_language_:
        print("True")
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        # print("2:", chosen_language)
        # chosen_language='hi'
        text = recognizer.recognize_google(audio, language=chosen_language_)
        print("Recognizing...")
        if chosen_language_ != 'en':
            translated_text = translator.translate(text, dest='en').text
          
            return {
                'recognized_text': text,
                'translated_text': translated_text
            }
        else:
            return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return "Sorry, I couldn't request results from the Google Speech Recognition service; {0}".format(e)

@app.route('/speech-to-text', methods=['POST'])
def convert_speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    language_choice = request.form.get('language').strip()
    

    # Save the audio file temporarily
    temp_audio_path = 'temp_audio.wav'
    audio_file.save(temp_audio_path)

    # Perform speech-to-text conversion
    transcription = speech_to_text(temp_audio_path, language_choice)

    # Delete the temporary audio file
    os.remove(temp_audio_path)

    return jsonify({'transcription': transcription}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
