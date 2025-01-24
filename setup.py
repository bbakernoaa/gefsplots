from setuptools import setup, find_packages

setup(
    name="gefsplots",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "xarray",
        "matplotlib",
        "pandas",
        "fsspec",
        "s3fs",
        "monet",
        "cartopy",
    ],
    dependency_links=[
        "git+https://github.com/noaa-mdl/grib2io.git#egg=grib2io"
    ],
    entry_points={
        'console_scripts': [
            'plot_sfc_variable=gefsplots.plot_sfc_variable:main',
            'plot_entire_atmosphere_variable=gefsplots.plot_entire_atmosphere_variable:main',
            'plot_halfdegree_dta=gefsplots.plot_halfdegree_dta:main',
        ],
    },
    author="Barry Baker",
    author_email="your.email@example.com",
    description="Tools for plotting GEFS aerosol and chemistry forecasts",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YourUsername/gefsplots",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
