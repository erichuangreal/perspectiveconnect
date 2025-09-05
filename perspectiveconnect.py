import gradio as gr
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import random
import string
import time
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import parselmouth

# Define the input messages for the AI chat model
# Input messages should be improved on. Currently, the AI response feedback is not specific or actionable enough.
# The input messages should be more detailed and specific to the presentation except chatgpt-3.5 keeps on giving
# broad, generic, and short responses. May we should consider fine-tuning.
input_messages = [{"role": "system", "content": """Please analyze the technical and devliery aspects of my
                   presentation and provide helpful feedback. I want examples from the text that I must improve in.
                   I want to know how I can improve my delivery and content. Never use # and * symbols. No italics,
                   bold, underlined, or any other font styles or emphasis text. Please provide as much detail and
                   examples as possible. I do not want generic feedback. I want specific feedback that I can use to.
                   A one sentence imrpovement is not enough. I want a detailed analysis of my presentation. Please the
                   feedback relevant and specific, thank you.
                   """}]


client = OpenAI(api_key='placeholder')

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
                audio_file = open(audio_path, "rb")
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file, 
                    response_format="text"
                )
                return transcription
                #with sr.AudioFile(audio_path) as source:
                #    audio_data = recognizer.record(source)
                #transcription = recognizer.recognize_google(audio_data)
                #return transcription
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
        model="gpt-4o",
        messages=input_messages,
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    response = response.replace("*", "")
    response = response.replace("#", "")
    return response

def text_to_speech(response):
    tts = gTTS(text=response, lang='en')
    audio_path = generate_ai_response_file_path() + ".mp3"
    tts.save(audio_path)
    return audio_path

def process_presentation(audio):
    # Step 1: Transcribe audio
    transcription = transcribe_audio(audio)
    
    # Step 2: Extract audio qualities
    audio_qualities = extracting_audio_qualities(audio)
    prompt = prepare_prompt(transcription, audio_qualities)
    print(prompt)
    # Step 3: Get feedback
    feedback = get_feedback(prompt)
    
    # Step 4: Convert feedback to speech
    audio_feedback_path = text_to_speech(feedback)
    
    
    return transcription, feedback, audio_feedback_path, audio_qualities

def extracting_audio_qualities(audio) :
    y, sr = librosa.load(audio)
    
    # Pitch analysis (fundamental frequency)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    pitch = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch.append(pitches[index, t])
    pitch = np.array([p for p in pitch if p > 0])

    # Loudness analysis
    S = np.abs(librosa.stft(y))
    loudness = librosa.amplitude_to_db(S, ref=np.max)

    # Timbre analysis
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_flatness = librosa.feature.spectral_flatness(y=y).mean()
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean(axis=1)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean()

    # Speech rate analysis (tempo in syllables per second)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    syllable_count = np.sum(onset_env > np.mean(onset_env))
    total_duration = librosa.get_duration(y=y, sr=sr)
    syllables_per_second = syllable_count / total_duration

    # Jitter, Shimmer, HNR (Sometimes the parselmouth.praat.call method throws an error because the snd object
    # is not compatible with the function, help fix this issue)
    snd = parselmouth.Sound(audio)
    print(f"Audio duration: {snd.get_total_duration()} seconds")
    print(f"Sampling frequency: {snd.get_sampling_frequency()} Hz")
    
    point_process = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 100, 1000)
    jitter = parselmouth.praat.call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    shimmer = parselmouth.praat.call([snd, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    harmonicity = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)


    # Results
    results = {
        "pitch_mean": np.mean(pitch),
        "pitch_std": np.std(pitch),
        "loudness_mean": np.mean(loudness),
        "loudness_std": np.std(loudness),
        "spectral_centroid_mean": np.mean(spectral_centroid),
        "spectral_bandwidth_mean": np.mean(spectral_bandwidth),
        "mfccs_mean": np.mean(mfccs, axis=1),
        "syllables_per_second": syllables_per_second,
        "spectral_flatness_mean": spectral_flatness,
        "spectral_contrast_mean": spectral_contrast.tolist(),
        "spectral_rolloff_mean": spectral_rolloff,
        "jitter": jitter,
        "shimmer": shimmer,
        "hnr": hnr,
        "harmonicity": harmonicity
    }
    
    return results

def prepare_prompt(transcription, voice_features):
    prompt = f"""
    Presentation Text:
    {transcription}

    Voice Features:
    - Pitch Mean: {voice_features['pitch_mean']}
    - Pitch Std: {voice_features['pitch_std']}
    - Loudness Mean: {voice_features['loudness_mean']}
    - Loudness Std: {voice_features['loudness_std']}
    - Spectral Centroid Mean: {voice_features['spectral_centroid_mean']}
    - Spectral Bandwidth Mean: {voice_features['spectral_bandwidth_mean']}
    - MFCCs Mean: {voice_features['mfccs_mean']}
    - Syllables Per Second: {voice_features['syllables_per_second']}
    - Spectral Flatness Mean: {voice_features['spectral_flatness_mean']}
    - Spectral Contrast Mean: {voice_features['spectral_contrast_mean']}
    - Spectral Rolloff Mean: {voice_features['spectral_rolloff_mean']}
    - Jitter: {voice_features['jitter']}
    - Shimmer: {voice_features['shimmer']}
    - Harmonics-to-Noise Ratio: {voice_features['hnr']}

    Please evaluate the presentation based on the provided text and voice features.
    """
    return prompt

ui = gr.Interface(fn=process_presentation, 
                inputs=gr.Audio(sources=["microphone"],  type="filepath"), 
                outputs=[
                    gr.Textbox(label="Presentation"),
                    gr.Textbox(label="AI Response"),
                    gr.Audio(label="Audio Ai Response", type="filepath")
                ],
                title="AI Presentation Trainer",
                description="<html><body><p>Practice your presentation to get transcription, feedback, and audio feedback. <br>Step1: start recording; <br>Step2: stop recording; <br>Step3: play back your recording; <br>Step4: submit your recording; <br>Step5: get feedback.</p></body></html>"
            )
#ui.launch(auth=(server_name="0.0.0.0", server_port=7860, "test", "eric123321!"), share=True)
ui.launch(share=True, server_name="0.0.0.0", server_port=7861)
