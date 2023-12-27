import os, re, math
import torch, whisper, ffmpeg
import tkinter as tk
from tkinter import filedialog

os.environ['PYTHONIOENCODING'] = 'utf-8'

def spool_whisper_model():
    if torch.cuda.is_available():
        print("Cuda Time!")
        TheWhisperer = whisper.load_model('large-v2', device='cuda')
    else:
        print("CPU Time :c")
        TheWhisperer = whisper.load_model('large-v2')
    return TheWhisperer
TheWhisperer = spool_whisper_model()

def save_transcription(texticles):
    sentences = re.split(r'(?<=[.!?]) +', texticles)
    try:
        return '\n'.join(sentences)
    except UnicodeEncodeError:
        sentences = [re.sub(r'[^\x00-\x7F]+', '', sentence) for sentence in sentences]
        return '\n'.join(sentences)
    
def time_slice(seconds):
    hours = math.floor(seconds / 3600)
    seconds -= hours * 3600
    minutes = math.floor(seconds / 60)
    seconds -= minutes * 60
    seconds = math.floor(seconds)
    if hours == 0:
        return '{:02d}:{:02d}'.format(minutes, seconds)
    else:
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

def MONEY_TIME(vfp):
    print("Zug Zug!")
    #button1.config(text = "Transcribing...")

    afp = vfp.replace(".mp4", ".mp3")
    video_stream = ffmpeg.input(vfp)
    audio_stream = video_stream.audio
    output_stream = ffmpeg.output(audio_stream, f"{afp}")
    ffmpeg.run(output_stream, capture_stdout=True)

    print("Transcribe time!")
    whisper_output = TheWhisperer.transcribe(afp, fp16=False)
    #print(f"DEY OUTPEWT WAS ALL DISHEET!!: {whisper_output}")
    os.remove(afp)
    nfp = vfp.replace(".mp4", "-Transcription.txt")

    # Raw Text
    el_text = whisper_output['text']
    la_text = re.split(r'(?<=[.!?]) +', el_text)
    das_text = '\n'.join(la_text)

    # Segment Texts
    del_text = ""
    seggus = whisper_output['segments']
    for dills in seggus:
        stt = time_slice(dills['start'])
        txticles = dills['text']
        del_text += str(stt) + " - " + str(txticles) + '\n'

        
    print(f"The Transcription was: {das_text}")
    print(f"The Time Coded Transcription was: {del_text}")

    try:
        with open(nfp, "w") as f:
            f.write("Text Transcription - No Timecodes" + '\n')
            f.write(str(das_text))
            f.write('\n' + '\n' + "Time Coded Text Transcription" + '\n')
            f.write(str(del_text))
    except UnicodeEncodeError:
        new_das_text = re.sub(r'[^\x00-\x7F]+', '', das_text)
        new_del_text = re.sub(r'[^\x00-\x7F]+', '', del_text)
        print(f"Error occured in text. New text is: {new_das_text}")
        with open(nfp, "w") as f:
            f.write("Text Transcription - No Timecodes" + '\n')
            f.write(str(new_das_text))
            f.write('\n' + '\n' + "Time Coded Text Transcription" + '\n')
            f.write(str(new_del_text))

    #button1.config(text = "Choose a Video to Transcribe.")
    print("Job Done!")


def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    return file_path

def button_click():
    video_path = open_file_dialog()
    if video_path:
        MONEY_TIME(video_path)
    else:
        print("No file selected.")


root = tk.Tk()
root.title("Arthen-VideoTransriber v11")

button1 = tk.Button(root, text="Choose a Video to Transcribe.", command=button_click)
button1.pack()

root.mainloop()