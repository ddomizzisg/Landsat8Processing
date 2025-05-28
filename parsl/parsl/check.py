from globus_compute_sdk import Client
from globus_compute_sdk import Executor

ep_uuid = "760a4f08-8a07-479a-ac16-3ef7ddf34b3e"

with Executor(ep_uuid) as gcx:
    print(gcx.get_worker_hardware_details())
    
c = Client()
c.get_endpoint_status(ep_uuid)