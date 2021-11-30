import re

from shift_oelint_adv.cls_rule import Rule
from shift_oelint_parser.cls_item import Variable
from shift_oelint_parser.constants import CONSTANTS
from shift_oelint_parser.helper_files import expand_term
from shift_oelint_parser.helper_files import get_valid_named_resources
from shift_oelint_parser.helper_files import get_valid_package_names


class VarPnBpnUsage(Rule):
    def __init__(self):
        super(VarPnBpnUsage, self).__init__(id='oelint.vars.specific',
                         severity='error',
                         message='\'{a}\' is set specific to [\'{b}\'], but isn\'t known from PACKAGES, MACHINE, DISTRO or resources',
                         onappend=False)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR,
                                  attributeValue='COMPATIBLE_MACHINE')
        _comp = ''.join(x.VarValueStripped for x in _comp)
        _packages = get_valid_package_names(stash, _file)
        _named_res = get_valid_named_resources(stash, _file)
        for i in items:
            _distro = []
            if i.GetDistroEntry():
                _distro = [i.GetDistroEntry(), expand_term(stash, _file, i.GetDistroEntry())]
            if any(x in _packages for x in _distro) or any(x in _named_res for x in _distro): # pragma: no cover
                continue # pragma: no cover
            if any(x in CONSTANTS.DistrosKnown for x in _distro):
                continue

            _machine = []
            if i.GetMachineEntry():
                _machine = [i.GetMachineEntry(), expand_term(
                    stash, _file, i.GetMachineEntry())]
            if not _machine:
                continue
            if any(x in _packages for x in _machine):
                continue
            if any(x in _named_res for x in _machine):
                continue
            if any(x in CONSTANTS.MachinesKnown for x in _machine):
                continue
            if _comp:
                if any(re.match(_comp, x) for x in _machine):
                    continue
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(a=i.VarName, b=_machine[0]))
        return res
