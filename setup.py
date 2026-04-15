#!/usr/bin/env python3
"""Setup configuration for LocalClaw"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="localclaw",
    version="0.1.0",
    author="LocalClaw Contributors",
    description="A fully local, open-source AI code agent with Ollama - no API keys required",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/localclaw",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/localclaw/issues",
        "Documentation": "https://github.com/yourusername/localclaw",
        "Source Code": "https://github.com/yourusername/localclaw",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.1",
        "pydantic>=2.0.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "aiofiles>=23.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "localclaw=localclaw.cli.main:cli",
        ],
    },
    include_package_data=True,
)
