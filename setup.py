from setuptools import setup

setup(
    name='variance',
    packages=['variance'],
    include_package_data=True,
    install_requires=[
        'flask', 'flask-restful', 'flask-marshmallow', 'flask-sqlalchemy', 'pyjwt', 'marshmallow-sqlalchemy', 'python-dotenv'
    ],
)
