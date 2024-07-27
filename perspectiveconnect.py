import gradio as gr
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import random
import string
import time

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

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcription = "Audio not clear enough to transcribe."
    return transcription

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

def process_presentation(audio):
    # Step 1: Transcribe audio
    transcription = transcribe_audio(audio)
    
    # Step 2: Get feedback from GPT-3.5
    feedback = get_feedback(transcription)
    
    # Step 3: Convert feedback to speech
    audio_feedback_path = text_to_speech(feedback)
    
    return transcription, feedback, audio_feedback_path

ui = gr.Interface(fn=process_presentation, 
                inputs=gr.Audio(sources=["microphone"], type="filepath"), 
                outputs=[
                    gr.Textbox(label="Presentation"),
                    gr.Textbox(label="AI Response"),
                    gr.Audio(label="Audio Ai Response", type="filepath")
                ],
                title="AI Presentation Trainer",
                description="Practise your presentation to get transcription, feedback, and audio feedback."
            )
#ui.launch(auth=(server_name="0.0.0.0", server_port=7860, "test", "eric123321!"), share=True)
ui.launch(server_name="0.0.0.0", server_port=7860)
