"""Backbround module used for calling vosk-transcriber on the wav file"""

import subprocess
import sys
import os
import json
from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel

SetLogLevel(-1)

SAMPLE_RATE = 16000
CHUNK_SIZE = 4000

class Transcriber():
    def __init__(self, model_path):
        self.model = Model(model_path)

    def fmt(self, data):
        data = json.loads(data)

        start = min(r["start"] for r in data.get("result", [{ "start": 0 }]))
        end = max(r["end"] for r in data.get("result", [{ "end": 0 }]))

        return data["text"]

    def transcribe(self, filename):
        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        transcription = []

        ffmpeg_command = [
                "ffmpeg",
                "-nostdin",
                "-loglevel",
                "quiet",
                "-i",
                filename,
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ]

        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE) as process:

            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    transcription.append(self.fmt(rec.Result()))

            transcription.append(self.fmt(rec.FinalResult()))
        return transcription
