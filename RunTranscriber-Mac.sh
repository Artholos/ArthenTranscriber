#!/bin/sh
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Warming up the Transcriber now! Please wait..."
python3 VideoTranscriber.py