import re

from shift_oelint_adv.cls_rule import Rule
from shift_oelint_parser.cls_item import Variable
from shift_oelint_parser.helper_files import expand_term
from shift_oelint_parser.parser import INLINE_BLOCK


class VarImproperInherit(Rule):
    def __init__(self):
        super(VarImproperInherit, self).__init__(id='oelint.var.improperinherit',
                         severity='error',
                         message='\'{INH}\' is not a proper bbclass name')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='inherit')
        for i in items:
            for subi in [expand_term(stash, _file, x) for x in i.get_items() if x and x != INLINE_BLOCK]:
                if not re.match(r'^[A-Za-z0-9_.-]+$', subi):
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace('{INH}', subi))
        return res
