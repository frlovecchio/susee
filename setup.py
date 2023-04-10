import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="susee",
    version='2.0',
    author="eng. Francesco Saverio Lovecchio, ph.D - Bari, Italy",
    author_email="frlovecchio@outlook.it",
    description="suSEE - Energy Monitoring System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/frlovecchio/susee',

    # packages=setuptools.find_packages(),
    packages=['susee'],

    install_requires=[
        'numpy',
        'pandas',
        'mysql-connector',
        'pymodbus=>3.2.2',  #requires python >3.8
        'pytz',
        'scipy',
        'statsmodels',
        'python-decouple',
        'setuptools',
        'wheel',
        'bokeh==1.3.4',  # 2.4.3',
    ],
   
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: System :: Monitoring',
        'Topic :: Scientific/Engineering :: Information Analysis',
        "Topic :: Software Development :: User Interfaces",
    ],

    package_dir={"": "src"},
    python_requires=">=3.8.0",
)
