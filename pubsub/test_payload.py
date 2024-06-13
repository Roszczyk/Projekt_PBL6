from collections import defaultdict
from pubsub_http import prepare_command_for_broker


payload = {
    "lights" : ["True"],
    "device_id" : ["2"],
    "timestamp" : ["489384.34823078"]
    }

print(prepare_command_for_broker(payload))