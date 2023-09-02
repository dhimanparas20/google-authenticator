# Google Authenticator

This is a user-friendly web application that allows users to register and log in using their email or Google account. The website also features an OTP (One-Time Password) authentication system for enhanced security. User data is stored in an SQLite database, and secure sessions are maintained for each user.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Registration**: Users can register on the website using their email or Google account.

- **Google Account Integration**: Users can opt to register and log in using their Google account, making the process more convenient.

- **OTP Authentication**: The website provides an OTP feature for added security during user registration and login.

- **Secure Sessions**: Each user's session is securely managed to ensure data privacy.

- **SQLite Database**: User information is stored in an SQLite database, which is easy to set up and maintain.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/dhimanparas20/google-authenticator.git
   cd google-authenticator
   pip install -r requirements.txt
   ```

## Configuration

1. Rename config-sample.ini to config.ini.

2. Fill out the required details in config.ini:
-  CLIENT_ID and CLIENT_SECRET: Google API credentials for Google account integration.
-  APP_SECRET_KEY and SECRET_KEY: Secret keys for securing your application.
-  DEBUG: Set to True for development mode.
-  GMAIL_ADDRESS and GMAIL_Name: Gmail credentials for sending OTP emails.
-  BREVO_API: API key for utilizing Brevo OTP API (if applicable).

## Usage

```bash
python3 app.py
http://localhost:5000/
```


