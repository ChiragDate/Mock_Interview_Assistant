import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import play, Voice, VoiceSettings

import numpy as np
import time
import os

from utils.config import (
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    RECORDING_SAMPLE_RATE,
    RECORDING_CHANNELS,
    TEMP_AUDIO_FILENAME,
)

try:
    el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
except Exception as e:
    print(f"Error initialising client:{e}")
    el_client = None
    
r = sr.Recognizer()     

#record, transcribe and textToSpeech function

def speak_text(text : str):
    """Uses ElevenLabs to conver text to speech and play it"""
    if not el_client:
        print("Client not initialised. Cannot speak.")
        print("Printing text instead.")
        print(f"Interviewer:{text}")
        
        time.sleep(len(text.split())/3)
        return
    
    try:
        print("Generating audio...")
        
        voice_obj = Voice(
            voice_id=ELEVENLABS_VOICE_ID,
            settings=VoiceSettings(stability=0.6,
                                   similarity_boost=0.85,
                                   style =0.1,
                                   use_speaker_boost=True)
        )
        
        audio = el_client.text_to_speech.convert(
            
            text = text,
            voice_id =ELEVENLABS_VOICE_ID,
            #model_id = "eleven_multilingual_v2"
        )
        print("Speaking...")
        play(audio)
        print("Finihsed speaking.")
    except Exception as e:
        print(f"Error {e}")
        print("Fallback to printing text")
        print(f"Interviewer: {text}")
        time.sleep(len(text.split())/3)
        

def record_audio(duration: int = 15, filename: str = TEMP_AUDIO_FILENAME) -> str | None:
    """Records audio from the microphone for a specified duration."""
    print(f"\n Recording for {duration} seconds... Speak clearly into the microphone.")
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        recording = sd.rec(int(duration * RECORDING_SAMPLE_RATE),
                           samplerate=RECORDING_SAMPLE_RATE,
                           channels=RECORDING_CHANNELS,
                           dtype='float32') # Use float32 which soundfile handles well
        sd.wait() 

        # Save as WAV file using soundfile
        sf.write(filename, recording, RECORDING_SAMPLE_RATE)

        print(f" Recording saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error during audio recording: {e}")
        return None

def transcribe_audio(filename: str = TEMP_AUDIO_FILENAME) -> str | None:
    """Transcribes audio file to text using SpeechRecognition (Google Web Speech API)."""
    print("Transcribing your response...")
    if not os.path.exists(filename):
        print(f"Error: Audio file not found for transcription: {filename}")
        return None

    with sr.AudioFile(filename) as source:
        try:
            audio_data = r.record(source) # Read the entire audio file
            # Use Google Web Speech API for transcription
            text = r.recognize_google(audio_data)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during transcription: {e}")
            return None
        finally:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"Warning: Could not delete temp audio file {filename}: {e}")