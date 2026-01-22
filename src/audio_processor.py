import whisper
import json
import os
# import senko  <-- REMOVED to fix installation error

class AudioProcessor:
    def __init__(self, model_size="base", device="auto"):
        """
        Initialize Whisper model only.
        """
        if device == "auto":
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                self.device = "cpu"
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Initialize Whisper
        print(f"Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size, device=self.device)
        print("Whisper model loaded.")

    def process_audio(self, file_path):
        """
        Process audio file: Transcribe ONLY.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # 1. Transcription (Whisper)
        print(f"Transcribing {file_path}...")
        whisper_result = self.model.transcribe(file_path)

        # 2. Format Output
        diarized_transcript = []

        for seg in whisper_result["segments"]:
            diarized_transcript.append({
                "start": seg["start"],
                "end": seg["end"],
                "speaker": "Speaker",  # Generic label since Senko is removed
                "text": seg["text"].strip()
            })

        return diarized_transcript

    def export_to_json(self, transcript_data, output_path):
        with open(output_path, 'w') as f:
            json.dump(transcript_data, f, indent=4)
        return output_path