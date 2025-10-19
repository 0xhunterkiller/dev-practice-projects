import subprocess
import tempfile
import os
import wave

# https://rhasspy.github.io/piper-samples/
MODEL_PATH="voices/en_US-ryan-high.onnx"
CONFIG_PATH="voices/en_US-ryan-high.onnx.json"

def say(text, piper_bin="piper"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name

    try:
        subprocess.run(
            [piper_bin, "--model", MODEL_PATH, "--config", CONFIG_PATH, "--output_file", output_path],
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        
        # Force the file to be flushed and readable
        with wave.open(output_path, "rb") as wf:
            wf.readframes(wf.getnframes())  # force decode/load

        # Now play it
        subprocess.run(["ffplay", "-nodisp", "-autoexit", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    finally:
        os.remove(output_path)