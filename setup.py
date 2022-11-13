import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="investment-rebalancer",
    version="1.0",
    author="Lukas Brauckmann",
    author_email="lukas.brauckmann@gmail.com",
    description="A simple tool helping you to calculate your portfolio rebalancing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Plebo13/investment-rebalancer",
    license="Apache License 2.0",
    packages=["main"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["prettytable", "prompt_toolkit", "sharepp"],
    entry_points={
        "console_scripts": [
            "investment = investment-rebalancer:main",
        ]
    },
)
