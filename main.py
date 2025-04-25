
import os

from app import server


if __name__ == "__main__":
    server.run(host="localhost", port=5000, debug=True)

