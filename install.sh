wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable
sudo apt install curl
chrome_version=$(google-chrome --version|awk '{split($0,a," "); print a[3]}'|awk '{split($0,a,"."); print a[1]}')
html=$(curl -k --silent 'https://chromedriver.chromium.org/downloads')
version=$(grep -oPm1 "ChromeDriver "$chrome_version"\.[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+" <<< "$html" | awk '{split($0,a," "); print a[2]}' | head -1)
wget -N https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d data
chmod +x data/chromedriver
rm chromedriver_linux64.zip
apt-get update
apt-get install -y libgconf-2-4
sudo apt-get install language-pack-ru
sudo update-locale LANG=ru_RU.UTF-8
sudo reboot
