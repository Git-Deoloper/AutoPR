"""File handling utilities for reading and writing code"""

from pathlib import Path
from typing import Optional
import os


class FileHandler:
    """Handles reading and writing files"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)

    def read_file(self, file_path: str) -> str:
        """
        Read a file's contents

        Args:
            file_path: Path to the file (relative to base_path)

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file can't be read
        """
        full_path = self.base_path / file_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {str(e)}")

    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> bool:
        """
        Write content to a file

        Args:
            file_path: Path to the file (relative to base_path)
            content: Content to write
            create_dirs: Whether to create parent directories

        Returns:
            True if successful

        Raises:
            IOError: If file can't be written
        """
        full_path = self.base_path / file_path
        
        try:
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            raise IOError(f"Failed to write file {file_path}: {str(e)}")

    def append_file(self, file_path: str, content: str) -> bool:
        """
        Append content to a file

        Args:
            file_path: Path to the file (relative to base_path)
            content: Content to append

        Returns:
            True if successful
        """
        full_path = self.base_path / file_path
        
        try:
            with open(full_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            raise IOError(f"Failed to append to file {file_path}: {str(e)}")

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        full_path = self.base_path / file_path
        return full_path.exists() and full_path.is_file()

    def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        full_path = self.base_path / file_path
        
        try:
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception as e:
            raise IOError(f"Failed to delete file {file_path}: {str(e)}")

    def get_file_lines(self, file_path: str, start: int = 0, end: Optional[int] = None) -> list:
        """
        Get specific lines from a file

        Args:
            file_path: Path to the file
            start: Starting line number (0-indexed)
            end: Ending line number (inclusive, optional)

        Returns:
            List of lines
        """
        content = self.read_file(file_path)
        lines = content.split('\n')
        
        if end is None:
            return lines[start:]
        else:
            return lines[start:end+1]

    def replace_in_file(self, file_path: str, old_text: str, new_text: str) -> bool:
        """
        Replace text in a file

        Args:
            file_path: Path to the file
            old_text: Text to replace
            new_text: Replacement text

        Returns:
            True if replacement was made
        """
        content = self.read_file(file_path)
        
        if old_text not in content:
            return False
        
        new_content = content.replace(old_text, new_text)
        self.write_file(file_path, new_content)
        return True
