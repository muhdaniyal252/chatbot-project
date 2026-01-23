import pytest
from unittest.mock import AsyncMock, patch
import io
from TTSs import get_tts
from STTs import get_stt

@pytest.mark.asyncio
async def test_tts_stt_roundtrip():
    original_text = "Hello, this is a test message."
    tts = get_tts('openai')
    stt = get_stt('openai')
    audio_buffer = io.BytesIO()

    # Mock TTS synthesize to write dummy audio bytes
    with patch.object(tts, 'synthesize', new=AsyncMock()) as mock_tts_synth:
        mock_tts_synth.side_effect = lambda text, buf: buf.write(b'dummy-audio-bytes')
        await tts.synthesize(original_text, audio_buffer)
        audio_buffer.seek(0)

    # Mock STT transcribe to return the original text
    with patch.object(stt, 'transcribe', new=AsyncMock(return_value=original_text)):
        transcribed_text = await stt.transcribe(audio_buffer)

    assert transcribed_text == original_text
