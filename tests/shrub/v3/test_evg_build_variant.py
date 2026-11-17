"""Unit tests for evg_build_variant.py."""
from shrub.v3.evg_build_variant import BuildVariant
from shrub.v3.evg_project import EvgProject
from shrub.v3.shrub_service import ShrubService


class TestBuildVariantFields:
    def test_build_variant_allowed_requesters(self):
        variant = BuildVariant(name="variant", tasks=[], allowed_requesters=["commit"])
        out = ShrubService.generate_yaml(EvgProject(buildvariants=[variant], tasks=[]))
        assert "allowed_requesters:" in out
        assert "- commit" in out

    def test_build_variant_allowed_requesters_absent_when_unset(self):
        variant = BuildVariant(name="variant", tasks=[])
        out = ShrubService.generate_yaml(EvgProject(buildvariants=[variant], tasks=[]))
        assert "allowed_requesters" not in out
