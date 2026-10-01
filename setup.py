"""
Dating App Conversation Research Framework

A research tool for studying conversation patterns in dating applications
using synthetic simulation and ethical analysis.

IMPORTANT: This tool uses SYNTHETIC DATA ONLY. It is designed for academic
research on conversation patterns. It does NOT interact with real Tinder
or other dating platforms. See ETHICS_FRAMEWORK.md for details.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tinder-conversation-research",
    version="0.1.0",
    author="Research Team",
    author_email="research@example.com",
    description="Research framework for analyzing conversation patterns in dating apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/tinder-research",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Sociology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.3.0",
        "scipy>=1.10.0",
        "networkx>=3.1",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "faker>=18.0.0",
        "nltk>=3.8.0",
        "spacy>=3.6.0",
        "fairlearn>=0.10.0",
        "click>=8.1.0",
        "pyyaml>=6.0",
        "loguru>=0.7.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tinder-research=tinder_research.cli:main",
        ],
    },
)
