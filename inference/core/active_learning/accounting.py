from typing import List, Optional

from inference.core.entities.types import DatasetID, WorkspaceID
from inference.core.roboflow_api import (
    get_roboflow_labeling_batches,
    get_roboflow_labeling_jobs,
)


def image_can_be_submitted_to_batch(
    batch_name: str,
    workspace_id: WorkspaceID,
    dataset_id: DatasetID,
    max_batch_images: Optional[int],
    api_key: str,
) -> bool:
    if max_batch_images is None:
        return True
    labeling_batches = get_roboflow_labeling_batches(
        api_key=api_key,
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )
    matching_labeling_batch = get_matching_labeling_batch(
        all_labeling_batches=labeling_batches["batches"],
        batch_name=batch_name,
    )
    if matching_labeling_batch is None:
        return max_batch_images > 0
    batch_images_under_labeling = 0
    if matching_labeling_batch["numJobs"] > 0:
        labeling_jobs = get_roboflow_labeling_jobs(
            api_key=api_key, workspace_id=workspace_id, dataset_id=dataset_id
        )
        batch_images_under_labeling = get_images_in_labeling_jobs_of_specific_batch(
            all_labeling_jobs=labeling_jobs["jobs"],
            batch_id=matching_labeling_batch["id"],
        )
    total_batch_images = matching_labeling_batch["images"] + batch_images_under_labeling
    return max_batch_images > total_batch_images


def get_matching_labeling_batch(
    all_labeling_batches: List[dict],
    batch_name: str,
) -> Optional[dict]:
    matching_batch = None
    for labeling_batch in all_labeling_batches:
        if labeling_batch["name"] == batch_name:
            matching_batch = labeling_batch
            break
    return matching_batch


def get_images_in_labeling_jobs_of_specific_batch(
    all_labeling_jobs: List[dict],
    batch_id: str,
) -> int:
    matching_jobs = []
    for labeling_job in all_labeling_jobs:
        if batch_id in labeling_job["sourceBatch"]:
            matching_jobs.append(labeling_job)
    return sum(job["numImages"] for job in matching_jobs)
