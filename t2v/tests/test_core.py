"""Tests for T2V core functionality."""

import pytest
from unittest.mock import patch, MagicMock

from t2v.core import T2VCore


class TestT2VCore:
    """Test cases for T2VCore class."""
    
    def test_init_default(self):
        """Test T2VCore initialization with default config."""
        core = T2VCore()
        assert core.config == {}
        assert core.initialized is False
    
    def test_init_with_config(self):
        """Test T2VCore initialization with custom config."""
        config = {"test_key": "test_value"}
        core = T2VCore(config)
        assert core.config == config
        assert core.initialized is False
    
    def test_initialize_success(self):
        """Test successful initialization."""
        core = T2VCore()
        result = core.initialize()
        assert result is True
        assert core.initialized is True
    
    @patch('t2v.core.logger')
    def test_initialize_failure(self, mock_logger):
        """Test initialization failure handling."""
        core = T2VCore()
        
        # Mock an exception during initialization
        with patch.object(core, 'initialized', side_effect=Exception("Test error")):
            result = core.initialize()
            assert result is False
    
    def test_process_not_initialized(self):
        """Test processing without initialization raises error."""
        core = T2VCore()
        with pytest.raises(RuntimeError, match="T2V Core not initialized"):
            core.process("test_data")
    
    def test_process_initialized(self):
        """Test processing with initialized core."""
        core = T2VCore()
        core.initialize()
        
        test_data = "test_input"
        result = core.process(test_data)
        assert result == test_data
    
    def test_get_status(self):
        """Test status retrieval."""
        config = {"test": "value"}
        core = T2VCore(config)
        
        status = core.get_status()
        assert status["initialized"] is False
        assert status["config"] == config
        assert status["version"] == "0.1.0"
        
        # Test after initialization
        core.initialize()
        status = core.get_status()
        assert status["initialized"] is True