import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):

    try:

        result = model.transcribe(
            audio_path,
            language="en"
        )

        return result["text"].strip()

    except Exception as e:

        print("Transcription Error:", str(e))

        return ""
