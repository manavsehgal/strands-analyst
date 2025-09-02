from setuptools import setup, find_packages

with open("analyst/requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="strands-analyst",
    version="0.1.0",
    description="A Strands AI agent package for analyzing websites and extracting metadata",
    author="Your Name",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sitemeta=analyst.cli.sitemeta:main",
            "news=analyst.cli.news:main",
            "article=analyst.cli.get_article:main",
            "htmlmd=analyst.cli.html_to_markdown:main",
            "analystchat=analyst.cli.chat:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)