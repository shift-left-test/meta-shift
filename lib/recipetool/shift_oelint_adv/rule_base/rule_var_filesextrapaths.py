import os

from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule


class VarBugtrackerIsUrl(Rule):
    def __init__(self):
        super(VarBugtrackerIsUrl, self).__init__(id="oelint.vars.fileextrapaths",
                                                 severity="warning",
                                                 message="'FILESEXTRAPATHS' shouldn't be used in a bb file")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in items:
            if i.VarName in ["FILESEXTRAPATHS_prepend", "FILESEXTRAPATHS_append", "FILESEXTRAPATHS"]:
                _, ext = os.path.splitext(i.Origin)
                if ext == ".bb":
                    res += self.finding(i.Origin, i.InFileLine)
        return res
