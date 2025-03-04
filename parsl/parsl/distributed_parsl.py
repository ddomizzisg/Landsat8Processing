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
        tar -xzvf {inputs[0]} -C {outputs[0]}
    """
    
@bash_app(executors=['uncompress']):
def corrections(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/corrections/main.py {inputs[0]} {inputs[1]} -o {outputs[0]}
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

    for file in os.listdir(inputs[0]):
        # upload_recursive(os.path.join(inputs[0], file), f"{ftp_dest}/{file}")
        local_path = os.path.join(inputs[0], file)
        remote_path = f"{ftp_dest}/{local_path}".replace("/uncompressed/", "")

        # print()
        try:
            ftp.mkd(os.path.dirname(remote_path))
        except Exception:
            pass  # Directory might already exist

        with open(local_path, "rb") as f:
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

@bash_app(executors=['corrections'])
def derivatives(inputs=[], outputs=[]):
    return f"""
        python3 /parsltests/apps/derivatives/LS.py {inputs[0]} {inputs[1]}
        ls -l {inputs[0]} | tee {outputs[0]}
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
    
    in_list = inputs[0]
    
    pushed = []
    
    # open file in_list
    with open(in_list, "r") as f:
        files = f.readlines()
        for file_ln in files:
            tokens = file_ln.split()
            if tokens[-1].startswith("Ind"):
                file = f"{inputs[1]}/{tokens[-1]}"
            
                with open(file, "rb") as f:
                    ftp.storbinary(f"STOR {file}", f)
                    pushed.append(file)

    #files = glob.glob(f'{}/Ind_*')
    return pushed



config = Config(
    executors=[
        GlobusComputeExecutor(
            label="uncompress",
            executor=Executor(
                endpoint_id="dcb31349-1c4b-4bdd-8e18-cbba50c07749")
        ),
        GlobusComputeExecutor(
            label="corrections",
            executor=Executor(
                endpoint_id="6e801abd-bb58-4bde-9ca6-f286fec26ba7")
        ),
        GlobusComputeExecutor(
            label="crop_derivatives",
            executor=Executor(
                endpoint_id="633ea728-f84f-40d3-81a5-9ca62d35c11f")
        )
    ]
)
parsl.load(config)

datadir = "/DATA/"

input_data = []
output_uncompress = []
input_indexing = []
output_indexing = []
names = []

for filename in glob.iglob(datadir + '**/*.tar.gz', recursive=True):
    input_data.append(File(filename))
    basename = os.path.splitext(os.path.basename(filename))[
        0].replace(".tar", "")
    # output_simulation.append(File("simulation/" + basename + ".csv"))
    output_uncompress.append(File("uncompressed/" + basename))
    input_indexing.append(
        File("uncompressed/" + basename + "/" + basename + "_MTL.txt"))
    output_indexing.append(File("indexing/" + basename + ".json"))
    names.append(basename)


Path("uncompressed").mkdir(parents=True, exist_ok=True)
Path("indexing").mkdir(parents=True, exist_ok=True)

uncompress_starttime = time.time()
results = []


# a = save_output("Hello World", output_file)
# print(a.result())

for i in range(len(input_data)):
    results.append(uncompress(
        inputs=[input_data[i]], outputs=[output_uncompress[i]]))

for r in results:
    out = r.result()
    print(out)
    if out == 0:
        outputs = r.outputs
        print(outputs)
        # res_ftp = upload_to_ftp(inputs=[outputs[0]], outputs=[])
        # uploaded_files = res_ftp.result()
        # downloaded_files = download_from_ftp(
        #     inputs=uploaded_files, outputs=[]).result()
        # derivatives_fut = derivatives(
        #     inputs=[downloaded_files[0], downloaded_files[0]], outputs=[File(f"{downloaded_files[0]}.txt")])
        # derivatives_res = derivatives_fut.result()
        # if derivatives_res == 0:
        #     push_der_fut = push_derivatives_to_ftp(inputs=[derivatives_fut.outputs[0], downloaded_files[0]], outputs=[])
        #     print(push_der_fut.result())
        #print(push_derivatives_to_ftp(inputs=[], outputs=[]).result())


# for i in range(len(output_uncompress)):
#    print(output_uncompress[i])

# print("---Uncompress %s seconds ---" % (time.time() - uncompress_starttime))

# derivatives_starttime = time.time()
