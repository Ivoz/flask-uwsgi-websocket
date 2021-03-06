#!/usr/bin/env python
from setuptools import setup

setup(
    name='Flask-uWSGI-WebSocket',
    version='0.1.5',
    url='https://github.com/zeekay/flask-uwsgi-websocket',
    license='MIT',
    author='Zach Kelling',
    author_email='zk@monoid.io',
    description='High-performance WebSockets for your Flask apps powered by uWSGI.',
    long_description=open('README.rst').read(),
    py_modules=['flask_uwsgi_websocket'],
    platforms='any',
    install_requires=[
        'Flask',
        'uwsgi',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='uwsgi flask websockets'
)
