from __future__ import print_function
import subprocess
import os


def gh_deploy(config):
    if not os.path.exists('.git'):
        print('Cannot deploy - this directory does not appear to be a git repository')
        return

    print("Copying '%s' to `gh-pages` branch and pushing to GitHub." % config['site_dir'])
    try:
        subprocess.check_call(['ghp-import', '-p', config['site_dir']])
    except:
        return

    # TODO: Also check for CNAME file
    url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
    url = url.decode('utf-8').strip()

    host = None
    path = None
    if 'github.com/' in url:
        host, path = url.split('github.com/', 1)
    elif 'github.com:' in url:
        host, path = url.split('github.com:', 1)

    if host is None:
        # This could be a GitHub Enterprise deployment.
        print('Your documentation should be available shortly.')
    else:
        username, repo = path.split('/', 1)
        if repo.endswith('.git'):
            repo = repo[:-len('.git')]
        url = 'http://%s.github.io/%s' % (username, repo)
        print('Your documentation should shortly be available at: ' + url)
