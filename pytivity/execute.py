import subprocess


def execute_in_subprocess(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = output.stdout.decode().split('\n')
    if stdout[-1] == '':
        del stdout[-1]
    stderr = output.stderr.decode().split('\n')
    if stderr[-1] == '':
        del stderr[-1]
    if stderr:
        raise subprocess.CalledProcessError(returncode=output.returncode, cmd=command, output=output.stdout,
                                            stderr=output.stderr)
    return stdout
