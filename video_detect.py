from transformers import pipeline

def video_detect(file="outputs/video_w_audio.mp4"):
    clf = pipeline(
        "video-classification",
        model="KoreaPeter/ms-eff-gcvit-deepfake-b0-ff-plus-plus", 
        trust_remote_code=True,
    )

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
    if len(result) > 1 :
        return result[1]["score"]
    else :
        return result[0]["score"]
    
    # [{'label': 'fake', 'score': 0.9634},
    #  {'label': 'real', 'score': 0.0366},
    #  {'frame_scores': [0.97, 0.95, 0.98, ...], 'agg_mode': 'conf'}]

if __name__ == "__main__":
    print(video_detect())