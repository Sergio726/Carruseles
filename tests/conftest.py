import pytest


@pytest.fixture
def tmp_historial(tmp_path, monkeypatch):
    """Redirige REPO_ROOT e HISTORIAL a directorio temporal."""
    import stlabs_memory as mem

    monkeypatch.setattr(mem, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mem, "HISTORIAL_DIR", tmp_path / "historial")
    monkeypatch.setattr(mem, "BUILDS_DIR", tmp_path / "builds")
    monkeypatch.setattr(mem, "INDEX_PATH", tmp_path / "historial" / "carruseles.json")
    (tmp_path / "historial").mkdir()
    (tmp_path / "builds").mkdir()
    yield tmp_path
