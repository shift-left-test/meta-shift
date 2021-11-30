from shift_oelint_parser.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule


class VarNativeSDKFilename(Rule):
    def __init__(self):
        super(VarNativeSDKFilename, self).__init__(id='oelint.var.nativesdkfilename',
                         severity='warning',
                         message='nativesdk-recipe-files should include \'nativesdk-\' in file name')

    def check(self, _file, stash):
        res = []
        items = [x for x in
                 stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='inherit')
                 if x.VarValueStripped == 'nativesdk']
        if any(items):
            if _file.find('nativesdk-') == -1:
                res += self.finding(_file, 0)
        return res
