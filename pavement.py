from paver.easy import task, path, cmdopts
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
@cmdopts([
    ('server=', 's', 'Server to push to'),
    ('local_branch=', 'l', 'Local Git branch to push'),
    ('remote_branch=', 'r', 'Remote Git branch to push to'),
])
def push(options):
    server = options.push.server
    local_branch = options.push.local_branch
    try:
        remote_branch = options.push.remote_branch
    except AttributeError:
        remote_branch = local_branch

    compile()
    pack()
    sh('git add -A')
    sh('git commit -am "Clean up"')
    sh('git push {!s} {!s}:{!s} --follow-tags'.format(
      server, local_branch, remote_branch))
    # unpack()
    # sh('git add -A')
    # sh('git commit -am "Unclean up"')
