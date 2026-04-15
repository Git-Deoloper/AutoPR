"""Prompt templates and management for LocalClaw"""

from typing import Dict, Optional


class PromptManager:
    """Manages prompts for different tasks"""

    # System prompts for different modes
    SYSTEM_PROMPTS = {
        "code_review": """You are an expert code reviewer with deep knowledge of software engineering best practices.
Provide constructive, actionable feedback on code quality, security, performance, and maintainability.
Be specific and cite concrete examples from the code.""",

        "code_generation": """You are an expert programmer proficient in multiple programming languages.
When generating code:
1. Follow language conventions and idioms
2. Include helpful comments for complex logic
3. Prioritize readability and maintainability
4. Consider edge cases and error handling""",

        "bug_finder": """You are a meticulous code auditor specializing in finding bugs and security issues.
Analyze code carefully for:
1. Logic errors and edge cases
2. Resource leaks and performance issues
3. Security vulnerabilities
4. Type and null reference issues
Be specific about the line numbers and nature of each issue.""",

        "code_explainer": """You are an excellent educator and technical writer.
When explaining code, focus on:
1. What the code does at a high level
2. How it works step-by-step
3. Why it's written this way
4. Key concepts and patterns used
Use analogies and examples when helpful.""",

        "refactoring": """You are a senior software architect specializing in code improvement.
When suggesting refactoring:
1. Identify code smells and anti-patterns
2. Suggest specific improvements with examples
3. Explain the benefits of each change
4. Prioritize readability and maintainability over cleverness""",

        "general": """You are a helpful AI code assistant. 
Provide clear, accurate, and practical advice about programming topics.
When discussing code, provide examples and explain your reasoning.""",
    }

    @staticmethod
    def get_system_prompt(task: str) -> str:
        """Get system prompt for a task"""
        return PromptManager.SYSTEM_PROMPTS.get(task, PromptManager.SYSTEM_PROMPTS["general"])

    @staticmethod
    def analyze_code_prompt(code: str, language: str) -> str:
        """Generate prompt for code analysis"""
        return f"""Analyze this {language} code for quality, correctness, and improvements:

```{language}
{code}
```

Provide:
1. Overview of what this code does
2. Identified issues or concerns
3. Suggestions for improvement
4. Overall quality assessment"""

    @staticmethod
    def find_bugs_prompt(code: str, language: str, context: str = "") -> str:
        """Generate prompt for bug finding"""
        context_str = f"\nContext: {context}" if context else ""
        return f"""Find bugs and potential issues in this {language} code:{context_str}

```{language}
{code}
```

For each issue found, specify:
1. The problem and its severity (critical/major/minor)
2. Why it's a problem
3. How to fix it
4. Line numbers if applicable"""

    @staticmethod
    def explain_code_prompt(code: str, language: str) -> str:
        """Generate prompt for code explanation"""
        return f"""Explain what this {language} code does:

```{language}
{code}
```

Explain:
1. The overall purpose
2. Step-by-step how it works
3. Key variables and data structures used
4. Important concepts or patterns"""

    @staticmethod
    def refactor_code_prompt(code: str, language: str, goals: str = "") -> str:
        """Generate prompt for code refactoring"""
        goals_str = f"\nSpecific goals: {goals}" if goals else ""
        return f"""Suggest refactoring improvements for this {language} code:{goals_str}

```{language}
{code}
```

Provide:
1. Current issues (code smells, anti-patterns, etc.)
2. Suggested improvements with explanations
3. Refactored code
4. Why each change improves the code"""

    @staticmethod
    def generate_code_prompt(requirement: str, language: str, context: str = "") -> str:
        """Generate prompt for code generation"""
        context_str = f"\nContext/existing code:\n{context}" if context else ""
        return f"""Generate {language} code that: {requirement}{context_str}

Requirements:
1. Follow {language} best practices
2. Include meaningful variable and function names
3. Add comments for complex logic
4. Handle edge cases and errors appropriately
5. Be readable and maintainable

Provide only the code, wrapped in ```{language}``` markers."""

    @staticmethod
    def fix_code_prompt(code: str, issue: str, language: str) -> str:
        """Generate prompt for fixing code"""
        return f"""Fix this {language} code to resolve: {issue}

Current code:
```{language}
{code}
```

Provide:
1. Brief explanation of the fix
2. The corrected code (in ```{language}``` markers)
3. What changed and why"""

    @staticmethod
    def codebase_summary_prompt(codebase_info: str) -> str:
        """Generate prompt for codebase summary"""
        return f"""Provide a concise overview of this codebase:

{codebase_info}

Include:
1. Purpose and main functionality
2. Architecture/structure overview
3. Key technologies and patterns used
4. Potential areas of complexity or concern"""

    @staticmethod
    def implement_feature_prompt(feature: str, context: str, language: str) -> str:
        """Generate prompt for feature implementation"""
        return f"""Implement the following feature in {language}:

Feature: {feature}

Codebase context:
{context}

Provide:
1. Implementation plan
2. Code changes needed
3. New files/modules to create
4. Integration points with existing code

Format code in ```{language}``` markers."""
