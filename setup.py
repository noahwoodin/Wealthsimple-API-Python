import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Wealthsimple-API-Python",
    version="0.1.0",
    license="MIT",
    author="Noah Woodin",
    author_email="noahwoodin1@gmail.com",
    description="Python wrapper for the Wealthsimple Trade API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noahwoodin/Wealthsimple-API-Python",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["wealthsimple", "trade", "finance", "DRIP", "dividend", "buy", "stocks", "market", "api", "wrapper"],
    install_requires=["requests", "pyotp", "certifi"],
)
