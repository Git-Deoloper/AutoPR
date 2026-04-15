"""Tests for LocalClaw"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from localclaw.core.codebase import CodebaseReader
from localclaw.core.file_handler import FileHandler


def test_codebase_reader():
    """Test codebase reader"""
    # Test with current directory
    reader = CodebaseReader(".")
    files = reader.read_codebase()
    
    # Should read at least some Python files
    assert len(files) > 0
    
    # Check stats
    stats = reader.get_stats()
    assert stats['total_files'] > 0
    assert stats['total_lines'] > 0


def test_file_handler():
    """Test file handler"""
    handler = FileHandler(".")
    
    # Test reading a Python file
    content = handler.read_file("README.md")
    assert len(content) > 0
    assert "LocalClaw" in content


def test_language_detection():
    """Test language detection"""
    reader = CodebaseReader(".")
    
    # Test various extensions
    assert reader._detect_language(Path("test.py")) == "python"
    assert reader._detect_language(Path("test.js")) == "javascript"
    assert reader._detect_language(Path("test.ts")) == "typescript"
    assert reader._detect_language(Path("test.java")) == "java"
