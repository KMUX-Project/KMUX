import unittest

import jinja2


class TestJinjaInclusion(unittest.TestCase):
    temploader = jinja2.FileSystemLoader("/Users/julian/Repositories/julian.kmux/test/")
    env = jinja2.Environment(loader=temploader)
    template = env.get_template("childtemplate3")
    print(template.render())
