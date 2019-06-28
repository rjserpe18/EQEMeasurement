import subprocess
import sys

subprocess.call(['python','get_pip.py'])
subprocess.call([sys.executable, '-m', 'pip', 'install', '{0}=={1}'.format('numpy', '1.15.4')])
subprocess.call([sys.executable, '-m', 'pip', 'install', '{0}=={1}'.format('matplotlib', '3.1.0')])
subprocess.call([sys.executable, '-m', 'pip', 'install', '{0}=={1}'.format('seaborn', '0.9.0')])

