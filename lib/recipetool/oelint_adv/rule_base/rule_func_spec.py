import re

from oelint_parser.cls_item import Function
from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import get_valid_package_names
from oelint_parser.parser import INLINE_BLOCK
from oelint_parser.constants import CONSTANTS


class VarPnBpnUsage(Rule):
    def __init__(self):
        super(VarPnBpnUsage, self).__init__(id="oelint.func.specific",
                         severity="error",
                         message="'{}' is set specific to ['{}'], but isn't known from PACKAGES, MACHINE or resources")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                  attribute=Function.ATTR_FUNCNAME)
        _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, 
                                  attribute=Variable.ATTR_VAR, 
                                  attributeValue="COMPATIBLE_MACHINE")
        _packages = get_valid_package_names(stash, _file)
        _valid_funcs = ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm']
        for b in ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm']:
            _valid_funcs += ["{}-{}".format(b,p) for p in _packages if p.strip() and p != INLINE_BLOCK]
        for i in items:
            _machine = i.GetMachineEntry()
            if not _machine or _machine in CONSTANTS.MachinesKnown:
                continue
            if i.FuncName in _valid_funcs:
                continue
            if _machine in ["ptest"]:
                # known exceptions
                continue
            if _comp and re.match("".join(x.VarValueStripped for x in _comp), _machine):
                continue
            res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(i.FuncName, _machine))
        return res
