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

# Step 1: Uncompress (parallel)
for i, file_obj in enumerate(input_data):  # Use integer index
    file_key = os.path.basename(file_obj.filename)  # Use filename as a key
    output_file = output_uncompress[i]  # Use list index for outputs
    print(file_obj)
    uncompress_futures[file_key] = uncompress(
        inputs=[file_obj], outputs=[output_file])

# Step 2: Corrections (parallel)
for file_key, fut in uncompress_futures.items():
    fut.result()  # Wait for completion (only ensures success)
    print(f"Uncompress {file_key} completed")
    out_files = fut.outputs  # Get actual output files
    print(out_files)
    corrections_futures[file_key] = corrections(
        inputs=[out_files[0].filename,
                os.path.basename(out_files[0].filename)],
        outputs=[File(out_files[0].filename)]
    )

# Step 3: Cropping (parallel)
for file_key, fut in corrections_futures.items():
    fut.result()
    out_files = fut.outputs
    image = os.path.basename(os.path.dirname(out_files[0].filename))
    crop_futures[file_key] = crop(
        inputs=[out_files[0].filename,
                os.path.basename(out_files[0].filename)],
        outputs=[outputs_cropping[out_files[0].filename]]
    )

# Step 4: Upload to FTP (parallel)
for file_key, fut in crop_futures.items():
    fut.result()
    out_files = fut.outputs
    upload_futures[file_key] = upload_to_ftp(inputs=inputs_ftps_1[os.path.basename(out_files[0].filename)], outputs=[])

# # Step 5: Download from FTP & Compute Derivatives (parallel)
for file_key, fut in upload_futures.items():
    uploaded_files = fut.result()  # Use .outputs instead of .result()
    download_derivatives_futures[file_key] = download_from_ftp(inputs=uploaded_files, outputs=[])
    
for file_key, fut in download_derivatives_futures.items():
    out_files = fut.result() 
        
    derivatives_futures[file_key] = derivatives(
        inputs=[out_files[0], out_files[0]],
        outputs=outputs_derivatives[out_files[0]]
    )

# # Step 6: Push derivatives to FTP (parallel)
for file_key, fut in derivatives_futures.items():
    fut.result()
    out_files = fut.outputs
    push_derivatives_futures[file_key] = push_derivatives_to_ftp(inputs=out_files, outputs=[])

# # Step 7: Download derivatives from FTP (parallel)
for file_key, fut in push_derivatives_futures.items():
    out_files = fut.result()
    download_derivatives_futures[file_key] = download_from_ftp_analysis(inputs=out_files, outputs=[])

# # Step 8: Collect Results
for file_key, fut in download_derivatives_futures.items():
    out_files = fut.result()
    inputs_summary = inputs_summary + out_files

# # Step 9: Summary
res_fut = summary(inputs=[".", inputs_summary])
print(res_fut.result())