from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule
from shift_oelint_adv.const_vars import get_mandatory_vars


class VarMandatoryExists(Rule):
    def __init__(self):
        super(VarMandatoryExists, self).__init__(id="oelint.var.mandatoryvar",
                                                 severity="error",
                                                 message="<FOO>",
                                                 onappend=False,
                                                 appendix=get_mandatory_vars())

    def check(self, _file, stash):
        res = []
        for var in get_mandatory_vars():
            items = stash.GetItemsFor(
                filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=var)
            if not any(items):
                res += self.finding(_file, 0, "Variable '{}' should be set".format(var), appendix=var)
        return res
