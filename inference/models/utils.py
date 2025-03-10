from inference.core.env import API_KEY
from inference.core.models.stubs import (
    ClassificationModelStub,
    InstanceSegmentationModelStub,
    KeypointsDetectionModelStub,
    ObjectDetectionModelStub,
)
from inference.core.registries.roboflow import get_model_type
from inference.models import (
    YOLACT,
    VitClassification,
    YOLOv5InstanceSegmentation,
    YOLOv5ObjectDetection,
    YOLOv7InstanceSegmentation,
    YOLOv8Classification,
    YOLOv8InstanceSegmentation,
    YOLOv8ObjectDetection,
)
from inference.models.yolov8.yolov8_keypoints_detection import YOLOv8KeypointsDetection

ROBOFLOW_MODEL_TYPES = {
    ("classification", "stub"): ClassificationModelStub,
    ("classification", "vit"): VitClassification,
    ("classification", "yolov8n"): YOLOv8Classification,
    ("classification", "yolov8s"): YOLOv8Classification,
    ("classification", "yolov8m"): YOLOv8Classification,
    ("classification", "yolov8l"): YOLOv8Classification,
    ("classification", "yolov8x"): YOLOv8Classification,
    ("object-detection", "stub"): ObjectDetectionModelStub,
    ("object-detection", "yolov5"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v2s"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v6n"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v6s"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v6m"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v6l"): YOLOv5ObjectDetection,
    ("object-detection", "yolov5v6x"): YOLOv5ObjectDetection,
    ("object-detection", "yolov8"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8s"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8n"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8s"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8m"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8l"): YOLOv8ObjectDetection,
    ("object-detection", "yolov8x"): YOLOv8ObjectDetection,
    ("instance-segmentation", "stub"): InstanceSegmentationModelStub,
    (
        "instance-segmentation",
        "yolov5-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov5n-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov5s-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov5m-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov5l-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov5x-seg",
    ): YOLOv5InstanceSegmentation,
    (
        "instance-segmentation",
        "yolact",
    ): YOLACT,
    (
        "instance-segmentation",
        "yolov7-seg",
    ): YOLOv7InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8n",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8s",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8m",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8l",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8x",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8n-seg",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8s-seg",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8m-seg",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8l-seg",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8x-seg",
    ): YOLOv8InstanceSegmentation,
    (
        "instance-segmentation",
        "yolov8-seg",
    ): YOLOv8InstanceSegmentation,
    ("keypoints-detection", "stub"): KeypointsDetectionModelStub,
    ("keypoints-detection", "yolov8n"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8s"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8m"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8l"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8x"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8n-pose"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8s-pose"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8m-pose"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8l-pose"): YOLOv8KeypointsDetection,
    ("keypoints-detection", "yolov8x-pose"): YOLOv8KeypointsDetection,
}

try:
    from inference.models import SegmentAnything

    ROBOFLOW_MODEL_TYPES[("embed", "sam")] = SegmentAnything
except:
    pass

try:
    from inference.models import Clip

    ROBOFLOW_MODEL_TYPES[("embed", "clip")] = Clip
except:
    pass

try:
    from inference.models import Gaze

    ROBOFLOW_MODEL_TYPES[("gaze", "l2cs")] = Gaze
except:
    pass

try:
    from inference.models import DocTR

    ROBOFLOW_MODEL_TYPES[("ocr", "doctr")] = DocTR
except:
    pass


def get_roboflow_model(model_id, api_key=API_KEY, **kwargs):
    task, model = get_model_type(model_id, api_key=api_key)
    return ROBOFLOW_MODEL_TYPES[(task, model)](model_id, api_key=api_key, **kwargs)
