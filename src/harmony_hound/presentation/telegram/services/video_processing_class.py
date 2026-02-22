import uuid
from pathlib import Path

from harmony_hound.application.common.utils import get_static_root
from harmony_hound.presentation.telegram.services.abstract_processing_class import AbstractProcessingClass


class VideoProcessingClass(AbstractProcessingClass):
    def get_source_full_path(self, message, file_path) -> Path:
        file_type = message.video.mime_type.split('/')[1]
        file_name = str(uuid.uuid4()) + '.' + file_type

        print(f"video file id {message.video.file_id}")
        print(f"file_path: {file_path}")
        print(f"file_type: {file_type}")
        print(f"file_name: {file_name}")

        full_file_path = get_static_root() / file_name
        return full_file_path

    def get_source_id(self, message) -> str:
        video_id = message.video.file_id

        return video_id