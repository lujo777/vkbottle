from .vkbottle import __version__
import setuptools

from distutils.core import setup
setup(
  name='vkbottle',
  packages=['vkbottle'],
  version=__version__,
  license='MIT',
  description='New bot-creating repo with options control like in the flask!',
  author='Arseniy Timonik',
  author_email='timonik.bss@gmail.com',
  url='https://github.com/timoniq/vkbottle',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  download_url='https://github.com/timoniq/vkbottle/archive/v0.11.tar.gz',
  keywords=['vk', 'vkontakte', 'vk-api', 'vk-bot', 'vkbottle', 'vk-bottle'],
  install_requires=[
    'requests',
    'six'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)