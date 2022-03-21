from setuptools import find_packages
from setuptools import setup

setup(
    name='catkin_tools_document',
    packages=find_packages(),
    package_data={'catkin_tools_document': ['catkin_tools_document/external/*']},
    include_package_data=True,
    version='0.5.2',
    author='Mike Purvis',
    author_email='mike@uwmike.com',
    maintainer='Mike Purvis',
    maintainer_email='mike@uwmike.com',
    url='https://github.com/mikepurvis/catkin_tools_document',
    keywords=['catkin'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    description="Plugin for catkin_tools to enable building workspace documentation.",
    license='Apache 2.0',
    entry_points={
        'catkin_tools.commands.catkin.verbs': [
            'document = catkin_tools_document:description',
        ],
        'catkin_tools.spaces': [
            'docs = catkin_tools_document.spaces.docs:description',
        ],
    },
    python_version=">=3.8",
    install_requires=[
        'catkin_pkg',
        'catkin_tools>=0.8.3',
        'catkin_sphinx',
        'pydoctor>=20.12.0',
        'pyyaml',
        'sphinx>=4.3.0'
    ]
)
