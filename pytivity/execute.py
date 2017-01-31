import subprocess


def execute_in_subprocess(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode().split('\n')
    stderr = stderr.decode().split('\n')

    if stdout[-1] == '':
        del stdout[-1]
    if stderr[-1] == '':
        del stderr[-1]
    if stderr:
        print(stdout)
        print(stderr)
        raise RuntimeError
    return stdout
