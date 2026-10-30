from transformers import pipeline
import torch

def video_detect(clf=None,file="outputs/video_w_audio.mp4"):
    if clf == None:
        clf = pipeline(
            "video-classification",
            model="KoreaPeter/ms-eff-gcvit-deepfake-b0-ff-plus-plus", 
            device = "cuda" if torch.cuda.is_available() else "cpu",
            trust_remote_code=True,
        )
    else:
        clf = clf

    # ── Basic Inference ───────────────────────────────────────────────
    result = clf(file)
    # [{'label': 'fake', 'score': 0.9634}, {'label': 'real', 'score': 0.0366}]

    # ── Custom Parameters ─────────────────────────────────────────────
    # result = clf(
    #     "video.mp4",
    #     num_frames=20,              # Number of frames to sample (default: 20)
    #     margin_ratio=0.2,           # Margin ratio around the detected face bbox (default: 0.2)
    #     conf_thres=0.5,             # Confidence threshold for YOLO face detection (default: 0.5)
    #     min_face_ratio=0.01,        # Minimum face-to-frame area ratio to process (default: 0.01)
    #     tta_hflip=0.0,              # Probability of horizontal flip for TTA (default: 0.0)
    #     agg_mode="conf",            # Aggregation mode: 'conf' | 'mean' | 'vote' (default: 'conf')
    #     return_frame_scores=True,   # Return per-frame scores (default: False)
    # )

    return result[0]["score"]
    
    # [{'label': 'fake', 'score': 0.9634},
    #  {'label': 'real', 'score': 0.0366},
    #  {'frame_scores': [0.97, 0.95, 0.98, ...], 'agg_mode': 'conf'}]

if __name__ == "__main__":
    video_model = pipeline(
                "video-classification",
                model="KoreaPeter/ms-eff-gcvit-deepfake-b0-ff-plus-plus", 
                device = "cuda" if torch.cuda.is_available() else "cpu",
                trust_remote_code=True,
            )
    print(video_detect(video_model))