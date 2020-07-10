from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule


class VarQuoted(Rule):
    def __init__(self):
        super(VarQuoted, self).__init__(id="oelint.vars.valuequoted",
                                        severity="error",
                                        message="Variable value should be quoted")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            # Don't use VarValueStripped here as we explicitly want the quotes
            # at the beginning and the end of the value
            val = i.VarValue.strip()
            if not val.startswith("\"") or not val.endswith("\""):
                res += self.finding(i.Origin, i.InFileLine)
        return res
