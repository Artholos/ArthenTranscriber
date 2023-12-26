Recommended Python 3.11.5 (Since that's what I used to make it), but it should work on anything 3.9+ but not 3.12! It doesn't work on 3.12 as of writing this.

Installation and prep:
1. Install Python 3.11.5 (Or whatever version you wanna use, I'm not your mom): https://www.python.org/downloads/release/python-3115/ (MAKE SURE TO ADD TO PATH AT THE END OF INSTALLATION!)
2. Create a directory for the program and put the VideoTranscriber.py and requirements.txt in it, along with your OS's Run file.
3. Open a cmd/terminal in the program folder and run the setup files.
   Windows > RunTranscriber-Windows.bat
   Mac > RunTranscriber-Mac.sh
   OR > Use the commands below to set up the environment manually:

Windows:
```py -3.11 -m venv venv```
```venv\Scripts\activate```
```python -m pip install --upgrade pip```
```pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```
```pip install -r requirements.txt```

Mac:
```python3.11 -m venv venv```
```python3.11 -m pip install --upgrade pip```
```source venv/bin/activate```
```install --upgrade pip```

Now you can run either the VideoTranscriber.py file directly and it should work probably... Best to use the bat/sh file to run it since it will make sure to use the venv.


HOW TO USE:

Once the program is started, it can take several minutes for the program to warm up and the UI to appear. Don't worry, it does take an honest minute or two.

Then simply click the button, choose a .mp4 video file (needs to be using h.265 codec). And let the magic happen!

* Please note that the first time you run it can take a minute or two to fetch the transription model from OpenAI. After that it will run right away everytime.

Finally, your transcription document will be created in the same folder as your video file. The file will be named like your video file: "____-Transcription.txt".
