from distutils.core import setup

setup(
    name='str2emoji',
    version='1.0',
    author='catbaron',
    author_email='catbaron@live.cn',
    url='https://github.com/catbaron0/str2emoji',
    packages=['str2emoji'],
    install_requirs=['lac'],
    package_data={"": ["*.json"]}
)
