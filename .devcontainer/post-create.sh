# Install `oc` CLI tool
arch="$(arch)"
case "$arch" in 
    x86_64) export TARGET='' ;; 
    aarch64) export TARGET='arm64-' ;; 
esac
wget -O /tmp/oc.tgz "https://github.com/okd-project/okd/releases/download/4.15.0-0.okd-2024-03-10-010116/openshift-client-linux-${TARGET}4.15.0-0.okd-2024-03-10-010116.tar.gz"
pushd /tmp
tar -xvzf oc.tgz
sudo mv oc /usr/bin/oc
rm kubectl oc.tgz README.md
popd

# Install Python Packages
pip install --upgrade pip
pip install -r requirements.txt