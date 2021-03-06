from shift_oelint_adv.cls_rule import Rule
from shift_oelint_parser.cls_item import Variable
from shift_oelint_parser.helper_files import get_scr_components


class VarBugtrackerIsUrl(Rule):
    def __init__(self):
        super(VarBugtrackerIsUrl, self).__init__(id='oelint.vars.bugtrackerisurl',
                         severity='warning',
                         message='\'BUGTRACKER\' should be an URL')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='BUGTRACKER')
        for i in items:
            val = i.VarValueStripped
            try:
                result = get_scr_components(val)
                if not result['scheme'] or not result['src']:
                    raise Exception()
            except Exception:
                res += self.finding(i.Origin, i.InFileLine)
        return res
