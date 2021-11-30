from shift_oelint_adv.cls_rule import Rule
from shift_oelint_parser.cls_item import Variable
from shift_oelint_parser.helper_files import get_scr_components


class VarPnBpnUsage(Rule):
    def __init__(self):
        super(VarPnBpnUsage, self).__init__(id='oelint.vars.pbpusage',
                         severity='error',
                         message='${BP} should be used instead of ${P}')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        needles = ['SRC_URI', 'S']
        for i in [x for x in items if x.VarName in needles]:
            for x in i.get_items():
                if i.VarName == 'SRC_URI':
                    _haystack = get_scr_components(x)['src']
                else:
                    _haystack = x
                if '${P}' in _haystack:
                    res += self.finding(i.Origin, i.InFileLine)
        return res
