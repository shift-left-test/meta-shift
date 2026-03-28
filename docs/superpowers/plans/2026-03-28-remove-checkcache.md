# Remove do_checkcache Task Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `do_checkcache` 태스크와 관련된 모든 코드를 프로젝트에서 완전히 제거한다. master 브랜치에서 먼저 작업한 뒤, 7개의 `-next` 브랜치에 cherry-pick한다.

**Architecture:** checkcache는 Bitbake 태스크 체인(checkcache.bbclass -> shifttest -> shiftutils)과 4개의 빌드시스템 클래스(cmake/autotools/qmake/enact), 설정 파일, 테스트로 구성된다. 파일 삭제 1개 + 파일 수정 16개로 완전 제거한다.

**Tech Stack:** Bitbake/Yocto bbclass, Python (pytest), JSON config

---

## Branch Strategy

1. `master` 브랜치에서 **단일 커밋**으로 모든 변경사항 적용
2. 다음 7개 브랜치에 순서대로 cherry-pick:
   - `kirkstone-next`, `langdale-next`, `nanbield-next`, `scarthgap-next`, `styhead-next`, `walnascar-next`, `whinlatter-next`
3. 브랜치별 차이점 (cherry-pick 시 conflict 가능):
   - **kirkstone-next ~ nanbield-next:** `checkcache.bbclass`에서 `SSTATEPOSTINSTFUNCS` 사용 (master는 `SSTATEPOSTUNPACKFUNCS`) — 파일 자체를 삭제하므로 conflict 시 삭제 선택
   - **kirkstone-next:** `shiftutils.bbclass`에 추가 diff 있음 — 해당 브랜치의 `shiftutils_get_source_availability`/`shiftutils_get_sstate_availability` 함수 위치가 다를 수 있음
   - **walnascar-next:** `test/conf/report.conf`가 확장된 형태 — conflict 시 `checkcache` 라인만 제거

## File Structure

### 삭제 대상 (1개)
| File | Role |
|------|------|
| `classes/checkcache.bbclass` | sstate 빌드 후 캐시 정보를 수집하는 Bitbake 클래스 |

### 수정 대상 (16개)
| File | Changes |
|------|---------|
| `classes/shifttest.bbclass` | addtask/stub/함수/report분기/lockfile 제거 |
| `classes/shifttasks.bbclass` | do_checkcacheall 블록 제거 |
| `classes/shiftutils.bbclass` | `get_source_availability()`, `get_sstate_availability()` 제거 |
| `classes/cmaketest.bbclass` | `do_checkcache` 함수 + EXPORT_FUNCTIONS 수정 |
| `classes/autotoolstest.bbclass` | `do_checkcache` 함수 + EXPORT_FUNCTIONS 수정 |
| `classes/qmaketest.bbclass` | `do_checkcache` 함수 + EXPORT_FUNCTIONS 수정 |
| `classes/enacttest.bbclass` | `do_checkcache` 함수 + EXPORT_FUNCTIONS + report tasks 수정 |
| `test/conf/test.conf` | `INHERIT:append: " checkcache"` 제거 |
| `test/conf/report.conf` | `INHERIT:append: " checkcache"` 제거 |
| `test/cmaketest_test.py` | `test_do_checkcache` 함수 제거 |
| `test/autotoolstest_test.py` | `test_do_checkcache` 함수 제거 |
| `test/qmaketest_test.py` | `test_do_checkcache` 함수 제거 |
| `test/enacttest_test.py` | `test_do_checkcache` 함수 제거 |
| `test/devtool_modify_test.py` | `test_do_checkcache` 함수 제거 |
| `test/shifttasks_test.py` | `test_do_checkcacheall` 함수 제거 |
| `README.md` | checkcache 설명 라인 제거 |

**참고:** `CLAUDE.md`는 이 커밋 후 별도로 업데이트 (코드 변경과 분리)

---

## Task 1: Remove checkcache.bbclass

**Files:**
- Delete: `classes/checkcache.bbclass`

- [ ] **Step 1: Delete the file**

```bash
git rm classes/checkcache.bbclass
```

---

## Task 2: Remove checkcache from shifttest.bbclass

**Files:**
- Modify: `classes/shifttest.bbclass:38-44` (task definition + stub)
- Modify: `classes/shifttest.bbclass:46-106` (shifttest_checkcache function)
- Modify: `classes/shifttest.bbclass:116` (report default tasks list)
- Modify: `classes/shifttest.bbclass:138-143` (report checkcache branch)
- Modify: `classes/shifttest.bbclass:163` (lockfile)

- [ ] **Step 1: Remove task definition and stub (lines 38-45)**

Remove these lines:
```
addtask checkcache after do_build
do_checkcache[nostamp] = "1"
do_checkcache[doc] = "Check cache availability of the recipe"

shifttest_do_checkcache() {
    :
}
```

- [ ] **Step 2: Remove shifttest_checkcache(d) function (lines 46-106)**

Remove the entire `def shifttest_checkcache(d):` function including `make_plain_report`, `make_json_report` helpers, and the function body through line 105 (the closing of the json write block). Keep the blank line before `addtask report`.

- [ ] **Step 3: Update shifttest_report default tasks list (line 116)**

Change:
```python
def shifttest_report(d, tasks=["checkcode", "test", "coverage", "checkcache", "checktest"]):
```
To:
```python
def shifttest_report(d, tasks=["checkcode", "test", "coverage", "checktest"]):
```

- [ ] **Step 4: Remove checkcache branch in shifttest_report (lines 138-143)**

Remove these lines from inside `shifttest_report()`:
```python
    if "checkcache" in tasks:
        if "checkcache" in str(dd.getVar("INHERIT", True)):
            dd.setVar("BB_CURRENTTASK", "checkcache")
            exec_func("do_checkcache", dd)
        else:
            plain("Skipping do_checkcache because checkcache is not inherited", dd)
```

- [ ] **Step 5: Remove lockfile line (line 163)**

Remove this line from the `python()` anonymous function:
```python
        d.appendVarFlag("do_checkcache", "lockfiles", "${TMPDIR}/do_checkcache.lock")
```

---

## Task 3: Remove checkcacheall from shifttasks.bbclass

**Files:**
- Modify: `classes/shifttasks.bbclass:66-75`

- [ ] **Step 1: Remove the entire checkcacheall block (lines 66-75)**

Remove these lines:
```
addtask checkcacheall
do_checkcacheall[recrdeptask] = "do_checkcacheall do_checkcache"
do_checkcacheall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_checkcacheall[nostamp] = "1"
do_checkcacheall[doc] = "Checks cache availability of all recipes required to build the target"
do_checkcacheall[postfuncs] = "show_affected_recipes"
do_checkcacheall[vardepsexclude] = "show_affected_recipes"
do_checkcacheall() {
    :
}
```

---

## Task 4: Remove checkcache utility functions from shiftutils.bbclass

**Files:**
- Modify: `classes/shiftutils.bbclass:240-274` (get_source_availability)
- Modify: `classes/shiftutils.bbclass:276-430` (get_sstate_availability)

- [ ] **Step 1: Remove shiftutils_get_source_availability (lines 240-274)**

Remove from `def shiftutils_get_source_availability(d):` through `shiftutils_get_source_availability[vardepsexclude] += "BB_TASKDEPDATA"`.

- [ ] **Step 2: Remove shiftutils_get_sstate_availability (lines 276-430)**

Remove from `def shiftutils_get_sstate_availability(d, siginfo=False):` through `shiftutils_get_sstate_availability[vardepsexclude] += "BB_TASKDEPDATA NATIVELSBSTRING"`.

---

## Task 5: Remove do_checkcache from build system classes

**Files:**
- Modify: `classes/cmaketest.bbclass:93-95` (function) and `:101` (EXPORT_FUNCTIONS)
- Modify: `classes/autotoolstest.bbclass:127-129` (function) and `:135` (EXPORT_FUNCTIONS)
- Modify: `classes/qmaketest.bbclass:99-101` (function) and `:107` (EXPORT_FUNCTIONS)
- Modify: `classes/enacttest.bbclass:186-188` (function), `:191` (report tasks), `:195` (EXPORT_FUNCTIONS)

- [ ] **Step 1: cmaketest.bbclass — remove function**

Remove:
```python
python cmaketest_do_checkcache() {
    shifttest_checkcache(d)
}
```

- [ ] **Step 2: cmaketest.bbclass — update EXPORT_FUNCTIONS**

Change:
```
EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest do_checkcache do_report
```
To:
```
EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest do_report
```

- [ ] **Step 3: autotoolstest.bbclass — remove function**

Remove:
```python
python autotoolstest_do_checkcache() {
    shifttest_checkcache(d)
}
```

- [ ] **Step 4: autotoolstest.bbclass — update EXPORT_FUNCTIONS**

Same pattern as Step 2: remove `do_checkcache` from the EXPORT_FUNCTIONS line.

- [ ] **Step 5: qmaketest.bbclass — remove function**

Remove:
```python
python qmaketest_do_checkcache() {
    shifttest_checkcache(d)
}
```

- [ ] **Step 6: qmaketest.bbclass — update EXPORT_FUNCTIONS**

Same pattern as Step 2: remove `do_checkcache` from the EXPORT_FUNCTIONS line.

- [ ] **Step 7: enacttest.bbclass — remove function**

Remove:
```python
python enacttest_do_checkcache() {
    shifttest_checkcache(d)
}
```

- [ ] **Step 8: enacttest.bbclass — update report tasks list**

Change:
```python
    tasks = ["checkcode", "coverage", "checkcache", "checktest"]
```
To:
```python
    tasks = ["checkcode", "coverage", "checktest"]
```

- [ ] **Step 9: enacttest.bbclass — update EXPORT_FUNCTIONS**

Same pattern as Step 2: remove `do_checkcache` from the EXPORT_FUNCTIONS line.

---

## Task 6: Remove checkcache from test configurations

**Files:**
- Modify: `test/conf/test.conf`
- Modify: `test/conf/report.conf`

- [ ] **Step 1: test.conf — remove checkcache inherit**

Remove this key-value pair from the `"local.conf"` JSON object:
```json
"INHERIT:append": " checkcache",
```

- [ ] **Step 2: report.conf — remove checkcache inherit**

Remove the same key-value pair:
```json
"INHERIT:append": " checkcache",
```

---

## Task 7: Remove checkcache test functions

**Files:**
- Modify: `test/cmaketest_test.py:23-27`
- Modify: `test/autotoolstest_test.py:23-27`
- Modify: `test/qmaketest_test.py:23-27`
- Modify: `test/enacttest_test.py:23-27`
- Modify: `test/devtool_modify_test.py:25-29`
- Modify: `test/shifttasks_test.py:16-17`

- [ ] **Step 1: cmaketest_test.py — remove test_do_checkcache**

Remove:
```python
def test_do_checkcache(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]
```

- [ ] **Step 2: autotoolstest_test.py — remove test_do_checkcache**

Remove (same structure, uses `autotools-project-1.0.0-r0`):
```python
def test_do_checkcache(stdout, report):
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/autotools-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]
```

- [ ] **Step 3: qmaketest_test.py — remove test_do_checkcache**

Remove (same structure, uses `qmake-project-1.0.0-r0`):
```python
def test_do_checkcache(stdout, report):
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/qmake-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]
```

- [ ] **Step 4: enacttest_test.py — remove test_do_checkcache**

Remove (same structure, uses `enact-project-1.0.0-r0`):
```python
def test_do_checkcache(stdout, report):
    assert stdout.contains("enact-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/enact-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]
```

- [ ] **Step 5: devtool_modify_test.py — remove test_do_checkcache**

Remove (same structure, uses `cmake-project-1.0.0-r0`):
```python
def test_do_checkcache(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]
```

- [ ] **Step 6: shifttasks_test.py — remove test_do_checkcacheall**

Remove:
```python
def test_do_checkcacheall(stdout):
    assert stdout.contains("do_checkcacheall")
```

---

## Task 8: Update documentation

**Files:**
- Modify: `README.md:82`

- [ ] **Step 1: README.md — remove checkcache line**

Remove this line:
```markdown
    *   `do_checkcache`: Checks SState and Premirror availability.
```

---

## Task 9: Commit on master

- [ ] **Step 1: Verify no remaining references**

```bash
grep -r "checkcache" classes/ test/ conf/ README.md --include="*.bbclass" --include="*.py" --include="*.conf" --include="*.md"
```

Expected: No output (zero matches).

- [ ] **Step 2: Commit all changes**

```bash
git add -A
git commit -m "Remove do_checkcache task and all related code

Remove the do_checkcache/do_checkcacheall tasks, checkcache.bbclass,
utility functions (get_source_availability, get_sstate_availability),
and all associated tests, configurations, and documentation.

The devtool cache command remains available as an alternative."
```

---

## Task 10: Cherry-pick to all -next branches

- [ ] **Step 1: Cherry-pick to each branch**

```bash
COMMIT=$(git rev-parse HEAD)

for branch in kirkstone-next langdale-next nanbield-next scarthgap-next styhead-next walnascar-next whinlatter-next; do
    git checkout $branch
    git cherry-pick $COMMIT
    # If conflict: git rm classes/checkcache.bbclass, resolve other conflicts, git cherry-pick --continue
done

git checkout master
```

**Conflict resolution guide:**
- `classes/checkcache.bbclass` — 삭제 대상이므로 conflict 시 `git rm classes/checkcache.bbclass`
- `classes/shiftutils.bbclass` (kirkstone-next) — 해당 브랜치에서 함수 위치/내용이 다를 수 있음. 삭제 대상 함수를 수동으로 확인 후 제거
- `test/conf/report.conf` (walnascar-next) — `INHERIT:append` 라인만 제거, 나머지 유지

- [ ] **Step 2: Verify each branch**

각 브랜치에서:
```bash
grep -r "checkcache" classes/ test/ conf/ README.md --include="*.bbclass" --include="*.py" --include="*.conf" --include="*.md"
```
Expected: No output.

---

## Task 11: Update CLAUDE.md (별도 커밋)

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Remove checkcache references from CLAUDE.md**

Remove/update:
- Architecture description에서 `checkcache` 언급 제거
- Task structure에서 `checkcache` 제거
- Bitbake Task Quick Reference에서 `checkcache` 라인 제거

- [ ] **Step 2: Commit and cherry-pick**

```bash
git commit -am "Update CLAUDE.md: remove checkcache references"
# Cherry-pick to all -next branches (same process as Task 10)
```
