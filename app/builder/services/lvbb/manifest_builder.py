from typing import List

from app.builder.services import BuilderService
from app.builder.state_manager.models import OutputFile, StrContentData
from app.builder.state_manager.state_manager import StateManager
from app.models import ContentType
from app.services.utils.helpers import load_template


class ManifestBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        manifest_file = self._create_manifest_file(
            state_manager.get_output_files(),
        )
        state_manager.add_output_file(manifest_file)

        return state_manager

    def _create_manifest_file(self, output_files: List[OutputFile]) -> OutputFile:
        content = load_template(
            "templates/lvbb/manifest.xml",
            pretty_print=True,
            output_files=output_files,
        )
        output_file = OutputFile(
            filename="manifest.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
