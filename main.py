
import os
from app import server
from populate_db import populate_if_needed



if __name__ == "__main__":
    populate_if_needed()
    server.run(host="0.0.0.0", port=5000)

