import gradio as gr
import speech_recognition as sr
import librosa
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np
from openai import OpenAI
from gtts import gTTS
import random
import string
import time
import os

#input_messages = [{"role": "system", "content": 'You are a knowledgeable and helpful intelligent chat robot. Your task is to chat with me. Please use a short conversational style and speak in Chinese. Each answer should not exceed 50 words!'}]
input_messages = [{"role": "system", "content": 'Please criticize the content and delivery my presentation and give constructive feedback for improvement!'}]


client = OpenAI(api_key='sk-aichoicesservice-OFNmT1NXrWnmZB3262bYT3BlbkFJv3hIZDbp4I1M6yAfocNq')

def generate_ai_response_file_path(length=10):
    # Get the current timestamp
    timestamp = time.time()
    
    # Seed the random number generator with the timestamp
    random.seed(timestamp)
    
    # Define the character set for the random string
    characters = string.ascii_letters + string.digits
    
    # Generate the random string
    ai_response_file_path = ''.join(random.choice(characters) for _ in range(length))
    
    return ai_response_file_path

# Function to transcribe audio with a retry mechanism
def transcribe_audio(audio_path, retries=5, delay=2):
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        if audio_path is not None and os.path.exists(audio_path):
            try:
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data)
                return transcription
            except sr.UnknownValueError:
                print("Audio not clear enough to transcribe.")
                return ""
        else:
            print(f"Attempt {attempt + 1}/{retries}: Audio file not available, retrying in {delay} seconds...")
            time.sleep(delay)
    return "Audio file not available after multiple attempts."

def get_feedback(transcription):
    global input_messages

    input_messages.append({"role": "user", "content": transcription})

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=input_messages,
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += " " + chunk.choices[0].delta.content
    return response

def text_to_speech(response):
    tts = gTTS(text=response, lang='en')
    audio_path = generate_ai_response_file_path() + ".mp3"
    tts.save(audio_path)
    return audio_path

def get_tempo(audio):
    # gets a dynamic tempo (accounts for fluctuations throughout)
    y, sr = librosa.load(audio, duration=30)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    dtempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    prior_lognorm = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
    dtempo_lognorm = librosa.feature.tempo(onset_envelope=onset_env, sr=sr,
                                       aggregate=None,
                                       prior=prior_lognorm)
    return dtempo, dtempo_lognorm, onset_env, sr
    
def plot_tempo(audio):
    dtempo, dtempo_lognorm, onset_env, sr = get_tempo(audio)
    
    # Convert to scalar
    if len(dtempo) == 1:
        tempo = dtempo.item()

    # Compute 2-second windowed autocorrelation
    hop_length = 512
    ac = librosa.autocorrelate(onset_env, max_size=2 * sr // hop_length)
    freqs = librosa.tempo_frequencies(len(ac), sr=sr, hop_length=hop_length)
    
    # plot dynamic tempo estimates over a tempogram
    fig, ax = plt.subplots()
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr,
                                hop_length=hop_length)
    librosa.display.specshow(tg, x_axis='time', y_axis='tempo', cmap='magma', ax=ax)
    ax.plot(librosa.times_like(dtempo), dtempo,
            color='c', linewidth=1.5, label='Tempo estimate (default prior)')
    
    # plots the lognorm; takes some time, not too sure what is the meaning of it yet.
    ax.plot(librosa.times_like(dtempo_lognorm), dtempo_lognorm,
            color='c', linewidth=1.5, linestyle='--',
            label='Tempo estimate (lognorm prior)')
    ax.set(title='Dynamic tempo estimation')
    ax.legend()

    # save image
    output_path = 'dynamic_tempo_plot.png'
    plt.savefig(output_path)
    plt.close(fig)
    return output_path

def process_presentation(audio):
    # Step 1: Transcribe audio
    transcription = transcribe_audio(audio)
    
    # Step 2: Get feedback from GPT-3.5
    feedback = get_feedback(transcription)
    
    # Step 3: Convert feedback to speech
    audio_feedback_path = text_to_speech(feedback)
    
    # Step 4: Get tempo
    tempo = plot_tempo(audio)

    return transcription, feedback, audio_feedback_path, tempo

ui = gr.Interface(fn=process_presentation, 
                inputs=gr.Audio(sources=["microphone"],  type="filepath"), 
                outputs=[
                    gr.Textbox(label="Presentation"),
                    gr.Textbox(label="AI Response"),
                    gr.Audio(label="Audio Ai Response", type="filepath"),
                    gr.Image(label="Dynamic Tempo")
                ],
                title="AI Presentation Trainer",
                description="Practise your presentation to get transcription, feedback, and audio feedback."
            )
#ui.launch(auth=(server_name="0.0.0.0", server_port=7860, "test", "eric123321!"), share=True)
ui.launch(share=True, server_name="0.0.0.0", server_port=7860)
