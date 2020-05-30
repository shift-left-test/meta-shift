from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule
from shift_oelint_adv.const_vars import get_suggested_vars


class VarSuggestedExists(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.suggestedvar",
                         severity="info",
                         message="<FOO>",
                         onappend=False,
                         appendix=get_suggested_vars())

    def check(self, _file, stash):
        res = []
        for var in get_suggested_vars():
            items = stash.GetItemsFor(
                filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=var)
            if not any(items):
                res += self.finding(_file, 0, "Variable '{}' should be set".format(var), appendix=var)
        return res
