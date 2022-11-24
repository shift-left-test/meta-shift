from shift_oelint_adv.cls_rule import Rule
from shift_oelint_parser.cls_item import Variable
import re


class VarMultiInherit(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.multiinherit',
                         severity='warning',
                         message='\'{inherit}\' is included multiple times')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='inherit')
        keys = []
        for i in items:
            for y in [x.strip() for x in re.split(r'\s|,|\t|\x1b', i.VarValue) if x]:
                if y not in keys:
                    keys.append(y)
                else:
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace('{inherit}', y))
        return res
