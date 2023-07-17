from locust import HttpUser, task, between
import random


sentences = [
    "That's just what I needed today",
    "I love coding in python",
    "Well what  a surprise",
    "James hates eating onions",
]


class AppUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def sentiment_page(self):
        mytext = random.choice(sentences)
        self.client.get("/sentiment/" + str(mytext))
