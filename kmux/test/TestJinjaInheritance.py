import unittest

import jinja2


class TestJinjaInheritance(unittest.TestCase):
    temploader = jinja2.FileSystemLoader(
        "/Users/julian/Repositories/julian.kmux/test/")
    env = jinja2.Environment(loader=temploader)
    template = env.get_template("childtemplate2")
    print(template.render({}))
    #template = env.get_template("childtemplate2")
    # print(template.render({}))
