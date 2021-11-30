from shift_oelint_parser.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule


class VarSummaryLinebreaks(Rule):
    def __init__(self):
        super(VarSummaryLinebreaks, self).__init__(id='oelint.vars.summarylinebreaks',
                         severity='warning',
                         message='\'SUMMARY\' should not contain line breaks')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SUMMARY')
        for i in items:
            if i.Raw.strip().find('\\n') != -1:
                res += self.finding(i.Origin, i.InFileLine)
        return res
