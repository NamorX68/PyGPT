import pytest
from unittest.mock import Mock, patch
from pygpt.llm.gpt import GptApi


def test_gpt_api():
    with patch('pygpt.llm.gpt.ChatOpenAI', return_value=Mock()) as mock_chat_openai, \
            patch('pygpt.llm.gpt.ConversationChain', return_value=Mock()) as mock_conversation_chain, \
            patch('pygpt.llm.gpt.ConversationBufferWindowMemory',
                  return_value=Mock()) as mock_conversation_buffer_window_memory:
        api = GptApi(api_key='test_key', model='test_model', prompt='test_prompt')
        assert api.OPENAI_API_KEY == 'test_key'
        assert api.OPENAI_MODEL == 'test_model'
        mock_chat_openai.assert_called_once_with(openai_api_key='test_key', model='test_model')
        mock_conversation_chain.assert_called_once()
        mock_conversation_buffer_window_memory.assert_called_once_with(k=4)
