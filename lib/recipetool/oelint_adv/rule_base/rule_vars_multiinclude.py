import re

from oelint_parser.cls_item import Include
from oelint_adv.cls_rule import Rule


class VarMultiInclude(Rule):
    def __init__(self):
        super(VarMultiInclude, self).__init__(id="oelint.var.multiinclude",
                         severity="warning",
                         message="'{INC}' is included multiple times")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Include.CLASSIFIER)
        keys = []
        for i in items:
            keys += [x.strip() for x in re.split(r"\s|,", i.IncName) if x]
        for key in list(set(keys)):
            _i = [x for x in items if x.IncName.find(key) != -1]
            if len(_i) > 1:
                res += self.finding(_i[-1].Origin, _i[-1].InFileLine,
                                    self.Msg.replace("{INC}", key))
        return res
