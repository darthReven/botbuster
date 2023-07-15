# Specify the installation directory
install_dir="./model/chrome"

# Create the installation directory if it doesn't exist
mkdir -p $install_dir

# Download the Chrome installer
wget -P $install_dir https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome using dpkg
sudo dpkg -i $install_dir/google-chrome-stable_current_amd64.deb

# Install any missing dependencies
sudo apt-get -f install

# Clean up the downloaded installer
rm $install_dir/google-chrome-stable_current_amd64.deb
