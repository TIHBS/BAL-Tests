from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'BAL_CALLBACK_URL': os.getenv("BAL_CALLBACK_URL"),
    'BAL_URL': os.getenv("BAL_URL"),
    'BAL_FLOW_PLUGIN': os.getenv("BAL_FLOW_PLUGIN")
}
