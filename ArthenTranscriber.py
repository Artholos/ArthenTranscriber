import os, re, math
import torch, whisper, ffmpeg
import tkinter as tk
from tkinter import filedialog

os.environ['PYTHONIOENCODING'] = 'utf-8'
rwd = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

def spool_whisper_model():
    global rwd
    model_dir = os.path.join(rwd, 'Model')
    if torch.cuda.is_available():
        print("Cuda Time!")
        TheWhisperer = whisper.load_model('large-v3', device='cuda', download_root=model_dir)
    else:
        print("CPU Time :c")
        TheWhisperer = whisper.load_model('large-v3', download_root=model_dir)
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
    miliseconds = seconds - math.floor(seconds)
    seconds = math.floor(seconds)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, int(miliseconds * 100))

def is_mp3(vfp):
    if vfp.endswith(".mp3"):
        filetype = "mp3"
    elif vfp.endswith(".wav"):
        filetype = "wav"
    else:
        filetype = "mp4"
    return filetype

def MONEY_TIME(vfp):
    print("Zug Zug!")
    #button1.config(text = "Transcribing...")

    filetype = is_mp3(vfp)
    if filetype == "mp4":
        print("Video File")
        afp = vfp.replace(".mp4", ".mp3")
        video_stream = ffmpeg.input(vfp)
        audio_stream = video_stream.audio
        output_stream = ffmpeg.output(audio_stream, f"{afp}")
        ffmpeg.run(output_stream, capture_stdout=True)
    else:
        print("Audio File")
        afp = vfp

    print("Transcribe time!")
    whisper_output = TheWhisperer.transcribe(afp, fp16=False)
    print(whisper_output)
    #os.remove(afp)
    nfp = vfp.replace(f".{filetype}", "-Transcription.txt")
    srt = vfp.replace(f".{filetype}", "-Transcription.srt")

    # Raw Text
    el_text = whisper_output['text']
    la_text = re.split(r'(?<=[.!?]) +', el_text)
    das_text = '\n'.join(la_text)

    # Segment Texts
    del_text = ""
    seggus = whisper_output['segments']
    counter = 1
    for dills in seggus:
        stts = time_slice(dills['start'])
        stte = time_slice(dills['end'])
        txticles = dills['text']
        del_text += str(counter) + " " + str(stts) + " --> " + str(stte) + str(txticles) + '\n'
        counter += 1

        
    print(f"The Transcription was: {das_text}")
    print(f"The Time Coded Transcription was: {del_text}")

    # Write Text File
    try:
        with open(nfp, "w") as f1:
            f1.write("Time Coded Text Transcription:" + '\n')
            f1.write(str(del_text))
            f1.write('\n' + '\n' + "Raw Text Transcription:" + '\n')
            f1.write(str(das_text))
        with open(srt, "w") as f2:
            f2.write(str(del_text))
    except UnicodeEncodeError:
        new_das_text = re.sub(r'[^\x00-\x7F]+', '', das_text)
        new_del_text = re.sub(r'[^\x00-\x7F]+', '', del_text)
        print(f"Error occured in text. New text is: {new_das_text}")
        with open(nfp, "w") as f1:
            f1.write("Time Coded Text Transcription:" + '\n')
            f1.write(str(new_del_text))
            f1.write('\n' + '\n' + "Raw Text Transcription:" + '\n')
            f1.write(str(new_das_text))
        with open(srt, "w") as f2:
            f2.write(str(new_del_text))

    #button1.config(text = "Choose a Video to Transcribe.")
    print("Job Done!")


def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Please choose a MP4, MP3, or Wav file", "*.mp4 *.mp3 *.wav")])
    return file_path

def button_click():
    video_path = open_file_dialog()
    if video_path:
        MONEY_TIME(video_path)
    else:
        print("No file selected.")


root = tk.Tk()
root.geometry("300x100")
root.title("ArthenTransriber v11.3")

button1 = tk.Button(root, text="Choose a Video/Audio file to Transcribe.", command=button_click)
button1.pack(pady = 20)

root.mainloop()