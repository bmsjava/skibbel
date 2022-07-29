wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable
chrome_version=$(google-chrome --version|awk '{split($0,a," "); print a[3]}'|awk '{split($0,a,"."); print a[1]}')
html=$(curl -k --silent 'https://chromedriver.chromium.org/downloads')
version=$(grep -oPm1 "ChromeDriver "$chrome_version"\.[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+" <<< "$html" | awk '{split($0,a," "); print a[2]}' | head -1)
wget -N https://chromedriver.storage.googleapis.com/$chrome_version/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
cp /usr/local/share/chromedriver "data/chromedriver"
ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
rm chromedriver_linux64.zip
apt-get update
apt-get install -y libgconf-2-4