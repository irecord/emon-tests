Remember to install the pip3 packages as sudo

Create service your_service.service in /lib/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable your_service.service
sudo systemctl start your_service.service
