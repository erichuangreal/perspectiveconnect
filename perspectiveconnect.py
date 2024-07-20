import gradio as gr
import subprocess
from openai import OpenAI

#input_messages = [{"role": "system", "content": 'You are a knowledgeable and helpful intelligent chat robot. Your task is to chat with me. Please use a short conversational style and speak in Chinese. Each answer should not exceed 50 words!'}]
input_messages = [{"role": "system", "content": 'Please criticize the content and delivery my presentation and give constructive feedback for improvement!'}]


client = OpenAI(api_key='sk-aichoicesservice-OFNmT1NXrWnmZB3262bYT3BlbkFJv3hIZDbp4I1M6yAfocNq')

def transcribe(audio):
    global input_messages

    audio_file = open(audio, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file, 
      response_format="text"
    )
    print(transcription)

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

    for line in response.splitlines():
        print(line)
        subprocess.call(["wsay", line])

    chat_transcript = ""
    for message in input_messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    chat_transcript += "Response from AI: " + response

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(sources=["microphone"], type="filepath"), outputs="text")
ui.launch()
