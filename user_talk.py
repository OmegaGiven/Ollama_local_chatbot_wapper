# user_talk.py

import whisper
import pyaudio
import numpy as np
import wave
import time
from threading import Thread
import streamlit as st

# Load Whisper model
model = whisper.load_model("turbo")

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
THRESHOLD = 500  # Threshold for silence detection
SILENCE_DURATION = 3.0  # Minimum silence in seconds to stop recording
audio_buffer = []

def is_silent(data):
    """Check if the audio chunk is silent."""
    return max(abs(s) for s in data) < THRESHOLD

def record_audio():
    """Record audio from microphone and detect silence."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press Ctrl+C to stop.")

    while True:
        data = stream.read(CHUNK)
        audio_buffer.append(np.frombuffer(data, dtype=np.int16))

        if is_silent(data):
            silence_start = time.time()
            while time.time() - silence_start < SILENCE_DURATION:
                data = stream.read(CHUNK)
                audio_buffer.append(np.frombuffer(data, dtype=np.int16))
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert buffer to numpy array
    audio_data = np.concatenate(audio_buffer)
    audio_data = audio_data.astype(np.float32) / 32768.0

    # Save audio to file
    with wave.open("transcribing_audio.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes())

    print("Recording stopped. Transcribing audio...")

def transcribe_audio():
    """Transcribe the recorded audio."""
    result = model.transcribe("transcribing_audio.wav")
    print("Transcribed text:", result["text"])
    st.session_state["transcribed_text"] = result["text"]

def start_transcription():
    """Start audio recording and transcription in separate threads."""
    record_thread = Thread(target=record_audio)
    record_thread.start()
    record_thread.join()

    transcribe_thread = Thread(target=transcribe_audio)
    transcribe_thread.start()
    transcribe_thread.join()