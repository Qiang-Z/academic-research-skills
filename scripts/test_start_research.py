#!/usr/bin/env python3
"""End-to-end tests of the beginner intake; synthetic fixtures remain in TEMP."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / 'scripts/start_research.py'
PIPELINE = ROOT / 'scripts/research_pipeline.py'
PRIVATE_VALUE = 'PRIVATE_FIXTURE_VALUE_NOT_FOR_REPORT'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = Path(tempfile.mkdtemp(prefix='ars-intake-tests-')).resolve()

    def setUp(self):
        self.folder = self.base / self.id().rsplit('.', 1)[-1]
        self.folder.mkdir()
        self.paper = self.folder / 'paper.md'
        self.paper.write_text('# Authored fixture only\n' + PRIVATE_VALUE + '\n', encoding='utf-8')
        self.data = self.folder / 'data.csv'
        self.data.write_text('record_id,predictor,outcome\n1,2,' + PRIVATE_VALUE + '\n2,,5\n', encoding='utf-8')

    def cli(self, *args, expected=None):
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ENTRY), *map(str, args)],
                                cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=45)
        if expected is not None:
            self.assertEqual(result.returncode, expected, result.stdout + '\n' + result.stderr)
        return result

    def start(self, name='run', paper=True, data=True, extra=(), expected=0):
        run = self.folder / name
        args = ['start', '--question', 'Does a specified predictor help describe a stated outcome?', '--output', run]
        if paper:
            args += ['--paper', self.paper]
        if data:
            args += ['--data', self.data]
        result = self.cli(*args, *extra, expected=expected)
        return run, result

    def issues(self, run):
        return {item['code'] for item in read(run / 'CHECKS.json')['issues']}

    def material(self, run, suffix):
        return next(item for item in read(run / 'CHECKS.json')['materials'] if item['source'].endswith(suffix))

    def test_01_question_only_stops_honestly_and_check_does_not_advance(self):
        run, result = self.start(paper=False, data=False, expected=2)
        checks = read(run / 'CHECKS.json')
        self.assertEqual(checks['status'], 'needs_attention')
        self.assertEqual(checks['pipeline']['current_stage'], 'question')
        self.assertTrue(checks['issues'])
        self.assertTrue(1 <= len(checks['next_actions']) <= 3)
        self.assertNotEqual(read(run / 'state.json')['status'], 'complete')
        for name in ('evidence.json', 'protocol.json', 'experiment.json', 'REPORT.md'):
            self.assertFalse((run / name).exists(), name)
        before = (run / 'state.json').read_bytes()
        self.cli('check', '--run', run, expected=2)
        self.assertEqual((run / 'state.json').read_bytes(), before)
        self.assertNotIn('Traceback', result.stderr)

    def test_02_available_text_and_table_are_not_claimed_as_completed_research(self):
        run, result = self.start()
        checks = read(run / 'CHECKS.json')
        self.assertEqual(checks['status'], 'ready_for_review')
        self.assertEqual(self.material(run, 'paper.md')['status'], 'text_available')
        self.assertEqual(self.material(run, 'data.csv')['status'], 'table_preview')
        self.assertEqual(checks['pipeline']['current_stage'], 'question')
        self.assertFalse((run / 'evidence.json').exists())
        self.assertFalse((run / 'results').exists())
        for item in checks['materials']:
            snapshot = run / item['path']
            self.assertTrue(snapshot.is_file())
            self.assertEqual(item['sha256'], sha(snapshot))
            self.assertEqual(snapshot.read_bytes(), Path(item['source']).read_bytes())
        published = result.stdout + result.stderr + (run / 'CHECKS.json').read_text(encoding='utf-8') + (run / 'START_HERE.md').read_text(encoding='utf-8')
        self.assertNotIn(PRIVATE_VALUE, published)
        history = run / 'intake-checks/0001.json'
        original_history = history.read_bytes()
        state = (run / 'state.json').read_bytes()
        self.cli('check', '--run', run, expected=0)
        self.assertEqual(history.read_bytes(), original_history)
        self.assertTrue((run / 'intake-checks/0002.json').is_file())
        self.assertEqual((run / 'state.json').read_bytes(), state)

    def test_03_urls_remain_unretrieved_references(self):
        run, _ = self.start(paper=False, data=False,
                            extra=['--paper', 'https://example.invalid/article', '--data', 'https://example.invalid/data.csv'], expected=2)
        checks = read(run / 'CHECKS.json')
        self.assertEqual([x['status'] for x in checks['materials']], ['pending_retrieval', 'pending_retrieval'])
        self.assertTrue(all('sha256' not in item for item in checks['materials']))
        self.assertFalse((run / 'evidence.json').exists())
        self.assertNotEqual(checks['status'], 'ready_for_review')

    def test_04_missing_empty_bad_encoding_and_malformed_csv_are_actionable(self):
        missing = self.folder / 'missing.csv'
        empty = self.folder / 'empty.csv'; empty.write_bytes(b'')
        encoded = self.folder / 'encoded.csv'; encoded.write_bytes(b'id,name\n1,\xff\xfe\n')
        malformed = self.folder / 'ragged.csv'; malformed.write_text('a,b\n1,2,3\n', encoding='utf-8')
        duplicate = self.folder / 'duplicate.csv'; duplicate.write_text('a,a\n1,2\n', encoding='utf-8')
        extra = []
        for path in (missing, empty, encoded, malformed, duplicate):
            extra += ['--data', path]
        run, result = self.start(data=False, extra=extra, expected=2)
        self.assertEqual(self.material(run, 'missing.csv')['status'], 'missing')
        self.assertEqual(self.material(run, 'empty.csv')['status'], 'empty')
        self.assertIn(self.material(run, 'encoded.csv')['status'], ('unreadable', 'invalid_format'))
        self.assertEqual(self.material(run, 'ragged.csv')['status'], 'invalid_format')
        self.assertIn(self.material(run, 'duplicate.csv')['status'], ('invalid_format', 'unreadable'))
        self.assertTrue(read(run / 'CHECKS.json')['next_actions'])
        self.assertNotIn('Traceback', result.stderr)

    def test_05_check_recovers_missing_material_and_can_append_before_protocol(self):
        missing = self.folder / 'later.csv'
        run, _ = self.start(data=False, extra=['--data', missing], expected=2)
        old = (run / 'intake-checks/0001.json').read_bytes()
        missing.write_text('x,y\n1,2\n', encoding='utf-8')
        self.cli('check', '--run', run, expected=0)
        self.assertEqual(self.material(run, 'later.csv')['status'], 'table_preview')
        self.assertEqual((run / 'intake-checks/0001.json').read_bytes(), old)
        state = (run / 'state.json').read_bytes()
        self.cli('check', '--run', run, '--data', self.data, expected=0)
        self.assertEqual(len(read(run / 'CHECKS.json')['materials']), 3)
        self.assertEqual((run / 'state.json').read_bytes(), state)

    def test_06_source_and_snapshot_changes_are_detected_without_rewriting_history(self):
        run, _ = self.start()
        before = self.data.read_bytes()
        item = self.material(run, 'data.csv'); snapshot = run / item['path']
        snapshot_before = snapshot.read_bytes()
        self.data.write_bytes(before + b'3,4,6\n')
        self.cli('check', '--run', run, expected=2)
        self.assertIn('source_changed', self.issues(run))
        self.assertEqual(snapshot.read_bytes(), snapshot_before)
        self.data.write_bytes(before)
        snapshot.write_bytes(snapshot_before + b'3,5,7\n')
        self.cli('check', '--run', run, expected=2)
        self.assertIn('snapshot_changed', self.issues(run))
        self.assertEqual(read(run / 'intake-checks/0001.json')['status'], 'ready_for_review')

    def test_07_declared_missing_dependency_is_not_ready_and_user_code_is_not_executed(self):
        marker = self.folder / 'executed.txt'
        program = self.folder / 'untrusted.py'
        program.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n', encoding='utf-8')
        run, result = self.start(extra=['--require', 'ars-test-package-deliberately-absent==1.0', '--paper', program], expected=2)
        dependency = next(d for d in read(run / 'CHECKS.json')['dependencies'] if d['name'] == 'ars-test-package-deliberately-absent')
        self.assertEqual(dependency['status'], 'not_detected')
        self.assertEqual(self.material(run, 'untrusted.py')['status'], 'unsupported')
        self.assertFalse(marker.exists())
        self.assertNotIn('Traceback', result.stderr)

    def test_08_existing_or_repository_output_is_rejected_without_overwrite(self):
        run, _ = self.start()
        before = {p.relative_to(run).as_posix(): sha(p) for p in run.rglob('*') if p.is_file()}
        self.cli('start', '--question', 'Replacement question', '--output', run, expected=1)
        after = {p.relative_to(run).as_posix(): sha(p) for p in run.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        forbidden = ROOT / 'ars-test-must-not-create-intake'
        self.assertFalse(forbidden.exists())
        self.cli('start', '--question', 'Fixture', '--output', forbidden, expected=1)
        self.assertFalse(forbidden.exists())

    def test_09_accepted_evidence_is_explained_and_protocol_blocks_new_materials(self):
        run, _ = self.start()
        item = self.material(run, 'data.csv')
        def save(name, obj):
            (run / name).write_text(json.dumps(obj) + '\n', encoding='utf-8')
        save('question.json', {'question': 'Authored fixture comparison', 'scope': 'Contract plumbing only',
             'resources': 'Authored small table', 'stopping_condition': 'One fixture comparison'})
        save('evidence.json', {'mode': 'reused', 'search_log': [], 'unresolved': ['No actual scientific reading'],
             'sources': [{'id': 'S1', 'url': 'https://example.invalid/authored-fixture', 'version': 'fixture-v1',
              'checked_at': '2026-10-23', 'status': 'read', 'read_scope': 'Authored fixture text only',
              'locator': 'Fixture itself', 'supports': 'Contract test only', 'does_not_support': 'Scientific validity'}]})
        advance_args = [sys.executable, '-B', '-X', 'utf8', str(PIPELINE), 'advance', '--run', str(run)]
        before_protocol = subprocess.run(advance_args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=45)
        self.assertEqual(before_protocol.returncode, 2, before_protocol.stdout + before_protocol.stderr)
        self.assertEqual(read(run / 'state.json')['stages'][1]['status'], 'accepted')
        evidence_bytes = (run / 'evidence.json').read_bytes()
        prior_state = (run / 'state.json').read_bytes()
        supplement = self.folder / 'supplement.md'
        supplement.write_text('Authored supplemental fixture, not scientific evidence.\n', encoding='utf-8')
        self.cli('check', '--run', run, '--paper', supplement, expected=0)
        self.assertEqual((run / 'evidence.json').read_bytes(), evidence_bytes)
        self.assertEqual((run / 'state.json').read_bytes(), prior_state)
        notes = '\n'.join(read(run / 'CHECKS.json')['handoff_notes'])
        self.assertIn('未自动纳入', notes)
        self.assertIn('问题范围', notes)
        self.assertIn('未自动纳入', (run / 'START_HERE.md').read_text(encoding='utf-8'))
        save('protocol.json', {'design': 'Fixture only', 'unit': 'Authored row', 'conditions': ['one'],
             'metrics': ['fixture count'], 'split_or_comparison': 'No actual scientific comparison',
             'leakage_control': 'No model fitted', 'stopping_rule': 'No execution in this test',
             'previous_results_known': True,
             'data': [{'path': item['path'], 'sha256': item['sha256'], 'source_id': 'S1', 'license': 'Authored fixture'}]})
        completed = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(PIPELINE), 'advance', '--run', str(run)],
                                   cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=45)
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        state = read(run / 'state.json')
        self.assertEqual(state['stages'][2]['status'], 'accepted')
        state_bytes = (run / 'state.json').read_bytes()
        extra = self.folder / 'extra.csv'; extra.write_text('a,b\n3,4\n', encoding='utf-8')
        intake_bytes = (run / 'intake.json').read_bytes()
        self.cli('check', '--run', run, '--data', extra, expected=1)
        self.assertEqual((run / 'intake.json').read_bytes(), intake_bytes)
        self.assertEqual((run / 'state.json').read_bytes(), state_bytes)
        # Rechecking may correctly request experiment inputs; it must not mutate
        # the already accepted protocol or turn a material preview into results.
        check = self.cli('check', '--run', run)
        self.assertIn(check.returncode, (0, 2), check.stdout + check.stderr)
        self.assertEqual((run / 'state.json').read_bytes(), state_bytes)
        self.assertEqual(read(run / 'CHECKS.json')['pipeline']['current_stage'], 'experiment')

    def test_10_metadata_version_checks_and_document_readers_are_not_execution_checks(self):
        # This is the sole controlled dependency simulation. No packages are
        # installed/imported; CLI tests elsewhere exercise the real environment.
        old_path = list(sys.path)
        try:
            sys.path.insert(0, str(ROOT / 'scripts'))
            spec = importlib.util.spec_from_file_location('intake_metadata_test', ENTRY)
            entry = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(entry)
        finally:
            sys.path[:] = old_path
        run = self.folder / 'version'
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(entry.importlib.metadata, 'version', return_value='1.0'), redirect_stdout(stdout), redirect_stderr(stderr):
            code = entry.main(['start', '--question', 'Fixture comparison', '--paper', str(self.paper),
                              '--data', str(self.data), '--require', 'ars-fixture-package==2.0', '--output', str(run)])
        self.assertEqual(code, 2, stdout.getvalue() + stderr.getvalue())
        dependency = next(d for d in read(run / 'CHECKS.json')['dependencies'] if d['name'] == 'ars-fixture-package')
        self.assertEqual(dependency['status'], 'version_mismatch')
        self.assertFalse(dependency['import_tested'])
        with patch.object(entry.importlib.metadata, 'version', return_value=None):
            self.assertEqual(entry.dependency('ars-fixture-package', 'Malformed metadata fixture')['status'], 'manual_check')
        pdf = self.folder / 'paper.pdf'; pdf.write_bytes(b'%PDF-1.4\n% Authored header-only fixture, not a valid scientific document\n')
        workbook = self.folder / 'table.xlsx'
        with zipfile.ZipFile(workbook, 'w') as archive:
            archive.writestr('xl/workbook.xml', '<workbook/>')
        other = self.folder / 'formats'
        with patch.object(entry.importlib.metadata, 'version', side_effect=entry.importlib.metadata.PackageNotFoundError), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = entry.main(['start', '--question', 'Fixture comparison', '--paper', str(pdf), '--data', str(workbook), '--output', str(other)])
        self.assertEqual(code, 2)
        checked = read(other / 'CHECKS.json')
        self.assertTrue(all(m['status'] == 'requires_reader' for m in checked['materials']))
        dependencies = {d['name']: d for d in checked['dependencies']}
        for package in ('pypdf', 'openpyxl'):
            self.assertEqual(dependencies[package]['status'], 'not_detected')
            self.assertFalse(dependencies[package]['import_tested'])
        self.assertFalse((other / 'evidence.json').exists())

    def test_11_bounded_and_non_utf8_table_previews_keep_their_actual_scope(self):
        large = self.folder / 'large.csv'
        large.write_text('id,x\n' + ''.join(f'{i},2\n' for i in range(1002)), encoding='utf-8')
        chinese = self.folder / 'chinese.csv'
        chinese.write_bytes('编号,数值\n1,2\n'.encode('gb18030'))
        run, _ = self.start(data=False, extra=['--data', large, '--data', chinese])
        first = self.material(run, 'large.csv')['inspection']
        self.assertEqual(first['rows_inspected'], 1000)
        self.assertFalse(first['complete_scan'])
        second = self.material(run, 'chinese.csv')['inspection']
        self.assertEqual(second['encoding'], 'gb18030')
        self.assertEqual(second['columns'], ['编号', '数值'])
        self.assertTrue(second['complete_scan'])

    def test_12_automatic_output_and_large_file_limit_need_no_user_configuration(self):
        result = self.cli('start', '--question', 'Minimal authored fixture comparison',
                          '--paper', self.paper, '--data', self.data, expected=0)
        line = next(x for x in result.stdout.splitlines() if x.startswith('项目目录：'))
        automatic = Path(line.split('：', 1)[1]).resolve()
        self.assertTrue(automatic.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.assertFalse(automatic.is_relative_to(ROOT))
        self.assertEqual(read(automatic / 'CHECKS.json')['status'], 'ready_for_review')
        self.assertFalse((automatic / 'REPORT.md').exists())
        large = self.folder / 'beyond-limit.csv'
        with large.open('wb') as stream:
            stream.truncate(50 * 1024 * 1024 + 1)
        run, _ = self.start(data=False, extra=['--data', large], expected=2)
        material = self.material(run, 'beyond-limit.csv')
        self.assertEqual(material['status'], 'too_large')
        self.assertNotIn('path', material)
        self.assertNotIn('sha256', material)


if __name__ == '__main__':
    unittest.main(verbosity=2)
