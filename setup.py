#!/usr/bin/env python3
"""
Setup script for Email Sender project
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="email-sender",
    version="1.0.0",
    author="Email Sender Project Contributors",
    author_email="your-email@example.com",
    description="A Python-based bulk email sender using Gmail SMTP with HTML templates and attachments",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/email_sender",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/email_sender/issues",
        "Documentation": "https://github.com/your-username/email_sender#readme",
        "Source Code": "https://github.com/your-username/email_sender",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
            "pre-commit>=2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-sender=email_sender:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.csv", "*.txt", "*.md"],
    },
    keywords="email, smtp, gmail, bulk, template, jinja2, html",
    packages=find_packages(),
    zip_safe=False,
)
