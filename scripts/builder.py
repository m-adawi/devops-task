#!/usr/bin/env python
import argparse
import subprocess

def start(repo, image, tag, path):
    if exists_on_dockerhub(repo, image, tag):
        print(universal_image + ' already exists on DockerHub') 
        return

    tagged_image = image+':'+tag
    universal_image = repo + '/' + tagged_image
    print('Building image...')
    build = subprocess.run(['docker', 'build', '-t', tagged_image, path])
    if build.returncode != 0:
        print("couldn't build image")
        return
    print('Image was built successfully')

    # Tag image with repo name before pusshing to DockerHub
    subprocess.run(['docker', 'tag', tagged_image, universal_image])

    login = subprocess.run(['docker', 'login'])
    print('Uploading image to DockerHub')
    subprocess.run(['docker', 'push', universal_image])
    



def exists_on_dockerhub(repo, image, tag):
    curl = cp = subprocess.run(['curl','--silent', '-f', '-lSL',
        'https://index.docker.io/v1/repositories/' + repo + '/' + image +'/tags/'+ tag], capture_output=True)
    return cp.returncode == 0
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='To build the docker image and upload it to DockerHub')
    parser.add_argument('--repo', help='repository on DockerHun, usually username or organization')
    parser.add_argument('--image', help='image name')
    parser.add_argument('--tag', '-t', help='image tag')
    parser.add_argument('path', help='path to the Dockerfile')

    args = parser.parse_args()
    start(args.repo, args.image, args.tag, args.path)
    

