"""
Validation tests to verify the testing infrastructure works correctly.
"""
import pytest
import sys
from pathlib import Path


def test_python_version():
    """Test that we're running on a supported Python version."""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


def test_pytest_markers():
    """Test that custom markers are registered."""
    # This will fail if markers aren't properly configured in pyproject.toml
    pytest.mark.unit
    pytest.mark.integration  
    pytest.mark.slow


def test_fixtures_available(temp_dir, mock_openai_client):
    """Test that shared fixtures are available."""
    assert temp_dir.exists()
    assert mock_openai_client is not None


def test_project_structure():
    """Test that the project structure is correct."""
    project_root = Path(__file__).parent.parent
    
    # Check main files exist
    assert (project_root / "chatgpt_voice.py").exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / ".gitignore").exists()
    
    # Check test structure
    tests_dir = project_root / "tests"
    assert tests_dir.exists()
    assert (tests_dir / "__init__.py").exists()
    assert (tests_dir / "conftest.py").exists()
    assert (tests_dir / "unit" / "__init__.py").exists()
    assert (tests_dir / "integration" / "__init__.py").exists()


@pytest.mark.unit
def test_unit_marker():
    """Test that unit marker works."""
    assert True


@pytest.mark.integration  
def test_integration_marker():
    """Test that integration marker works."""
    assert True


@pytest.mark.slow
def test_slow_marker():
    """Test that slow marker works."""
    assert True


def test_mock_audio_disabled():
    """Test that audio playback is mocked in tests."""
    # This fixture should be automatically applied
    # If pygame.mixer is not mocked, this could cause issues in headless environments
    from unittest.mock import Mock
    import pygame.mixer
    assert isinstance(pygame.mixer.init, Mock)


def test_sample_data_fixtures(sample_messages, mock_audio_file):
    """Test that sample data fixtures work."""
    assert len(sample_messages) == 3
    assert sample_messages[0]["role"] == "system"
    assert mock_audio_file.exists()
    assert mock_audio_file.suffix == ".mp3"