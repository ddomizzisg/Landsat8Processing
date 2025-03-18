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
                endpoint_id="760a4f08-8a07-479a-ac16-3ef7ddf34b3e")
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
outputs_corrections = {}
outputs_cropping = {}
outputs_derivatives = {}
inputs_summary = []
names = []

for filename in glob.iglob(datadir + '**/*.tar', recursive=True):
    input_data.append(File(filename))
    basename = os.path.splitext(os.path.basename(filename))[
        0].replace(".tar", "")
    # output_simulation.append(File("simulation/" + basename + ".csv"))
    output_uncompress.append(File("uncompressed/" + basename))

    outputs_corrections[basename] = []
    outputs_cropping[basename] = []
    outputs_derivatives[basename] = []
    for i in range(1, 10):
        outputs_corrections[basename].append(
            File(f"uncompressed/{basename}/{basename}_B{i}.TIF"))
        outputs_corrections[basename].append(
            File(f"uncompressed/{basename}/{basename}_B{i}_corr.TIF"))

        outputs_cropping[basename].append(
            File(f"cropped/{basename}/{basename}_B{i}.TIF"))
    for i in ["ndvi_", "ndwi_b4", "ndwi_green_b7", "ndwi_red_b6", "ndwi_red_b7", "rgb_", "rgb_high_contrast_"]:
        outputs_derivatives[basename].append(
            File(f"cropped/{basename}/{i}{basename}.png"))
        # outputs_derivatives[basename].append(File(f"cropped/{basename}/{i}{basename}.tif"))

    outputs_derivatives[basename].append(
        File(f"cropped/{basename}/ndwi_red_b7{basename}.tif"))

    # outputs_derivatives[basename].append()

    names.append(basename)


Path("uncompressed").mkdir(parents=True, exist_ok=True)
Path("indexing").mkdir(parents=True, exist_ok=True)

uncompress_starttime = time.time()
results = []


# a = save_output("Hello World", output_file)
# print(a.result())

print(input_data)
print(output_uncompress)
for i in range(len(input_data)):
    results.append(uncompress(
        inputs=[input_data[i]], outputs=[output_uncompress[i]]))

for r in results:
    out = r.result()
    if out == 0:
        outputs = r.outputs
        res_corrections = corrections(inputs=[outputs[0].filename, os.path.basename(
            outputs[0].filename)], outputs=outputs_corrections[os.path.basename(outputs[0].filename)])

        if res_corrections.result() == 0:
            real_outputs_corrections = res_corrections.outputs

            print(f"python3 /parsltests/apps/crop/crop.py {outputs[0].filename} {os.path.basename(
                outputs[0].filename)} -101.315881 19.870015 -100.827868 20.084173 -o cropped")

            res_crop = crop(inputs=[outputs[0].filename, os.path.basename(
                outputs[0].filename)], outputs=outputs_cropping[os.path.basename(outputs[0].filename)])

            if res_crop.result() == 0:
                real_outputs_crop = res_crop.outputs
                print(real_outputs_crop)
                res_ftp = upload_to_ftp(
                    inputs=real_outputs_crop, outputs=[])
                uploaded_files = res_ftp.result()
                downloaded_files = download_from_ftp(
                    inputs=uploaded_files, outputs=[]).result()

                print(
                    f"python3 /parsltests/apps/derivatives/main.py {downloaded_files[0]} {downloaded_files[0]} -o cropped")

                print(
                    outputs_derivatives[os.path.basename(outputs[0].filename)])

                derivatives_fut = derivatives(
                    inputs=[downloaded_files[0], downloaded_files[0]], outputs=outputs_derivatives[os.path.basename(outputs[0].filename)])
                derivatives_res = derivatives_fut.result()
                # print(derivatives_res)
                if derivatives_res == 0:
                    print(derivatives_fut.outputs)
                    push_der_fut = push_derivatives_to_ftp(
                        inputs=derivatives_fut.outputs, outputs=[])
                    push_der_result = push_der_fut.result()
                    print(push_der_result)
                    downloded_derivatives = download_from_ftp_analysis(
                        inputs=push_der_result, outputs=[])

                    res_down_der = downloded_derivatives.result()

                    print(res_down_der)

                    inputs_summary = inputs_summary + res_down_der


print(inputs_summary)
res_fut = summary(inputs=[".", inputs_summary])
print(res_fut.result())

# res_sum = summary(inputs=)

# for i in range(len(output_uncompress)):
#    print(output_uncompress[i])

# print("---Uncompress %s seconds ---" % (time.time() - uncompress_starttime))

# derivatives_starttime = time.time()
