import base64
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ObjectDetectionPrediction(BaseModel):
    """Object Detection prediction.

    Attributes:
        x (float): The center x-axis pixel coordinate of the prediction.
        y (float): The center y-axis pixel coordinate of the prediction.
        width (float): The width of the prediction bounding box in number of pixels.
        height (float): The height of the prediction bounding box in number of pixels.
        confidence (float): The detection confidence as a fraction between 0 and 1.
        class_name (str): The predicted class label.
        class_confidence (Union[float, None]): The class label confidence as a fraction between 0 and 1.
        class_id (int): The class id of the prediction
    """

    x: float = Field(description="The center x-axis pixel coordinate of the prediction")
    y: float = Field(description="The center y-axis pixel coordinate of the prediction")
    width: float = Field(
        description="The width of the prediction bounding box in number of pixels"
    )
    height: float = Field(
        description="The height of the prediction bounding box in number of pixels"
    )
    confidence: float = Field(
        description="The detection confidence as a fraction between 0 and 1"
    )
    class_name: str = Field(alias="class", description="The predicted class label")

    class_confidence: Union[float, None] = Field(
        description="The class label confidence as a fraction between 0 and 1"
    )
    class_id: int = Field(description="The class id of the prediction")
    tracker_id: Optional[int] = Field(
        description="The tracker id of the prediction if tracking is enabled",
        default=None,
    )


class Point(BaseModel):
    """Point coordinates.

    Attributes:
        x (float): The x-axis pixel coordinate of the point.
        y (float): The y-axis pixel coordinate of the point.
    """

    x: float = Field(description="The x-axis pixel coordinate of the point")
    y: float = Field(description="The y-axis pixel coordinate of the point")


class Point3D(Point):
    """3D Point coordinates.

    Attributes:
        z (float): The z-axis pixel coordinate of the point.
    """

    z: float = Field(description="The z-axis pixel coordinate of the point")


class InstanceSegmentationPrediction(BaseModel):
    """Instance Segmentation prediction.

    Attributes:
        x (float): The center x-axis pixel coordinate of the prediction.
        y (float): The center y-axis pixel coordinate of the prediction.
        width (float): The width of the prediction bounding box in number of pixels.
        height (float): The height of the prediction bounding box in number of pixels.
        confidence (float): The detection confidence as a fraction between 0 and 1.
        class_name (str): The predicted class label.
        class_confidence (Union[float, None]): The class label confidence as a fraction between 0 and 1.
        points (List[Point]): The list of points that make up the instance polygon.
        class_id: int = Field(description="The class id of the prediction")
    """

    x: float = Field(description="The center x-axis pixel coordinate of the prediction")
    y: float = Field(description="The center y-axis pixel coordinate of the prediction")
    width: float = Field(
        description="The width of the prediction bounding box in number of pixels"
    )
    height: float = Field(
        description="The height of the prediction bounding box in number of pixels"
    )
    confidence: float = Field(
        description="The detection confidence as a fraction between 0 and 1"
    )
    class_name: str = Field(alias="class", description="The predicted class label")

    class_confidence: Union[float, None] = Field(
        description="The class label confidence as a fraction between 0 and 1"
    )
    points: List[Point] = Field(
        description="The list of points that make up the instance polygon"
    )
    class_id: int = Field(description="The class id of the prediction")


class ClassificationPrediction(BaseModel):
    """Classification prediction.

    Attributes:
        class_name (str): The predicted class label.
        class_id (int): Numeric ID associated with the class label.
        confidence (float): The class label confidence as a fraction between 0 and 1.
    """

    class_name: str = Field(alias="class", description="The predicted class label")
    class_id: int = Field(description="Numeric ID associated with the class label")
    confidence: float = Field(
        description="The class label confidence as a fraction between 0 and 1"
    )


class MultiLabelClassificationPrediction(BaseModel):
    """Multi-label Classification prediction.

    Attributes:
        confidence (float): The class label confidence as a fraction between 0 and 1.
    """

    confidence: float = Field(
        description="The class label confidence as a fraction between 0 and 1"
    )


class InferenceResponseImage(BaseModel):
    """Inference response image information.

    Attributes:
        width (int): The original width of the image used in inference.
        height (int): The original height of the image used in inference.
    """

    width: int = Field(description="The original width of the image used in inference")
    height: int = Field(
        description="The original height of the image used in inference"
    )


class InferenceResponse(BaseModel):
    """Base inference response.

    Attributes:
        frame_id (Optional[int]): The frame id of the image used in inference if the input was a video.
        time (Optional[float]): The time in seconds it took to produce the predictions including image preprocessing.
    """

    frame_id: Optional[int] = Field(
        default=None,
        description="The frame id of the image used in inference if the input was a video",
    )
    time: Optional[float] = Field(
        default=None,
        description="The time in seconds it took to produce the predictions including image preprocessing",
    )


class CvInferenceResponse(InferenceResponse):
    """Computer Vision inference response.

    Attributes:
        image (Union[List[inference.core.entities.responses.inference.InferenceResponseImage], inference.core.entities.responses.inference.InferenceResponseImage]): Image(s) used in inference.
    """

    image: Union[List[InferenceResponseImage], InferenceResponseImage]


class WithVisualizationResponse(BaseModel):
    """Response with visualization.

    Attributes:
        visualization (Optional[Any]): Base64 encoded string containing prediction visualization image data.
    """

    visualization: Optional[Any] = Field(
        default=None,
        description="Base64 encoded string containing prediction visualization image data",
    )

    # We need to tell pydantic how to encode bytes as base64 strings. We don't encode the visualization field directly because we want to return it directly for the legacy infer route with content type image/jpeg.
    class Config:
        json_encoders = {bytes: lambda v: base64.b64encode(v).decode("utf-8")}


class ObjectDetectionInferenceResponse(CvInferenceResponse, WithVisualizationResponse):
    """Object Detection inference response.

    Attributes:
        predictions (List[inference.core.entities.responses.inference.ObjectDetectionPrediction]): List of object detection predictions.
    """

    predictions: List[ObjectDetectionPrediction]


class Keypoint(Point):
    confidence: float = Field(
        description="Model confidence regarding keypoint visibility."
    )
    class_id: int = Field(description="Identifier of keypoint.")
    class_name: str = Field(field="class", description="Type of keypoint.")


class KeypointsPrediction(ObjectDetectionPrediction):
    keypoints: List[Keypoint]


class KeypointsDetectionInferenceResponse(
    CvInferenceResponse, WithVisualizationResponse
):
    predictions: List[KeypointsPrediction]


class InstanceSegmentationInferenceResponse(
    CvInferenceResponse, WithVisualizationResponse
):
    """Instance Segmentation inference response.

    Attributes:
        predictions (List[inference.core.entities.responses.inference.InstanceSegmentationPrediction]): List of instance segmentation predictions.
    """

    predictions: List[InstanceSegmentationPrediction]


class ClassificationInferenceResponse(CvInferenceResponse, WithVisualizationResponse):
    """Classification inference response.

    Attributes:
        predictions (List[inference.core.entities.responses.inference.ClassificationPrediction]): List of classification predictions.
        top (str): The top predicted class label.
        confidence (float): The confidence of the top predicted class label.
    """

    predictions: List[ClassificationPrediction]
    top: str = Field(description="The top predicted class label")
    confidence: float = Field(
        description="The confidence of the top predicted class label"
    )


class MultiLabelClassificationInferenceResponse(
    CvInferenceResponse, WithVisualizationResponse
):
    """Multi-label Classification inference response.

    Attributes:
        predictions (Dict[str, inference.core.entities.responses.inference.MultiLabelClassificationPrediction]): Dictionary of multi-label classification predictions.
        predicted_classes (List[str]): The list of predicted classes.
    """

    predictions: Dict[str, MultiLabelClassificationPrediction]
    predicted_classes: List[str] = Field(description="The list of predicted classes")


class FaceDetectionPrediction(ObjectDetectionPrediction):
    """Face Detection prediction.

    Attributes:
        class_name (str): fixed value "face".
        landmarks (Union[List[inference.core.entities.responses.inference.Point], List[inference.core.entities.responses.inference.Point3D]]): The detected face landmarks.
    """

    class_id: Optional[int] = Field(
        description="The class id of the prediction", default=0
    )
    class_name: str = Field(
        alias="class", default="face", description="The predicted class label"
    )
    landmarks: Union[List[Point], List[Point3D]]


class StubResponse(InferenceResponse, WithVisualizationResponse):
    is_stub: bool = Field(description="Field to mark prediction type as stub")
    model_id: str = Field(description="Identifier of a model stub that was called")
    task_type: str = Field(description="Task type of the project")
