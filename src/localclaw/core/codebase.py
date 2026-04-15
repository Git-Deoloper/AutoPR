"""Codebase reader module for analyzing and understanding code repositories"""

import os
import json
from pathlib import Path
from typing import Optional, Set, Dict, List
from dataclasses import dataclass, asdict
import mimetypes

@dataclass
class FileInfo:
    """Information about a code file"""
    path: str
    relative_path: str
    size: int
    content: str
    language: str
    is_binary: bool = False


class CodebaseReader:
    """Reads and analyzes entire codebases"""

    # Common file extensions to include
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp', '.cs',
        '.go', '.rb', '.php', '.swift', '.kt', '.rs', '.sh', '.bash',
        '.sql', '.html', '.css', '.scss', '.json', '.yaml', '.yml',
        '.xml', '.toml', '.md', '.rst', '.tex'
    }

    # Directories to exclude
    IGNORE_DIRS = {
        '__pycache__', '.git', '.venv', 'venv', 'env', 'node_modules',
        '.pytest_cache', 'build', 'dist', '.egg-info', '.tox',
        '.mypy_cache', '.coverage', '.idea', '.vscode', 'target',
        'vendor', '.next', 'out', 'build', 'dist', '.turbo',
        '.DS_Store', '.env', '.env.local', '.gradle', '.maven'
    }

    # Files to exclude
    IGNORE_FILES = {
        '.DS_Store', 'Thumbs.db', '.env', '.env.local', '.env.*.local',
        'package-lock.json', 'yarn.lock', 'poetry.lock', 'Gemfile.lock'
    }

    def __init__(self, root_path: str, max_file_size: int = 1024 * 1024):
        """
        Initialize the CodebaseReader

        Args:
            root_path: Root directory of the codebase
            max_file_size: Maximum file size to read (default 1MB)
        """
        self.root_path = Path(root_path)
        self.max_file_size = max_file_size
        self.files: List[FileInfo] = []
        self._file_count = 0
        self._skipped_files = 0

    def read_codebase(self) -> List[FileInfo]:
        """
        Read the entire codebase and return file information

        Returns:
            List of FileInfo objects
        """
        self.files = []
        self._file_count = 0
        self._skipped_files = 0

        if not self.root_path.exists():
            raise ValueError(f"Path does not exist: {self.root_path}")

        self._walk_directory(self.root_path)
        return self.files

    def _walk_directory(self, directory: Path) -> None:
        """Recursively walk through directory and read code files"""
        try:
            for item in directory.iterdir():
                # Skip symbolic links
                if item.is_symlink():
                    continue

                # Skip ignored directories
                if item.is_dir() and item.name in self.IGNORE_DIRS:
                    continue

                if item.is_dir():
                    self._walk_directory(item)
                else:
                    self._read_file(item)

        except (PermissionError, OSError):
            pass

    def _read_file(self, file_path: Path) -> None:
        """Read a single file if it matches criteria"""
        # Skip ignored files
        if file_path.name in self.IGNORE_FILES:
            self._skipped_files += 1
            return

        # Check file extension
        if file_path.suffix.lower() not in self.CODE_EXTENSIONS:
            self._skipped_files += 1
            return

        # Check file size
        try:
            if file_path.stat().st_size > self.max_file_size:
                self._skipped_files += 1
                return
        except (OSError, FileNotFoundError):
            self._skipped_files += 1
            return

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            relative_path = str(file_path.relative_to(self.root_path))
            language = self._detect_language(file_path)

            file_info = FileInfo(
                path=str(file_path),
                relative_path=relative_path,
                size=file_path.stat().st_size,
                content=content,
                language=language,
                is_binary=False
            )

            self.files.append(file_info)
            self._file_count += 1

        except (IOError, UnicodeDecodeError, OSError):
            self._skipped_files += 1

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.rs': 'rust',
            '.sh': 'bash',
            '.bash': 'bash',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.toml': 'toml',
            '.md': 'markdown',
            '.rst': 'rst',
            '.tex': 'latex',
        }
        return ext_to_lang.get(file_path.suffix.lower(), 'text')

    def get_file_content(self, relative_path: str) -> Optional[str]:
        """Get content of a specific file by relative path"""
        for file_info in self.files:
            if file_info.relative_path == relative_path:
                return file_info.content
        return None

    def get_stats(self) -> Dict:
        """Get statistics about the codebase"""
        total_lines = sum(len(f.content.split('\n')) for f in self.files)
        total_chars = sum(len(f.content) for f in self.files)

        by_language = {}
        for file_info in self.files:
            lang = file_info.language
            if lang not in by_language:
                by_language[lang] = {'files': 0, 'lines': 0}
            by_language[lang]['files'] += 1
            by_language[lang]['lines'] += len(file_info.content.split('\n'))

        return {
            'total_files': self._file_count,
            'skipped_files': self._skipped_files,
            'total_lines': total_lines,
            'total_chars': total_chars,
            'by_language': by_language,
        }

    def get_file_tree(self) -> Dict:
        """Get a tree structure of the codebase"""
        tree = {}
        for file_info in self.files:
            parts = file_info.relative_path.split(os.sep)
            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = {
                'size': file_info.size,
                'language': file_info.language,
                'lines': len(file_info.content.split('\n'))
            }
        return tree

    def search_files(self, pattern: str, search_content: bool = False) -> List[FileInfo]:
        """
        Search for files matching a pattern

        Args:
            pattern: File name pattern or content pattern
            search_content: If True, search in file contents

        Returns:
            List of matching FileInfo objects
        """
        results = []
        pattern_lower = pattern.lower()

        for file_info in self.files:
            if search_content:
                if pattern_lower in file_info.content.lower():
                    results.append(file_info)
            else:
                if pattern_lower in file_info.relative_path.lower():
                    results.append(file_info)

        return results

    def get_summary(self) -> str:
        """Get a human-readable summary of the codebase"""
        stats = self.get_stats()
        summary = f"""
📊 Codebase Summary
{'='*50}
Total Files: {stats['total_files']}
Total Lines: {stats['total_lines']:,}
Total Characters: {stats['total_chars']:,}

Languages:
"""
        for lang, data in sorted(stats['by_language'].items(), 
                                  key=lambda x: x[1]['lines'], reverse=True):
            summary += f"  {lang}: {data['files']} files, {data['lines']:,} lines\n"

        return summary
