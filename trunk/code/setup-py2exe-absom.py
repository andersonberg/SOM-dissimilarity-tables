from distutils.core import setup
import py2exe
import glob

setup( 
	name = 'absom',
	scripts=['gui_absom.py'],
	windows = [
				{
					'script': 'gui_absom.py'
				}
			  ],
			  
	options = {
				'py2exe':{
							'packages':'encodings',
							'includes':'cairo, pango, pangocairo, atk, gobject, gio',
						 },
			  },
)