from pathlib import Path

from paver.easy import task, path, cmdopts
from paver.shell import sh


rapyddir = Path('rapyd')
htmldir = Path('.')
jsdir = Path('js')
cssdir = Path('css')

@task
def compile():
    """
    Compile all Rapyd-stuff files where they lie
    """
    # Compile SASS files
    for f in cssdir.glob('*.sass'):
        sh('rapydcss {!s}'.format(f))

    # Compile RapydScript files
    for f in jsdir.glob('*.pyj'):
        jsfile = f.parent/(f.stem + '.js')
        sh('rapydscript {!s} -o {!s} -p'.format(f, jsfile))

    # Compile RapydML files, basics first
    for f in htmldir.glob('*.pyml'):
        if f.name in ['base.pyml', 'ui.pyml']:
            sh('rapydml {!s}'.format(f))

    for f in htmldir.glob('*.pyml'):
        sh('rapydml {!s}'.format(f))

@task
def pack():
    """
    Move Rapyd-stuff files into rapyddir
    """
    if not rapyddir.exists():
        rapyddir.mkdir()
    for f in list(htmldir.glob('*.pyml')) + list(jsdir.glob('*.pyj')) +\
      list(cssdir.glob('*.sass')):
        f.rename(rapyddir/f.name)
    for f in list(rapyddir.glob('*.html')) + list(rapyddir.glob('*.css')) +\
      list(rapyddir.glob('*.js')):
        f.unlink()

@task
def unpack():
    """
    Move Rapyd-stuff files out of rapyddir
    """
    if not rapyddir.exists():
        return

    for f in rapyddir.iterdir():
        if f.suffix == '.pyml':
            f.rename(htmldir/f.name)
        elif f.suffix == '.pyj':
            f.rename(jsdir/f.name)
        elif f.suffix == '.sass':
            f.rename(cssdir/f.name)
        else:
            f.unlink()
    rapyddir.rmdir()

# @task
# @cmdopts([
#     ('server=', 's', 'Server to push to'),
#     ('local_branch=', 'l', 'Local Git branch to push'),
#     ('remote_branch=', 'r', 'Remote Git branch to push to'),
# ])
# def push(options):
#     server = options.push.server
#     local_branch = options.push.local_branch
#     try:
#         remote_branch = options.push.remote_branch
#     except AttributeError:
#         remote_branch = local_branch

#     pack()
#     status = sh('git status', capture=True)
#     if not 'nothing to commit' in status:
#         sh('git add -A')
#         sh('git commit -am "Packed"')
#     push_command = 'git push {!s} {!s}:{!s} --follow-tags'.format(
#       server, local_branch, remote_branch)
#     if server == 'webfaction':
#         push_command += ' --force'
#     sh(push_command)
#     unpack()
#     sh('git add -A')
#     sh('git commit -am "Unpacked"')
