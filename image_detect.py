from transformers import pipeline
import torch


def image_detect(file="outputs/image_test.png"):
    clf = pipeline(
        "image-classification",
        model="KoreaPeter/ms-eff-gcvit-deepfake-b0-ff-plus-plus", 
        device = "cuda" if torch.cuda.is_available() else "cpu",
        trust_remote_code=True,
    )

    # ── Basic Inference ───────────────────────────────────────────────
    result = clf(file)
    # [{'label': 'fake', 'score': 0.9712}, {'label': 'real', 'score': 0.0288}]

    # ── Custom Parameters ─────────────────────────────────────────────
    # result = clf(
    #     file,
    #     margin_ratio=0.2,      # Margin ratio around the detected face bbox (default: 0.2)
    #     conf_thres=0.5,        # Confidence threshold for YOLO face detection (default: 0.5)
    #     min_face_ratio=0.01,   # Minimum face-to-frame area ratio to process (default: 0.01)
    #     tta_hflip=0.0,         # Probability of horizontal flip for TTA (default: 0.0)
    #     top_k=1,               # Number of top labels to return (default: all)
    # )
    # [{'label': 'fake', 'score': 0.9712}]

    return result[0]["score"]

if __name__ == "__main__":
    print(image_detect("outputs/image_test.png"))
