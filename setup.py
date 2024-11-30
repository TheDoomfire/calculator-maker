from setuptools import setup, find_packages  # type: ignore

setup( 
    name='calc_help', 
    version='0.1',
    packages=find_packages(),
    description='A sample Python package', 
    entry_points={
        "console_scripts": [
            "ci_calc=main:main",  # 'my_project' will be the command
        ],
    },
) 