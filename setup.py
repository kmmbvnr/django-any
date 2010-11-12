from setuptools import setup, find_packages

setup(
    name='django-fsm',
    version='0.0.1',
    description='Unobtrusive test models  creation for django.',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    url='http://github.com/kmmbvnr/django-any',
    keywords = "django",
    packages=['django_any', 'django_any.contrib', 'django_any.tests'],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    platforms = ['any'],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)

