import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.debug("Debug info")
logging.info("General info")
logging.warning("Warning!")