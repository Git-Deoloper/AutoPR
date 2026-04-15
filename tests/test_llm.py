"""Tests for LLM modules"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from localclaw.llm.prompts import PromptManager


def test_system_prompts():
    """Test system prompts"""
    # Test getting system prompts
    code_review_prompt = PromptManager.get_system_prompt("code_review")
    assert "code reviewer" in code_review_prompt.lower()
    
    bug_finder_prompt = PromptManager.get_system_prompt("bug_finder")
    assert "bug" in bug_finder_prompt.lower()
    
    # Test default
    default_prompt = PromptManager.get_system_prompt("nonexistent")
    assert len(default_prompt) > 0


def test_prompt_generation():
    """Test prompt generation"""
    code_sample = "def hello():\n    print('Hello')"
    
    # Test analysis prompt
    analyze_prompt = PromptManager.analyze_code_prompt(code_sample, "python")
    assert "python" in analyze_prompt.lower()
    assert code_sample in analyze_prompt
    
    # Test explanation prompt
    explain_prompt = PromptManager.explain_code_prompt(code_sample, "python")
    assert "explain" in explain_prompt.lower()
    
    # Test fix prompt
    fix_prompt = PromptManager.fix_code_prompt(code_sample, "infinite loop", "python")
    assert "infinite loop" in fix_prompt.lower()
