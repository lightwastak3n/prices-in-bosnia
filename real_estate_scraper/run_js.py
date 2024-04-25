import js2py
import re
import json


def run_js(js):
    target_script = js.replace("new Map([])", "[]")
    output = js2py.eval_js(target_script)
    output = str(output)
    if "Request failed with status code 404" in output:
        print("Listing deleted")
        return None
    output = (
        output.replace("None", "null")
        .replace("False", "false")
        .replace("True", "true")
        .replace("'", '"')
        .replace("\\", "")
    )
    pattern = r'"description":\s*".*?"\s*,\s*"updated_at"'
    output = re.sub(pattern, '"description": null, "updated_at"', output)
    try:
        output = json.loads(output)
    except json.decoder.JSONDecodeError:
        print("Json decode error probably some shit in the title")
        return None
    return output
