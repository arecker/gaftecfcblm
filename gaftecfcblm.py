#!/usr/bin/python3
import collections
import configparser
import logging
import pathlib
import random
import subprocess
import sys


MESSAGES = (
    'Late night hacking',
    'WIP, not sure about this',
    'save work',
    'eh, sure',
)


Repo = collections.namedtuple('Repo', [
    'name',
    'dir',
    'touch',
])


def load_repos(path='~/.gaftecfcblm.conf'):
    path = pathlib.Path(path).expanduser()
    parser = configparser.ConfigParser()
    parser.read(path)

    for section in parser.sections():
        kwargs, values = {}, parser[section]
        kwargs['name'] = section
        kwargs['dir'] = pathlib.Path(values['path']).expanduser()
        kwargs['touch'] = values['touch']
        yield Repo(**kwargs)


def update_repo(repo):
    # toggle end newline
    target = repo.dir / repo.touch
    with target.open('r') as f:
        content = f.read()
    if content.endswith('\n'):
        content = content[:-1]
    else:
        content += '\n'
    with target.open('w') as f:
        f.write(content)
    logging.info('%s: touched %s', repo.name, target)

    # git add
    cmd = ['git', 'add', repo.touch,]
    subprocess.run(cmd, cwd=repo.dir, check=True)
    logging.info('%s: git added %s', repo.name, repo.touch)

    # git commit
    msg = random.choice(MESSAGES)
    cmd = ['git', '-c', 'commit.gpgsign=false', 'commit', '-m', msg, '-n']
    subprocess.run(cmd, cwd=repo.dir, check=True)
    logging.info('%s: git committed "%s"', repo.name, msg)

    # git push
    cmd = ['git', 'push']
    subprocess.run(cmd, cwd=repo.dir, check=True)
    logging.info('%s: git pushed', repo.name)


def main():
    for repo in load_repos():
        update_repo(repo)


if __name__ == '__main__':
    logfile = pathlib.Path(__file__).parent / 'last.log'
    if logfile.is_file():
        logfile.unlink()
    logfile.touch()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', filename=str(logfile))
    main()
