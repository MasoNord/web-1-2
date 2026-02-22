import uuid
from pathlib import Path

from harmony_hound.application.common.utils import get_static_root
from harmony_hound.presentation.telegram.services.abstract_processing_class import AbstractProcessingClass


class VideoNoteProcessingClass(AbstractProcessingClass):
    def get_source_full_path(self, message, file_path) -> Path:
        file_type = "mp4"
        file_name = str(uuid.uuid4()) + "." + file_type

        full_file_path = get_static_root() / file_name

        print(f"video note file id {message.video_note.file_id}")
        print(f"file_path: {file_path}")
        print(f"file_type: {file_type}")
        print(f"file_name: {file_name}")

        return full_file_path

    def get_source_id(self, message) -> str:
        video_id = message.video_note.file_id

        return video_id