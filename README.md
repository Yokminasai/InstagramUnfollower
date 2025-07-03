# Instagram Auto Unfollow/Remove Follower

This Python script automates the process of unfollowing accounts you follow or removing followers from your Instagram account. It uses Selenium to interact with the Instagram web interface.

---

## Features

* **Automated Login:** Logs into your Instagram account securely.
* **Unfollow Following:** Automatically unfollows accounts you are currently following, with options for a maximum number of unfollows and a customizable delay.
* **Remove Followers:** Identifies and removes followers from your account.
* **2FA/OTP Handling:** Provides prompts for manual 2-Factor Authentication or OTP input if required.
* **Captcha/Challenge Handling:** Informs the user if a CAPTCHA or security challenge appears, requiring manual intervention.

---

## Prerequisites

Before running the script, ensure you have the following installed:

* **Python 3.x**
* **pip** (Python package installer)
* **Google Chrome browser**
* **ChromeDriver** compatible with your Chrome browser version. You can download it from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads). Make sure `chromedriver` is in your system's PATH or in the same directory as the script.

---

## Installation

1.  **Clone the repository (or download the script):**

    ```bash
    git clone [https://github.com/your-username/instagram-auto-unfollow.git](https://github.com/your-username/instagram-auto-unfollow.git)
    cd instagram-auto-unfollow
    ```

    (Replace `your-username` with the actual GitHub username if this were a real repository.)

2.  **Install Python dependencies:**

    ```bash
    pip install selenium
    ```

---

## Usage

1.  **Run the script:**

    ```bash
    python your_script_name.py
    ```

    (Replace `your_script_name.py` with the actual name of your Python file, e.g., `instagram_bot.py`)

2.  **Follow the on-screen prompts:**

    * **Select Mode:** Choose whether you want to "Unfollow Following" (1) or "Remove Follower" (2).
    * **Instagram Username:** Enter your Instagram username.
    * **Instagram Password:** Enter your Instagram password. The input will be hidden for security using `getpass`.
    * **Max Actions:** Specify the maximum number of accounts to process in one run (e.g., 10, 50).
    * **Delay:** Set the delay in seconds between each action (e.g., 3 seconds). This helps to avoid triggering Instagram's rate limits.

3.  **Monitor the browser:** The script will open a Chrome browser window. Keep an eye on it, especially if 2FA/OTP or a CAPTCHA/challenge pops up, as you may need to intervene manually.

---

## Important Notes

* **Rate Limits:** Instagram has strict rate limits. Performing too many actions too quickly can lead to your account being temporarily restricted or even banned. Use reasonable delays and limits to avoid this.
* **Account Security:** Be cautious when using automation tools. While this script aims to be safe, any form of automation carries a risk.
* **Browser Window:** The script will open a visible Chrome browser window. Do not close it manually until the script finishes or you are prompted to do so.
* **Error Handling:** The script includes basic error handling but might encounter unexpected Instagram UI changes. If the script stops working, inspect the error message and the Instagram web page to understand the issue. You might need to update the XPath selectors in the code.
* **Disclaimer:** This script is for educational purposes and personal use only. Use it responsibly and at your own risk. The developer is not responsible for any consequences arising from the misuse of this script.

---

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

MIT License

Copyright (c) 2025 Yokception

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
