from bs4 import BeautifulSoup
import urllib2
import os
import subprocess

def get_repos(gcode_projectname, out_dir):
    gcode_url = 'https://code.google.com/p/%s/source/checkout' % gcode_projectname

    # get the file.
    page_html = urllib2.urlopen(gcode_url).read()
    page_soup = BeautifulSoup(page_html)

    options = page_soup.find('select').find_all('option')

    repo_url = "https://code.google.com/p/%s" % gcode_projectname
    repo_strings = ["%s.%s" % (repo_url, option.string) for option in options]

    for repo in repo_strings:
        repo_basename = os.path.basename(repo)

        if not os.path.exists(repo_basename):
            subprocess.call('hg clone --noupdate %s' % repo, shell=True)
        else:
            subprocess.call('hg pull -R %s' % repo_basename, shell=True)

        subprocess.call('hg bundle --all -R %s %s.hg' % (
            repo_basename, os.path.join(out_dir, repo_basename)), shell=True)


def mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def scp(dirname):
    subprocess.call('scp -r %s jdouglass@ncp-geome:~/backblaze_mount' % dirname, shell=True)

if __name__ == '__main__':
    archive_dir = 'archives'
    mkdir(archive_dir)

    for project in ['invest-natcap', 'natcap-dev']:
        get_repos(project, archive_dir)

    scp(archive_dir)
