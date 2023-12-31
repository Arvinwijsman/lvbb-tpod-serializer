from app.builder.services import BuilderService
from app.builder.services.ow.ow_divisie import OwDivisieContent
from app.builder.services.ow.ow_locaties import OwLocatiesContent
from app.builder.services.ow.ow_manifest import ManifestContent
from app.builder.services.ow.ow_regelinggebied import OwRegelingsgebiedContent
from app.builder.state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    """
    The OwBuilder class is responsible for building IMOW related objects
    and generating output files in XML format.

    Builds: OWGebied, OWGebiedenGroep, OWDivisie, OWDivisieTekst, OWTekstDeel for annotating policy.
    """

    def apply(self, state_manager: StateManager) -> StateManager:
        """
        Create all ow objects and save the output files to state
        """
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()
        leveringid = state_manager.input_data.publication_settings.opdracht.id_levering

        locaties_content = OwLocatiesContent(
            werkingsgebieden=werkingsgebieden,
            object_tekst_lookup=state_manager.object_tekst_lookup,
            levering_id=leveringid,
        )
        locaties_state = locaties_content.create_locations()
        state_manager.ow_repository.store_locaties_content(locaties_state)

        divisie_content = OwDivisieContent(
            object_tekst_lookup=state_manager.object_tekst_lookup,
            levering_id=leveringid,
        )
        divisie_state = divisie_content.create_divisies()
        state_manager.ow_repository.store_divisie_content(divisie_state)

        regelinggebied_content = OwRegelingsgebiedContent(levering_id=leveringid)
        regelinggebied_state = regelinggebied_content.create_regelingen()
        state_manager.ow_repository.store_regelingsgebied_content(regelinggebied_state)

        manifest_content = ManifestContent(
            act_akn=str(state_manager.input_data.publication_settings.regeling_frbr.work),
            doel=state_manager.input_data.publication_settings.doel,
        )

        manifest_content.create_manifest(
            state_manager.ow_repository.divisie_content,
            state_manager.ow_repository.locaties_content,
            state_manager.ow_repository.regelingsgebied_content,
        )

        state_manager.add_output_file(locaties_content.file)
        state_manager.add_output_file(divisie_content.file)
        state_manager.add_output_file(regelinggebied_content.file)
        state_manager.add_output_file(manifest_content.file)

        return state_manager
