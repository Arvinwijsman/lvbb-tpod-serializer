from app.builder.services import BuilderService
from app.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from app.builder.state_manager.models import OutputFile, StrContentData
from app.builder.state_manager.state_manager import StateManager
from app.models import ContentType
from app.services.utils.hashlib import compute_sha512_of_output_file
from app.services.utils.helpers import load_template


class GioAanleveringInformatieObjectBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()

        for werkingsgebied in werkingsgebieden:
            output_file: OutputFile = self._generate_gio(state_manager, werkingsgebied)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_gio(
        self,
        state_manager: StateManager,
        werkingsgebied: Werkingsgebied,
    ):
        gml_filename = werkingsgebied.get_gml_filename()
        output_file = state_manager.get_output_file_by_filename(gml_filename)
        gml_hash = compute_sha512_of_output_file(output_file)

        content = load_template(
            "templates/geo/AanleveringInformatieObject.xml",
            pretty_print=True,
            werkingsgebied_frbr=werkingsgebied.get_FRBR(),
            bestandsnaam=werkingsgebied.get_gml_filename(),
            gml_hash=gml_hash,
            regeling_frbr=state_manager.input_data.publication_settings.regeling_frbr,
            provincie_ref=state_manager.input_data.publication_settings.provincie_ref,
            naamInformatie_object=werkingsgebied.Title,
        )

        output_file = OutputFile(
            filename=werkingsgebied.get_gio_filename(),
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
