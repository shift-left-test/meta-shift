python checkcacheinternal() {
    import bb.fetch2

    class Fetch2(bb.fetch2.Fetch):
        def __init__(self, d):
            self.src_uri = (d.getVar("SRC_URI", True) or "").split()
            super(Fetch2, self).__init__(self.src_uri, d)

        def size(self):
            return len(self.src_uri)

        def check_premirrors(self):
            def mirror_from_string(s):
                mirrors = bb.fetch2.mirror_from_string(s)
                return [x for x in mirrors if not "downloads.yoctoproject.org" in x[1]]

            for u in self.urls:
                # Ignores local URLs
                if u.startswith("file://"):
                    continue
                ud = self.ud[u]
                ud.setup_localpath(self.d)
                # Check if the source tarball and the stamp exist
                if os.path.exists(ud.localpath) and (not ud.needdonestamp or os.path.exists(ud.donestamp)):
                    continue
                mirrors = mirror_from_string(self.d.getVar("PREMIRRORS", True))
                ret = bb.fetch2.try_mirrors(self, self.d, ud, mirrors, True)
                if not ret:
                    return False
            return True

    path = d.expand("${TOPDIR}/checkcache/${PN}")
    bb.utils.mkdirhier(path)
    with open(os.path.join(path,"source_availability"), "w") as f:
        f.write(str(Fetch2(d).check_premirrors()))
}

SSTATEPOSTINSTFUNCS_append = " checkcacheinternal"
sstate_install[vardepsexclude] += "checkcacheinternal"
SSTATEPOSTINSTFUNCS[vardepvalueexclude] .= "| checkcacheinternal"
