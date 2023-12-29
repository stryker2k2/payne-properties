# Payne Properties Payment Portal
A website for Payne Properties Payments

### APT Dependencies
- (apt) python3 
- (apt) python3.10-venv
- see ./support/install_requirements.sh

### PIP Dependencies
- see ./support/requirements.txt

### Setup
- apt install python3.10-venv
- python3 -m venv venv
- source venv/bin/activate
- ./support/install_requirements.sh
- *setup Database with 'support/notes/database.md'*
- make run

### Daily Use
- make run

### SSH into Production Server
- ping [production-server-ip]
- ssh root@[production-server-ip]

### Other Commands
- flask shell
- grip (view README.md locally)

### TODO
- Password Reset Request via Email
    - https://youtu.be/vutyTx7IaAI
- Flask Sessions
    - testdriven.io/blog/flask-sessions
- Disable SSH Password Login on Linode Server
- Fix error when trying to login on remote website
- Fix error with user image when you reload website