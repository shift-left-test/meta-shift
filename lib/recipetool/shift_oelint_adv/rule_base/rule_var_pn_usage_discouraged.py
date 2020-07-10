from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule


class VarPnUsageDiscouraged(Rule):
    def __init__(self):
        super(VarPnUsageDiscouraged, self).__init__(id="oelint.vars.pnusagediscouraged",
                                                    severity="warning",
                                                    message="Variable shouldn't contain ${PN} or ${BPN}")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        needles = ["SUMMARY", "HOMEPAGE", "BUGTRACKER", "DESCRIPTION"]
        for i in [x for x in items if x.VarName in needles]:
            if "${PN}" in i.VarValue or "${BPN}" in i.VarValue:
                res += self.finding(i.Origin, i.InFileLine)
        return res
