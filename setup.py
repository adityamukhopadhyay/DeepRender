from setuptools import setup, find_packages

setup(
    name="trellis-3d-generator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fal-serverless==0.6.41",
        "Pillow>=10.0.0",
        "python-dotenv>=1.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for converting images to 3D models using the Trellis API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/trellis-3d-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 