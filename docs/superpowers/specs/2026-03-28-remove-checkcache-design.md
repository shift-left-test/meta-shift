# Remove do_checkcache Task — Design Spec

**Date:** 2026-03-28
**Status:** Approved

## Summary

`do_checkcache` 태스크와 관련된 모든 코드를 프로젝트에서 완전히 제거한다.

## Scope

### 삭제 대상 파일
- `classes/checkcache.bbclass`

### 수정 대상 파일

#### bbclass 파일 (7개)
1. **`classes/shifttest.bbclass`**
   - `addtask checkcache after do_build` 및 관련 플래그 제거
   - `shifttest_do_checkcache()` 스텁 함수 제거
   - `shifttest_checkcache(d)` 함수 전체 제거
   - `shifttest_report()` 기본 tasks 리스트에서 `"checkcache"` 제거
   - `shifttest_report()` 내 checkcache 분기 조건문 제거
   - `do_checkcache` lockfile 설정 제거

2. **`classes/shifttasks.bbclass`**
   - `addtask checkcacheall` 및 관련 플래그/스텁 함수 제거

3. **`classes/shiftutils.bbclass`**
   - `shiftutils_get_source_availability()` 함수 제거
   - `shiftutils_get_sstate_availability()` 함수 제거

4. **`classes/cmaketest.bbclass`**
   - `cmaketest_do_checkcache()` 함수 제거
   - `EXPORT_FUNCTIONS`에서 `do_checkcache` 제거

5. **`classes/autotoolstest.bbclass`**
   - `autotoolstest_do_checkcache()` 함수 제거
   - `EXPORT_FUNCTIONS`에서 `do_checkcache` 제거

6. **`classes/qmaketest.bbclass`**
   - `qmaketest_do_checkcache()` 함수 제거
   - `EXPORT_FUNCTIONS`에서 `do_checkcache` 제거

7. **`classes/enacttest.bbclass`**
   - `enacttest_do_checkcache()` 함수 제거
   - `EXPORT_FUNCTIONS`에서 `do_checkcache` 제거
   - report tasks 목록에서 `"checkcache"` 제거

#### 설정 파일 (2개)
1. **`test/conf/test.conf`** — `"INHERIT:append": " checkcache"` 제거
2. **`test/conf/report.conf`** — `"INHERIT:append": " checkcache"` 제거

#### 테스트 파일 (6개)
1. **`test/cmaketest_test.py`** — `test_do_checkcache` 제거
2. **`test/autotoolstest_test.py`** — `test_do_checkcache` 제거
3. **`test/qmaketest_test.py`** — `test_do_checkcache` 제거
4. **`test/enacttest_test.py`** — `test_do_checkcache` 제거
5. **`test/devtool_modify_test.py`** — `test_do_checkcache` 제거
6. **`test/shifttasks_test.py`** — `test_do_checkcacheall` 제거

#### 문서 파일 (2개)
1. **`README.md`** — checkcache 관련 설명 제거
2. **`CLAUDE.md`** — checkcache 관련 설명 제거

## Approach

- 방법 A (완전 제거) 채택
- git history로 복원 가능하므로 코드 잔류 없이 깔끔하게 제거

## Constraints

- `EXPORT_FUNCTIONS` 행에서 `do_checkcache`만 제거, 나머지 태스크 유지
- `shiftutils.bbclass`에서 checkcache 전용 함수만 제거, 다른 유틸리티 보존
- `shifttest_report()`의 checkcache 조건 분기만 제거, 다른 태스크의 report 흐름 유지
