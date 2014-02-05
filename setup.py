from setuptools import find_packages, setup

setup(
    name = 'pylinkedin',
    version = '0.2.0',
    author = 'Kyle McCullough',
    author_email = 'kylemcc@gmail.com',
    url = 'https://github.com/kylemcc/pylinkedin',
    description = 'Python library for interacting with the LinkedIn REST API',
    packages = find_packages(),
    license = 'MIT License',
    install_requires = [
        "requests >= 1.2.3",
        "requests_oauthlib >= 0.3.3",
    ]
)
