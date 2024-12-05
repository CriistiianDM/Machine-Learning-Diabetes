base=https://github.com/docker/machine/releases/download/v0.16.2 &&
curl -L $base/docker-machine-$(uname -s)-$(uname -m) > /usr/local/bin/docker-machine &&
chmod +x /usr/local/bin/docker-machine