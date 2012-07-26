from setuptools import find_packages, setup

setup(
    name = 'pylinkedin',
    version = '0.1.0',
    author = 'Kyle McCullough',
    author_email = 'kylemcc@gmail.com',
    url = 'https://github.com/kylemcc/pylinkedin',
    description = 'Python library for interacting with the LinkedIn REST API',
    packages = find_packages(),
    license = 'MIT License',
    install_requires = ['httplib2', 'simplejson']
)
