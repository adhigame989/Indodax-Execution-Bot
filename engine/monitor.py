import threading
import time

from api.indodax import api


class MarketMonitor:

    def __init__(self):

        self.running = False

        self.interval = 2

        self.thread = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        self.thread.start()

        print("Market Monitor Started")

    def stop(self):

        self.running = False

        print("Market Monitor Stopped")

    def loop(self):

        while self.running:

            api.update()

            time.sleep(self.interval)


monitor = MarketMonitor()
