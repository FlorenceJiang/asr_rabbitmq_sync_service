import torch
import numpy as np
from transformers import Wav2Vec2Processor, HubertForCTC


class ASR():
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/hubert-large-ls960-ft")
        self.model = HubertForCTC.from_pretrained("facebook/hubert-large-ls960-ft")

    def transcribe(self, input):
        # TODO: input could be either bytes or array depending on what you want.
        input_values = self.processor(input, return_tensors="pt", sampling_rate=16000).input_values  # Batch size 1
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])
        return transcription


model = ASR()
sr, duration = 16000, 5
input = np.random.randn(sr * duration)
transcript = model.transcribe(input)
print(transcript)