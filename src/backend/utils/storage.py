"""
JSON file storage utilities for the Astra Resilience Copilot.
Provides simple file-based storage for sensor readings and alerts.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Resolve project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "processed"


class JSONStorage:
    """Simple JSON file storage manager."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize storage manager.
        
        Args:
            data_dir: Directory path for storing JSON files (defaults to PROJECT_ROOT/data/processed)
        """
        self.data_dir = data_dir if data_dir else DEFAULT_DATA_DIR
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, filename: str) -> Path:
        """Get full path for a data file."""
        return self.data_dir / filename
    
    def read_json(self, filename: str) -> List[Dict[str, Any]]:
        """
        Read data from a JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            List of dictionaries from the JSON file, or empty list if file doesn't exist
        """
        file_path = self._get_file_path(filename)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {filename}: {e}")
            return []
    
    def write_json(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """
        Write data to a JSON file (overwrites existing content).
        
        Args:
            filename: Name of the JSON file
            data: List of dictionaries to write
            
        Returns:
            True if successful, False otherwise
        """
        file_path = self._get_file_path(filename)
        
        try:
            # Write to temporary file first for atomic operation
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            
            # Replace original file with temp file
            temp_path.replace(file_path)
            return True
        except IOError as e:
            print(f"Error writing {filename}: {e}")
            return False
    
    def append_json(self, filename: str, new_item: Dict[str, Any]) -> bool:
        """
        Append a new item to a JSON file.
        
        Args:
            filename: Name of the JSON file
            new_item: Dictionary to append
            
        Returns:
            True if successful, False otherwise
        """
        data = self.read_json(filename)
        data.append(new_item)
        return self.write_json(filename, data)
    
    def get_latest(self, filename: str) -> Dict[str, Any] | None:
        """
        Get the most recent item from a JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Most recent dictionary or None if file is empty
        """
        data = self.read_json(filename)
        return data[-1] if data else None
    
    def filter_by_status(self, filename: str, status: str) -> List[Dict[str, Any]]:
        """
        Filter items by status field.
        
        Args:
            filename: Name of the JSON file
            status: Status value to filter by
            
        Returns:
            List of items matching the status
        """
        data = self.read_json(filename)
        return [item for item in data if item.get('status') == status]


# Global storage instance
storage = JSONStorage()

# Made with Bob
