"""Utility functions for T2V package."""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

logger = logging.getLogger(__name__)


class T2VUtils:
    """Utility class for T2V operations."""
    
    @staticmethod
    def load_config(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load configuration from a file.
        
        Args:
            file_path: Path to the configuration file (JSON or YAML)
            
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file format is unsupported
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    config = json.load(f)
                elif file_path.suffix.lower() in ['.yaml', '.yml']:
                    config = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {file_path.suffix}")
            
            logger.info(f"Configuration loaded from {file_path}")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration from {file_path}: {e}")
            raise
    
    @staticmethod
    def save_config(config: Dict[str, Any], file_path: Union[str, Path]) -> None:
        """Save configuration to a file.
        
        Args:
            config: Configuration dictionary to save
            file_path: Path where to save the configuration
        """
        file_path = Path(file_path)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    json.dump(config, f, indent=2)
                elif file_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(config, f, default_flow_style=False)
                else:
                    raise ValueError(f"Unsupported config file format: {file_path.suffix}")
            
            logger.info(f"Configuration saved to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration to {file_path}: {e}")
            raise
    
    @staticmethod
    def setup_logging(level: str = "INFO", log_file: Optional[Union[str, Path]] = None) -> None:
        """Set up logging configuration.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file
        """
        log_level = getattr(logging, level.upper())
        
        # Basic configuration
        handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        handlers.append(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            handlers.append(file_handler)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            handlers=handlers,
            force=True
        )
        
        logger.info(f"Logging configured with level: {level}")
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate the environment for T2V.
        
        Returns:
            Dictionary with validation results
        """
        results = {}
        
        # Check Python version
        import sys
        python_version = sys.version_info
        results["python_version_ok"] = python_version >= (3, 8)
        
        # Check required packages
        required_packages = {
            "numpy": "numpy",
            "pandas": "pandas", 
            "scikit-learn": "sklearn"
        }
        for package_name, import_name in required_packages.items():
            try:
                __import__(import_name)
                results[f"{package_name}_available"] = True
            except ImportError:
                results[f"{package_name}_available"] = False
        
        # Check write permissions
        try:
            test_file = Path("test_write_permission.tmp")
            test_file.touch()
            test_file.unlink()
            results["write_permission"] = True
        except Exception:
            results["write_permission"] = False
        
        return results