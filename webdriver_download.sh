wget -N https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv -f chromedriver /usr/local/share/chromedriver
ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
rm chromedriver_linux64.zip
apt-get update
apt-get install -y libgconf-2-4