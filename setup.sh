#!/bin/bash

sudo apt update -y
sudo apt-get install pkg-config -y

# Step 1: Install MySQL
sudo apt-get install libmysqlclient-dev -y

sudo apt-get install python3-dev -y

sudo apt-get install libmariadb3 libmariadb-dev -y

echo "Installing MySQL..."
sudo apt update
sudo apt install -y mysql-server

# Step 2: Log in to MySQL as root and create database, user, and grant privileges
echo "Creating MySQL database and user..."
sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS HolidayQuest;
CREATE USER IF NOT EXISTS 'user1'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
GRANT ALL PRIVILEGES ON HolidayQuest.* TO 'user1'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

echo "MySQL database 'HolidayQuest' created and user 'user1' granted all privileges."

# Step 4: Install Python3 and pip if not already installed
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Step 7: Install the dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
	pip3 install --break-system-packages -r requirements.txt

else
	echo "requirements.txt not found. Please make sure the file exists."
fi

# Step 8: Verify MySQL service is running
echo "Starting MySQL service..."
sudo systemctl start mysql
sudo systemctl enable mysql

# Step 9: Applying django migrations

echo "Applying migrations..."
python3 HolidayQuest/manage.py migrate

# Final confirmation message
echo "MySQL installation complete. User 'user1' has been added with all privileges for the 'HolidayQuest' database."
echo "Virtual environment created and dependencies installed from requirements.txt (if it exists)."
