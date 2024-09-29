import os
import speech_recognition as sr
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

app = Client("hpclbot", api_id=11163590, api_hash="fa76f31e5f7a64d906d4978dd0e5d3b3", bot_token="7614990586:AAHlIXcDSKKXUwmJs0aKvEHyRSg7BUFpYSY")

DOWNLOAD_PATH = "./downloads/"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

def voice_to_text(file_path: str) -> str:
    recognizer = sr.Recognizer()
    try:
        # Convert audio file to WAV
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        return f"Error recognizing speech: {str(e)}"
      
@app.on_message(filters.voice)
async def handle_voice(client: Client, message: Message):
    await message.reply_text("🔄 Processing your voice message...")
    file_path = await app.download_media(message.voice.file_id, file_name=DOWNLOAD_PATH + "voice.oga")
    wav_path = file_path.replace(".oga", ".wav")
    os.system(f"ffmpeg -i {file_path} {wav_path}")
    transcription = voice_to_text(wav_path)
    await message.reply_text(f"📝 Transcription: {transcription}")
    os.remove(file_path)
    os.remove(wav_path)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
