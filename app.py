from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.text_summarizer import TextSummarizer
from utils.text_to_speech import TextToSpeech
import speech_recognition as sr

app = Flask(__name__)

# Initialize models
summarizer = TextSummarizer()
tts = TextToSpeech()
recognizer = sr.Recognizer()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form["text"]
    if not text:
        return redirect(url_for("index"))

    # Generate summary
    summary = summarizer.summarize(text)

    # Convert summary to speech and save the audio file
    audio_path = "static/summary_audio.mp3"
    tts.convert_to_speech(summary, output_path=audio_path)

    return render_template("index.html", summary=summary)

@app.route("/speech_to_text", methods=["GET"])
def speech_to_text():
    return render_template("speech_to_text.html")

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Add timeout and phrase_time_limit to avoid hanging
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")

            text = recognizer.recognize_google(audio)
            return jsonify({'success': True, 'text': text})
    except sr.WaitTimeoutError:
        return jsonify({'success': False, 'error': "Timeout: No speech detected."})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': "Speech unclear."})
    except sr.RequestError as e:
        return jsonify({'success': False, 'error': f"Google API error: {e}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
