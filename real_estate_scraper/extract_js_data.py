import subprocess
import json


def get_js_data(func):
    declare_function = "let x = "
    extract_data = "\nconsole.log(JSON.stringify(x.state.search.results))"
    js = declare_function + func + extract_data
    proc = subprocess.Popen(
        ["node", "-e", js], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    output = json.loads(stdout.decode())
    return output
