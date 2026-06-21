import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):

    try:

        result = model.transcribe(audio_path)

        print("TRANSCRIPT:")
        print(result["text"])

        return result["text"]

    except Exception as e:

        print("Transcription Error:", e)

        return ""