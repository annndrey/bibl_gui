#from py2exe.build_exe import py2exe
from distutils.core import setup
#setup(name='bibliography', version='0.6', py_modules=['bibl'])#console=[{"script": "bibl.py"}] )
setup( windows=[{"script": "bibl.py"}],
       options={"py2exe":{"includes":["sip"], "bundle_files":1}},
       #data_files=matplotlib.get_py2exe_datafiles(),
       zipfile = None,
       )

