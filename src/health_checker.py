import pwd
import os
import sys
import platform

import json
import six

from flask import current_app


class HealthChecker:
    def __init__(self) -> None:
        self.functions = {
            "os": self.get_os,
            "config": self.get_config,
            "python": self.get_python,
            "process": self.get_process,
        }

    def dump_info(self):
        data = {}
        for (name, func) in six.iteritems(self.functions):
            data[name] = func()

        return json.dumps(data), 200, {"Content-Type": "application/json"}

    def get_os(self):
        return {"platform": sys.platform, "name": os.name, "uname": platform.uname()}

    def get_config(self):
        return self.safe_dump(current_app.config)

    def get_python(self):
        result = {
            "version": sys.version,
            "executable": sys.executable,
            "pythonpath": sys.path,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
                "releaselevel": sys.version_info.releaselevel,
                "serial": sys.version_info.serial,
            },
        }
        return result

    def get_process(self):
        return {
            "argv": sys.argv,
            "cwd": os.getcwd(),
            "user": pwd.getpwuid(os.geteuid()).pw_name,
            "pid": os.getpid(),
            "environ": self.safe_dump(os.environ),
        }

    def safe_dump(self, dictionary):
        result = {}
        for key in dictionary.keys():
            if "key" in key.lower() or "token" in key.lower() or "pass" in key.lower():
                # Try to avoid listing passwords and access tokens or keys in the output
                result[key] = "********"
            else:
                try:
                    json.dumps(dictionary[key])
                    result[key] = dictionary[key]
                except TypeError:
                    pass
        return result
