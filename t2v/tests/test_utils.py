"""Tests for T2V utility functions."""

import json
import yaml
import pytest
import tempfile
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

from t2v.utils import T2VUtils


class TestT2VUtils:
    """Test cases for T2VUtils class."""
    
    def test_load_config_json(self):
        """Test loading JSON configuration."""
        config_data = {"key1": "value1", "key2": 123}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = T2VUtils.load_config(config_path)
            assert loaded_config == config_data
        finally:
            Path(config_path).unlink()
    
    def test_load_config_yaml(self):
        """Test loading YAML configuration."""
        config_data = {"key1": "value1", "key2": 123}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = T2VUtils.load_config(config_path)
            assert loaded_config == config_data
        finally:
            Path(config_path).unlink()
    
    def test_load_config_file_not_found(self):
        """Test loading config from non-existent file."""
        with pytest.raises(FileNotFoundError):
            T2VUtils.load_config("/path/that/does/not/exist.json")
    
    def test_load_config_unsupported_format(self):
        """Test loading config with unsupported format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("some text")
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported config file format"):
                T2VUtils.load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_save_config_json(self):
        """Test saving JSON configuration."""
        config_data = {"key1": "value1", "key2": 123}
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            T2VUtils.save_config(config_data, config_path)
            
            # Verify the saved config
            with open(config_path, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == config_data
        finally:
            Path(config_path).unlink()
    
    def test_save_config_yaml(self):
        """Test saving YAML configuration."""
        config_data = {"key1": "value1", "key2": 123}
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
            config_path = f.name
        
        try:
            T2VUtils.save_config(config_data, config_path)
            
            # Verify the saved config
            with open(config_path, 'r') as f:
                saved_data = yaml.safe_load(f)
            assert saved_data == config_data
        finally:
            Path(config_path).unlink()
    
    def test_setup_logging_default(self):
        """Test setting up logging with defaults."""
        T2VUtils.setup_logging()
        
        # Verify logging level
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
    
    def test_setup_logging_custom_level(self):
        """Test setting up logging with custom level."""
        T2VUtils.setup_logging(level="DEBUG")
        
        # Verify logging level
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
    
    def test_setup_logging_with_file(self):
        """Test setting up logging with file output."""
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as f:
            log_path = f.name
        
        try:
            T2VUtils.setup_logging(level="INFO", log_file=log_path)
            
            # Verify log file is created
            assert Path(log_path).exists()
            
            # Test logging
            logger = logging.getLogger("test")
            logger.info("Test log message")
            
            # Verify log content
            with open(log_path, 'r') as f:
                log_content = f.read()
            assert "Test log message" in log_content
        finally:
            Path(log_path).unlink()
    
    @patch('t2v.utils.sys')
    def test_validate_environment_python_version(self, mock_sys):
        """Test environment validation for Python version."""
        # Mock Python 3.8+
        mock_sys.version_info = (3, 8, 0)
        results = T2VUtils.validate_environment()
        assert results["python_version_ok"] is True
        
        # Mock Python 3.7
        mock_sys.version_info = (3, 7, 0)
        results = T2VUtils.validate_environment()
        assert results["python_version_ok"] is False
    
    @patch('t2v.utils.__import__')
    def test_validate_environment_packages(self, mock_import):
        """Test environment validation for required packages."""
        # Mock successful import
        mock_import.return_value = MagicMock()
        results = T2VUtils.validate_environment()
        
        # Should have package availability checks
        assert "numpy_available" in results
        assert "pandas_available" in results
        assert "scikit-learn_available" in results
    
    def test_validate_environment_write_permission(self):
        """Test environment validation for write permissions."""
        results = T2VUtils.validate_environment()
        # Should be able to write in current directory
        assert "write_permission" in results
        assert isinstance(results["write_permission"], bool)