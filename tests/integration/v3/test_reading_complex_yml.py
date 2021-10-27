"""Integration tests for reading evergreen yml."""
from shrub.v3.evg_project import EvgProject


class TestReadingEvergreenYaml:
    def test_reading_complex_yaml(self, sample_files_location):
        project = EvgProject.from_file(sample_files_location / "mongo_evergreen.yml")

        assert len(project.pre) == 2
        assert len(project.tasks) == 367

        build_variants = [bv.name for bv in project.buildvariants]
        assert "linux-64-duroff" in build_variants

        assert project.modules[0].get_repository_name() == "mongo-enterprise-modules"
