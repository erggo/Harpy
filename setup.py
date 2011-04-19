# -*- coding: utf-8 -*-
DISTUTILS_DEBUG="True"

from glob import glob
from distutils.core import setup

config = {}

config['classifiers'] = [
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: GNU General Public License (GPL)',
			'Natural Language :: English',
			'Operating System :: OS Independent',
			'Programming Language :: C',
			'Programming Language :: Python',
			'Topic :: Scientific/Engineering',
			'Topic :: Software Development :: Code Generators',
			]


setup(name='harpia',
			version='1.0',
			packages=['harpia', 'harpia.amara','harpia.bpGUI'],
			scripts=['launcher/harpia'],
			description='Image Processing and Computer Vision Automatic Programming Tool',
			author='Clovis Peruchi Scotti',
			author_email='scotti@ieee.org',
			maintainer="Clovis Peruchi Scotti",
			maintainer_email="scotti@ieee.org",
			license="GNU GPL",
			url='http://s2i.das.ufsc.br/harpia/en/home.html',
			data_files=[ ('share/harpia/images', glob("app_data/images/*")), #this is fucked up! must put it in package_data!!
		 							 ('share/harpia/xml', glob("app_data/xml/*.xml")), #same thing
		 							 ('share/harpia/po/pt/LC_MESSAGES/', glob("app_data/po/pt/LC_MESSAGES/*")),
		 							 ('share/harpia/help', glob("app_data/help/*.help")),
		 							 ('share/harpia/glade', glob("app_data/glade/*.glade")),
		 							 ('share/harpia/examples', glob("app_data/examples/*.hrp")),
		 							 ('share/applications/', ["app_data/harpia.desktop"]),
									 ('share/icons/hicolor/scalable/apps', ['app_data/images/harpia.svg']),
									 ('share/pixmaps', ['app_data/images/harpia.svg']),
									 ('share/icons/hicolor/24x24/apps', ['app_data/images/harpia.png']),],
			**config
			)
