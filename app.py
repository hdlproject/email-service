from flask import Flask
import fire
from src.google import GoogleAPIClient
from src.imap import IMAP


class App:
    def __init__(self):
        self.app = Flask(__name__)

    def run(self, port: int):
        self.app.run(host='0.0.0.0', port=port)


class CLI:
    def __init__(self, app: App, google_api: GoogleAPIClient, imap: IMAP):
        self.app = app
        self.google_api = google_api
        self.imap = imap

    def serve_http(self, port: int = 9090):
        self.app.run(port)

    def login_google(self):
        self.google_api.login()

    def read_latest_imap(self, username: str, password: str):
        self.imap.login(username, password)
        self.imap.read_latest()


if __name__ == '__main__':
    fire.Fire(
        CLI(
            App(),
            GoogleAPIClient(),
            IMAP(),
        )
    )
