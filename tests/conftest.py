import pytest
import tempfile
import os
from unittest.mock import Mock, MagicMock
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test response"
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_speech_recognizer():
    """Mock speech recognizer for testing."""
    mock_recognizer = Mock()
    mock_recognizer.recognize_google.return_value = "test speech"
    return mock_recognizer


@pytest.fixture
def mock_tts_engine():
    """Mock text-to-speech engine for testing."""
    mock_engine = Mock()
    mock_voice = Mock()
    mock_voice.id = "test_voice_id"
    mock_engine.getProperty.return_value = [mock_voice, mock_voice, mock_voice]
    return mock_engine


@pytest.fixture
def mock_gtts():
    """Mock gTTS for testing."""
    mock_gtts = Mock()
    return mock_gtts


@pytest.fixture
def mock_playsound():
    """Mock playsound function for testing."""
    return Mock()


@pytest.fixture
def mock_microphone():
    """Mock microphone source for testing."""
    mock_mic = Mock()
    return mock_mic


@pytest.fixture
def sample_messages():
    """Sample messages for testing chat functionality."""
    return [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]


@pytest.fixture
def mock_audio_file(temp_dir):
    """Create a mock audio file for testing."""
    audio_file = temp_dir / "test_audio.mp3"
    audio_file.write_bytes(b"fake audio data")
    return audio_file


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    yield
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


@pytest.fixture(autouse=True)
def disable_audio_playback(monkeypatch):
    """Automatically disable audio playback in all tests."""
    # Mock pygame.mixer for audio playback
    monkeypatch.setattr("pygame.mixer.init", Mock())
    monkeypatch.setattr("pygame.mixer.music.load", Mock())
    monkeypatch.setattr("pygame.mixer.music.play", Mock())
    

@pytest.fixture
def mock_numpy():
    """Mock numpy for testing."""
    mock_np = Mock()
    mock_np.random.choice.return_value = "Test greeting"
    return mock_np