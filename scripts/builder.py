#!/usr/bin/python3
import argparse
import subprocess

def main(repo, image, tag, path):
    tagged_image = image+':'+tag
    universal_image = repo + '/' + tagged_image

    if exists_on_dockerhub(repo, image, tag):
        print(universal_image + ' already exists on DockerHub') 
        return
    
    build(image, path)
    
    # Tag image with repo name before pusshing to DockerHub
    image_latest = image + ':latest'
    universal_latest = repo + '/' + image_latest
    subprocess.run(['docker', 'tag', image, tagged_image])
    subprocess.run(['docker', 'tag', tagged_image, universal_image])
    subprocess.run(['docker', 'tag', image_latest, universal_latest])

    upload(universal_image, universal_latest)
    
    
def exists_on_dockerhub(repo, image, tag):
    cp = subprocess.run(['curl','--silent', '-f', '-lSL', 
        'https://index.docker.io/v1/repositories/' + repo + '/' + image +'/tags/'+ tag], capture_output=True)
    return cp.returncode == 0
   
def build(image, path):
    print('Building image...')
    build = subprocess.run(['docker', 'build', '-t', image, path])
    if build.returncode != 0:
        print("couldn't build image")
        return
    print('Image was built successfully')

def upload(universal_image, universal_latest):
    # login and upload image and tags
    login = subprocess.run(['docker', 'login'])
    print('Uploading image to DockerHub')
    subprocess.run(['docker', 'push', universal_image])
    subprocess.run(['docker', 'push', universal_latest])


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='To build the docker image and upload it to DockerHub')
    parser.add_argument('--repo', required=True, help='repository on DockerHun, usually username or organization')
    parser.add_argument('--image', required=True, help='image name')
    parser.add_argument('--tag', '-t', required=True, help='image tag')
    parser.add_argument('path', help='path to the Dockerfile')

    args = parser.parse_args()
    main(args.repo, args.image, args.tag, args.path)
    

