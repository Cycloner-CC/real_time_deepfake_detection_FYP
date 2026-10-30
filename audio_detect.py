import torch
import librosa
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

def audio_detect(model=None,feature_extractor=None,file="outputs/audio.wav"):

    # Load model and feature extractor
    if model == None or feature_extractor == None:
        audio_model_name = "garystafford/wav2vec2-deepfake-voice-detector"
        model = AutoModelForAudioClassification.from_pretrained(audio_model_name)
        feature_extractor = AutoFeatureExtractor.from_pretrained(audio_model_name)
    else:
        model = model
        feature_extractor = feature_extractor

    # Move to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    # Load and preprocess audio (automatically resamples to 16kHz)
    audio, sr = librosa.load(file, sr=16000, mono=True)
    inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

    # Get prediction
    prob_real = probs[0][0].item()
    prob_fake = probs[0][1].item()
    # prediction = "fake" if prob_fake > 0.5 else "real"

    # print(f"Prediction: {prediction}")
    # print(f"Confidence: {max(prob_real, prob_fake):.2%}")
    # print(f"Probabilities - Real: {prob_real:.2%}, Fake: {prob_fake:.2%}")

    return prob_fake


if __name__ == "__main__":
    audio_model_name = "garystafford/wav2vec2-deepfake-voice-detector"
    audio_model = AutoModelForAudioClassification.from_pretrained(audio_model_name)
    feature_extractor = AutoFeatureExtractor.from_pretrained(audio_model_name)
    print(torch.cuda.is_available())
    print(audio_detect(audio_model,feature_extractor))
    print(audio_detect())