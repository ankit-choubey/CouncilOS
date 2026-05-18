from setuptools import setup, find_packages

setup(
    name="CouncilOS",
    version="0.1.0",
    description="Multi-agent orchestration and coordination framework",
    author="Ankit Choubey",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "google-generativeai>=0.3.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
        "rich>=13.7.0",
        "chromadb>=0.4.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
    ],
    python_requires=">=3.10",
)
