upgrade solr

stop jetty apache nginx


https://gist.github.com/hvwaldow/67fecf80a9790b5c9153

apt-get remove --purge solr-common

apt-get remove --purge jetty8    
rm -rf /var/lib/jetty8
apt-get autoremove


apt-get update
apt-get install openjdk-8-jre-headless


apt install -t jessie-backports  openjdk-8-jre-headless ca-certificates-java
apt-get install unzip

wget http://www.eu.apache.org/dist/lucene/solr/5.5.5/solr-5.5.5.tgz
tar xzf solr-5.5.5.tgz solr-5.5.5/bin/install_solr_service.sh --strip-components=2
sudo bash ./install_solr_service.sh solr-5.5.5.tgz    #using default installation into /opt

service solr status   #Should show its up and running

