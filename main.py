import json
import random
from time import sleep

def randoutput():
    return json.dumps({
        'blink': random.getrandbits(1),
        'track': [
            random.randint(0, 1920),
            random.randint(0, 1080)
        ]
    })

# while 1:
for i in range(5):
    print(randoutput())
    sleep(0.2 +  random.uniform(-0.1, 0.1))
