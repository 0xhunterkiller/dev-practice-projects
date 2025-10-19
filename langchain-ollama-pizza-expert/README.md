# langchain-ollama-pizza-expert
A pizza expert written with the help of rating from a pizza.csv file. It Talks!

# Text To Speech

The Text to Speech Module uses Piper. Install Piper with `pip`

```
pip install piper-tts
```

Or, you can just install  the requirements.txt file, that I have provided.

```
pip install -r requirements.txt
```

Create a folder called `voices` and put these two files there:

[en_US-ryan-high.onnx](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/ryan/high/en_US-ryan-high.onnx)
[en_US-ryan-high.onnx.json](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/ryan/high/en_US-ryan-high.onnx.json)

---
# Ollama

Install Ollama

Run,

```
ollama pull gemma3:1b # or a better model if your computer supports it
ollama pull mxbai-embed-large # for embeddings, you can use whatever you choose
```

---

