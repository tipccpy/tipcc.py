import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tipcc",
    version="1.0.1",
    author="UpByTheStars",
    author_email="upbythestars@gmail.com",
    description="Tools for interacting with the tip.cc api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UpByTheStars/tipcc.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
