from paver.easy import *
from paver.shell import sh 

rapyddir = path('rapyd')
htmldir = path('.')
jsdir = path('js')
cssdir = path('css')

@task
def compile():
    """
    Compile all Rapyd-stuff files where they lie
    """
    # Compile SASS files
    for f in cssdir.files('*.sass'):
        sh('rapydcss {!s}'.format(f))
    # Compile RapydScript files
    for f in jsdir.files('*.pyj'):
        jsfile = f.replace('.pyj', '.js')
        sh('rapydscript {!s} -o {!s}'.format(f, jsfile))
    # Compile RapydML files, basics first
    for f in htmldir.files('*.pyml'):
        if f.name in ['base.pyml', 'ui.pyml']:
            sh('rapydml {!s}'.format(f))
    for f in htmldir.files('*.pyml'):
        sh('rapydml {!s}'.format(f))

@task 
def pack():
    """
    Move Rapyd-stuff files into rapyddir
    """
    for f in htmldir.files('*.pyml') +\
      jsdir.files('*.pyj') +\
      cssdir.files('*.sass'):
        f.copy(rapyddir)
        f.remove()

@task
def unpack():
    """
    Move Rapyd-stuff files out of rapyddir
    """
    for f in rapyddir.files('*.pyml'):
        f.copy(htmldir)
        f.remove()
    for f in rapyddir.files('*.pyj'):
        f.copy(jsdir)
        f.remove()
    for f in rapyddir.files('*.sass'):
        f.copy(cssdir)
        f.remove()

@task
def push_github():
    compile()
    pack()
    sh('git add -A')
    sh('git commit -am "Clean up"')
    sh('git push github master')
    unpack()
    sh('git add -A')
    sh('git commit -am "Unclean up"')
