from distutils.core import setup
setup(
  name = 'vkbottle',
  packages = ['vkbottle'],
  version = '0.1',
  license='MIT',
  description = 'New bot-creating repo with options control like in the flask!',
  author = 'Arseniy Timonik',
  author_email = 'timonik.bss@gmail.com',
  url = 'https://github.com/timoniq/vkbottle',
  download_url = 'https://github.com/timoniq/vkbottle/archive/v0.1.tar.gz',
  keywords = ['vk', 'vkontakte', 'vk-api', 'vk-bot', 'vkbottle', 'vk-bottle'],
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