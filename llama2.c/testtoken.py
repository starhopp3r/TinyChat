import os
import struct
import argparse
from typing import List

from sentencepiece import SentencePieceProcessor

TOKENIZER_MODEL = "tokenizer.model" # the llama sentencepiece tokenizer model

class Tokenizer:
    def __init__(self, tokenizer_model=None):
        model_path = tokenizer_model if tokenizer_model else TOKENIZER_MODEL
        assert os.path.isfile(model_path), model_path
        self.sp_model = SentencePieceProcessor(model_file=model_path)
        self.model_path = model_path

        # BOS / EOS token IDs
        self.n_words: int = self.sp_model.vocab_size()
        self.bos_id: int = self.sp_model.bos_id()
        self.eos_id: int = self.sp_model.eos_id()
        self.pad_id: int = self.sp_model.pad_id()
        #print(f"#words: {self.n_words} - BOS ID: {self.bos_id} - EOS ID: {self.eos_id}")
        assert self.sp_model.vocab_size() == self.sp_model.get_piece_size()

    def encode(self, s: str, bos: bool, eos: bool) -> List[int]:
        assert type(s) is str
        # Split the input text by "[INST]" tag
        segments = s.split("[INST]")
        # Initialize the final encoded list
        final_encoding = []
        # Process each segment
        for segment in segments:
            # Check if the segment is not empty
            if segment.strip():
                # Strip the segment of leading/trailing whitespaces
                segment = "[INST] " + segment.strip()
                # Encode the segment using the SentencePiece model
                t = self.sp_model.encode(segment)
                # Add BOS and EOS tokens if specified
                if bos:
                    t = [self.bos_id] + t
                if eos:
                    t = t + [self.eos_id]
                # Append the encoded segment to the final encoding list
                final_encoding += t
        # Return fully encoded text
        return final_encoding

    def decode(self, t: List[int]) -> str:
            return self.sp_model.decode(t)


if __name__ == "__main__":
    text = "TEST DATA GOES HERE"
    t = Tokenizer()
    encoded_text = t.encode(text, True, True)
    print(encoded_text)
    print(t.decode(encoded_text))