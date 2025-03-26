import parsl
from parsl import Config, python_app, bash_app
from parsl.executors import GlobusComputeExecutor, HighThroughputExecutor
from globus_compute_sdk import Executor
from parsl.data_provider.files import File
import time
import glob
import os
from pathlib import Path


@bash_app(executors=['uncompress'])
def uncompress(inputs=[], outputs=[]):
    return f"""
        mkdir -p {outputs[0]}
        tar -xvf {inputs[0]} -C {outputs[0]}
    """


@bash_app(executors=['uncompress'])
def corrections(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/apps/corrections/main.py {inputs[0]} {inputs[1]} -o uncompressed
        """


@bash_app(executors=['uncompress'])
def crop(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/apps/crop/crop.py {inputs[0]} {inputs[1]} -6.501424 36.969786  -6.446088 36.996563 -o cropped
        """


@python_app(executors=['uncompress'])
def upload_to_ftp(inputs=[], outputs=[]):
    from ftplib import FTP
    import os

    ftp_host = "ftp"
    ftp_user = "parsltests"
    ftp_pass = "dodosaga1234."
    ftp_dest = ""

    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    # Get directory name from file
    # with open(inputs[0], "r") as f:
    #    directory = f.read().strip()

    uploaded_files = []

    for file in inputs:
        # upload_recursive(os.path.join(inputs[0], file), f"{ftp_dest}/{file}")
        remote_path = f"{ftp_dest}/{file}".replace("/cropped/", "")

        # print()
        try:
            ftp.mkd(os.path.dirname(remote_path))
        except Exception:
            pass  # Directory might already exist

        with open(file, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f)
            uploaded_files.append(remote_path)

    print(f"Uploading {inputs[0]} to {ftp_dest}")

    ftp.quit()
    return uploaded_files


@python_app(executors=['corrections'])
def download_from_ftp(inputs=[], outputs=[]):
    from ftplib import FTP
    import os

    ftp_host = "ftp"
    ftp_user = "parsltests"
    ftp_pass = "dodosaga1234."
    ftp_dest = ""

    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)
    
    for file in inputs:
        dir_name = os.path.dirname(file)
        os.makedirs(dir_name, exist_ok=True)

        with open(file, "wb") as f:
            ftp.retrbinary(f"RETR {file}", f.write)

    ftp.quit()

    outputs.append(dir_name)

    return outputs


@python_app(executors=['analysis'])
def download_from_ftp_analysis(inputs=[], outputs=[]):
    from ftplib import FTP
    import os

    ftp_host = "ftp"
    ftp_user = "parsltests"
    ftp_pass = "dodosaga1234."
    ftp_dest = ""

    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    for file in inputs:
        dir_name = os.path.dirname(file)
        os.makedirs(dir_name, exist_ok=True)

        with open(file, "wb") as f:
            ftp.retrbinary(f"RETR {file}", f.write)

    ftp.quit()

    outputs.append(dir_name)

    return outputs


@bash_app(executors=['corrections'])
def derivatives(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/apps/derivatives/main.py {inputs[0]} {inputs[1]} -o cropped
        """


@python_app(executors=['corrections'])
def push_derivatives_to_ftp(inputs=[], outputs=[]):
    from ftplib import FTP
    import os

    ftp_host = "ftp"
    ftp_user = "parsltests"
    ftp_pass = "dodosaga1234."
    ftp_dest = ""

    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    pushed = []

    # open file in_list
    for file in inputs:

        remote_path = f"{ftp_dest}/{file}".replace("/cropped/", "")

        try:
            ftp.mkd(os.path.dirname(remote_path))
        except Exception:
            pass  # Directory might already exist

        with open(file, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f)
            pushed.append(remote_path)

    # files = glob.glob(f'{}/Ind_*')

    print(f"Uploading {inputs} to {ftp_dest}")

    ftp.quit()

    return pushed


@bash_app(executors=['analysis'])
def summary(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/apps/summary/main.py {inputs[0]} -o summary
        """

BATCH_SIZE = 10  # Adjust batch size based on your API limit

config = Config(
    executors=[
        GlobusComputeExecutor(
            label="uncompress",
            executor=Executor(
                endpoint_id="760a4f08-8a07-479a-ac16-3ef7ddf34b3e"),
        ),
        GlobusComputeExecutor(
            label="corrections",
            executor=Executor(
                endpoint_id="c3f8d398-bbb8-4317-b168-7c7bb0089979")
        ),
        GlobusComputeExecutor(
            label="analysis",
            executor=Executor(
                endpoint_id="5873e13d-be88-4750-b4e3-243aa795ee0e")
        )
    ]
)
parsl.load(config)

datadir = "/DATA/"

input_data = []
output_uncompress = []
outputs_corrections = []
outputs_cropping = {}
inputs_ftps_1 = {}
outputs_derivatives = {}
inputs_summary = []
names = []

for filename in glob.iglob(datadir + '**/*.tar', recursive=True):
    input_data.append(File(filename))
    basename = os.path.splitext(os.path.basename(filename))[
        0].replace(".tar", "")
    # output_simulation.append(File("simulation/" + basename + ".csv"))
    output_uncompress.append(File("uncompressed/" + basename))

    # outputs_corrections[basename] = []
    inputs_ftps_1[basename] = []
    outputs_derivatives[basename] = []

    outputs_corrections.append(File("uncompressed/" + basename))
    outputs_cropping["uncompressed/" + basename] = File("cropped/" + basename)

    for i in range(1, 10):
        # outputs_corrections[basename].append(
        #    File(f"uncompressed/{basename}/{basename}_B{i}.TIF"))
        # outputs_corrections[basename].append(
        #    File(f"uncompressed/{basename}/{basename}_B{i}_corr.TIF"))

        inputs_ftps_1[basename].append(
            File(f"cropped/{basename}/{basename}_B{i}.TIF"))
    for i in ["ndvi_", "ndwi_b4", "ndwi_green_b7", "ndwi_red_b6", "ndwi_red_b7", "rgb_", "rgb_high_contrast_"]:
        outputs_derivatives[basename].append(
            File(f"cropped/{basename}/{i}{basename}.png"))
        # outputs_derivatives[basename].append(File(f"cropped/{basename}/{i}{basename}.tif"))

    outputs_derivatives[basename].append(
        File(f"cropped/{basename}/ndwi_red_b7{basename}.tif"))

    # outputs_derivatives[basename].append()"""

    names.append(basename)


Path("uncompressed").mkdir(parents=True, exist_ok=True)
Path("indexing").mkdir(parents=True, exist_ok=True)

uncompress_starttime = time.time()
results = []


# a = save_output("Hello World", output_file)
# print(a.result())

# Store all futures
uncompress_futures = {}
corrections_futures = {}
crop_futures = {}
upload_futures = {}
derivatives_futures = {}
push_derivatives_futures = {}
download_derivatives_futures = {}

# Step 1: Uncompress (parallel)}
tasks_uncompress = [uncompress(inputs=[file_obj], outputs=[output_file]) for file_obj, output_file in zip(input_data, output_uncompress)]

# Wait for all tasks to complete
results_uncompress = [task.result() for task in tasks_uncompress]

print("Uncompress termino")

# Step 2: Corrections (parallel)
tasks_corrections = [corrections(inputs=[input_file.outputs[0].filename, os.path.basename(input_file.outputs[0].filename)], outputs=[File(input_file.outputs[0].filename)]) for input_file in tasks_uncompress]

# wait for all tasks to complete
results_corrections = [task.result() for task in tasks_corrections]

print("Corrections termino")

# Step 3: Cropping (parallel)
tasks_cropping = [crop(inputs=[task.outputs[0].filename, os.path.basename(task.outputs[0].filename)], outputs=[outputs_cropping[task.outputs[0].filename]]) for task in tasks_corrections] 

# wait for all tasks to complete
results_cropping = [task.result() for task in tasks_cropping]

print("Cropping termino")

# Step 4: Upload to FTP (parallel)
tasks_upload = [upload_to_ftp(inputs=inputs_ftps_1[os.path.basename(task.outputs[0].filename)], outputs=[]) for task in tasks_cropping]

# wait for all tasks to complete
results_upload = [task.result() for task in tasks_upload]

print("Upload termino")

# Step 5: Download from FTP & Compute Derivatives (parallel)
tasks_download = [download_from_ftp(inputs=uploaded_files, outputs=[]) for uploaded_files in results_upload]

# wait for all tasks to complete
results_download = [task.result() for task in tasks_download]

print("Download termino")

# Step 6: Compute Derivatives (parallel)
tasks_derivatives = [derivatives(inputs=[out_files[0], out_files[0]], outputs=outputs_derivatives[out_files[0]]) for out_files in results_download]

# wait for all tasks to complete
results_derivatives = [task.result() for task in tasks_derivatives]

print("Derivatives termino")

# Step 7: Push derivatives to FTP (parallel)
tasks_push_derivatives = [push_derivatives_to_ftp(inputs=out_files.outputs, outputs=[]) for out_files in tasks_derivatives]

# wait for all tasks to complete
results_push_derivatives = [task.result() for task in tasks_push_derivatives]

print("Push derivatives termino")

# Step 8: Download derivatives from FTP (parallel)
tasks_download_derivatives = [download_from_ftp_analysis(inputs=push_der_result, outputs=[]) for push_der_result in results_push_derivatives]

# wait for all tasks to complete
results_download_derivatives = [task.result() for task in tasks_download_derivatives]

print("Download derivatives termino")

for fut in download_derivatives_futures.items():
    out_files = fut.result()
    inputs_summary = inputs_summary + out_files

#  Step 9: Summary
res_fut = summary(inputs=[".", inputs_summary])
print(res_fut.result())