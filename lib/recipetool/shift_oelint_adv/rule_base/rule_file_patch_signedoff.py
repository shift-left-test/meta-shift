import os

from shift_oelint_adv.cls_item import Variable
from shift_oelint_adv.cls_rule import Rule
from shift_oelint_adv.helper_files import get_files


class FilePatchIsSignedOff(Rule):
    def __init__(self):
        super(FilePatchIsSignedOff, self).__init__(id="oelint.file.patchsignedoff",
                                                   severity="warning",
                                                   message="Patch '{FILE}' should contain a Signed-Off entry")

    def check(self, _file, stash):
        res = []
        items = get_files(stash, _file, "*.patch")
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in items:
            with open(i) as _input:
                try:
                    content = _input.readlines()
                    if not any([x for x in content if x.startswith("Signed-off-by: ")]):
                        # Find matching SRC_URI assignment
                        _assign = [x for x in _items if x.VarValue.find(
                            os.path.basename(i)) != -1]
                        if any(_assign):
                            res += self.finding(_assign[0].Origin,
                                                _assign[0].InFileLine,
                                                self.Msg.replace("{FILE}", os.path.basename(i)))
                except UnicodeDecodeError:
                    pass
        return res
