call py -3.11 -m venv venv
call venv\Scripts\activate
call python -m pip install --upgrade pip
call pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
call pip install -r requirements.txt
echo Warming up the Transcriber now! Please wait...
call ArthenTranscriber.py
cmd /k