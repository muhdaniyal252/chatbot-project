import pytest
from LLMs import get_llm

from unittest.mock import patch

def test_gptllm_invoke():
    llm = get_llm('gpt')
    assert hasattr(llm, 'invoke')
    with patch.object(llm, 'invoke', side_effect=Exception('Mocked error')):
        with pytest.raises(Exception):
            llm.invoke('test')

def test_geminillm_invoke():
    llm = get_llm('gemini')
    assert hasattr(llm, 'invoke')
    with patch.object(llm, 'invoke', side_effect=Exception('Mocked error')):
        with pytest.raises(Exception):
            llm.invoke('test')
