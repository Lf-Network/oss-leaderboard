import setuptools

# Function to read requirements from a file
def read_requirements(file_name):
    with open(file_name) as f:
        return f.read().splitlines()

# Read long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

# Load requirements
requirements = read_requirements('requirements.txt')
requirements_dev = read_requirements('requirements-dev.txt')

# Set up the package
setuptools.setup(
    name="oss-leaderboard",
    version="0.0.1",
    author="lftechnology",
    author_email="opensource@lftechnology.com",
    description="Open Source Leaderboard",
    url="https://github.com/leapfrogtechnology/oss-leaderboard",
    license="MIT",
    packages=setuptools.find_packages(
        where="scripts", exclude=["dist", "build", "*.egg-info"]
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Bug Reports": "https://github.com/leapfrogtechnology/oss-leaderboard/issues",
        "Source": "https://github.com/leapfrogtechnology/oss-leaderboard",
    },
)
