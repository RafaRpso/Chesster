from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chesster",  
    version="0.4",
    author="Rafael Raposo",
    author_email="rafaelalvesraposo@hotmail.com",
    description="Chesster is a Chess.com wrapper for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RafaRpso/Chesster",
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "aiohttp",
        "requests",
        "urllib3",
        "asyncio"
    ],
)
