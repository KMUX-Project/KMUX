import unittest

import jinja2

class TestJinjaCondition(unittest.TestCase):
    temploader = jinja2.FileSystemLoader("/Users/julian/Repositories/julian.kmux/test/")
    env = jinja2.Environment(loader=temploader)
    template = env.get_template("conditiontemplate")
    print(template.render({"link" : "tre", "links" :
        [ "/private/tmp/lnk0", "/private/tmp/lnk1"], "dest" : "/tmp/lnkdest" }))
