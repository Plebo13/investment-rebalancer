import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="investment-rebalancer",
    version="0.9",
    author="Lukas Brauckmann",
    author_email="lukas.brauckmann@gmail.com",
    description="A simple tool helping you to calculate your portfolio rebalancing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Plebo13/investment-rebalancer",
    license="Apache License 2.0",
    packages=[
        "investment_rebalancer",
        "investment_rebalancer.model",
        "investment_rebalancer.model.asset",
        "investment_rebalancer.model.classification",
        "investment_rebalancer.controller",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["prettytable~=2.4.0", "prompt_toolkit==3.0.29", "sharepp==1.0.1"],
    entry_points={
        "console_scripts": [
            "investment-rebalancer = investment_rebalancer.main:main",
        ]
    },
)
