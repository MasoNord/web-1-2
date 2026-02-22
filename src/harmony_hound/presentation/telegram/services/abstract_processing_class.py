import os
from abc import ABC, abstractmethod
from pathlib import Path

import ffmpeg

from harmony_hound.application.common.dto import SongRecognitionResponse
from harmony_hound.application.common.exceptions import FileSizeLimitError, FileDurationLimitError
from harmony_hound.main.config import bot, load_application_specific_config
from harmony_hound.presentation.telegram.services.google_drive_service import GoogleDriveService
from harmony_hound.presentation.telegram.services.recognition_service import RecognitionService

config = load_application_specific_config()

class AbstractProcessingClass(ABC):
    """
    The Abstract Processing Clas will serve as a template method that contains a skeleton of
    the algorithm for processing audio from different sources
    """

    async def process_source(self, message):
        google_drive_service = GoogleDriveService()
        recognition_service = RecognitionService()

        source_id = self.get_source_id(message)

        source = await bot.get_file(source_id)

        source_path = source.file_path

        full_file_path = self.get_source_full_path(message, source_path)

        await bot.download_file(source_path, full_file_path)

        res = self.check_file_size(full_file_path)

        if not res:
            raise FileSizeLimitError("The file size limit exceeded")

        res = self.check_file_duration(full_file_path)

        if res is None:
            raise Exception("Something went wrong while processing your file")

        if not res:
            raise FileDurationLimitError("The file duration limit exceeded")

        google_drive_source_id = google_drive_service.upload_file(full_file_path)
        web_view_link = google_drive_service.get_web_view_link(google_drive_source_id)

        # Applying permission flags in order the recognition service
        # will be able to download and recognise a given song
        google_drive_service.apply_share_flag(google_drive_source_id)

        # Recognise song by web_view_link
        result = recognition_service.recognise_song(web_view_link)

        # Removing uploaded file from a Google Drive storage
        google_drive_service.delete_file_by_id(google_drive_source_id)

        # Removing downloaded file from a file system
        os.remove(full_file_path)

        parsed_response = self.parse_result(result)

        return parsed_response

    def parse_result(self, result: str) -> SongRecognitionResponse:
        result = SongRecognitionResponse()
        return result

    def check_file_size(self, full_file_path: Path):
        size_in_bytes = os.path.getsize(full_file_path)

        # Converting bytes to megabytes
        size_in_megabytes = size_in_bytes / 1_048_576

        if size_in_megabytes > config.file_size_limit:
            return False

        return True

    def check_file_duration(self, full_file_path: Path):
        try:
            probe = ffmpeg.probe(full_file_path)

            duration = float(probe['format']['duration'])

            if duration > config.file_duration_limit:
                return False

            return True
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            return None
        except KeyError:
            print("Could not find duration in file metadata. Ensure the file is a valid media file.")
            return None
        except FileNotFoundError:
            print(f"File not found: {full_file_path}. Make sure FFprobe is installed and in your PATH.")
            return None

    @abstractmethod
    def get_source_full_path(self, message, file_path) -> Path:
        pass

    @abstractmethod
    def get_source_id(self, message) -> str:
        pass

async def client_code(abstract_class: AbstractProcessingClass, message) -> SongRecognitionResponse:
    return await abstract_class.process_source(message)