import json
import os

import numpy as np

# from .core import utils


function_root = os.environ.get("function_root")

# Now  pre-load the model, e.g.
# from .core import model


def handle(req: bytes) -> str:
    """handle a request to the function
    Args:
        req (bytes): request body
    """
    #inp = json.loads(req)

    return json.dumps({
        "echo": req,
        "random": np.random.random_sample()
    })
