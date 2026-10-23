#!/usr/bin/env python3
"""Meaningful integration and failure tests; fixtures stay in new OS temp folders."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pipeline_under_test', HERE / 'research_pipeline.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = Path(tempfile.mkdtemp(prefix='ars-pipeline-tests-'))
        cls.demo = p.initialize(cls.base / 'demo', 'wine')
        if p.advance(cls.demo) != 0:
            raise RuntimeError('Real demo failed')

    def custom(self, suffix):
        return p.initialize(self.base / suffix, 'custom', 'Does a stated comparison change an observed outcome?')

    def prepared(self, suffix, run=None):
        run = run or self.custom(suffix)
        p.write(run / 'question.json', {'question': 'Fixture comparison', 'scope': 'Contract test fixture, not research',
                'resources': 'Authored two-row synthetic fixture', 'stopping_condition': 'One fixed comparison'})
        p.write(run / 'evidence.json', {'mode': 'reused', 'search_log': [], 'unresolved': ['No real scientific review'],
                'sources': [{'id': 'S1', 'url': 'https://example.org/test-fixture', 'version': 'test-v1',
                    'checked_at': '2026-10-23', 'status': 'read', 'read_scope': 'Contract test only',
                    'locator': 'Fixture source entry', 'supports': 'Schema plumbing only',
                    'does_not_support': 'Scientific validity or actual source identity'}]})
        (run / 'data.txt').write_text('synthetic fixture only\n1\n2\n', encoding='utf-8')
        p.write(run / 'protocol.json', {'design': 'Fixture only', 'unit': 'One authored value',
                'conditions': ['baseline', 'comparison'], 'metrics': ['fixture sum'],
                'split_or_comparison': 'Fixed authored pair', 'leakage_control': 'No learned transformation',
                'stopping_rule': 'One fixture calculation', 'previous_results_known': True,
                'data': [{'path': 'data.txt', 'sha256': p.digest(run / 'data.txt'), 'source_id': 'S1', 'license': 'Authored test fixture'}]})
        (run / 'result.txt').write_text('Fixture sum: 3\n', encoding='utf-8')
        p.write(run / 'experiment.json', {'status': 'measured', 'protocol_sha256': p.digest(run / 'protocol.json'),
                'command': 'Test fixture sum(1,2); not a real experiment', 'environment': 'Python unittest fixture',
                'artifacts': [{'id': 'R1', 'path': 'result.txt', 'sha256': p.digest(run / 'result.txt')}], 'failures': []})
        claim = {'id': 'C1', 'text': 'The fixture records the value 3.', 'artifact_ids': ['R1'],
                 'source_ids': ['S1'], 'locator': 'result.txt line 1'}
        limitations = ['Synthetic contract test; no scientific claim.']
        p.write(run / 'analysis.json', {'unit': 'Fixture value', 'comparisons': 'One authored sum',
                'limitations': limitations, 'claims': [claim]})
        p.write(run / 'claims.json', {'claims': [claim], 'limitations': limitations,
                'review_status': 'host_reviewed', 'review_scope': 'Fixture consistency only'})
        (run / 'REPORT.md').write_text(claim['text'] + '\n' + limitations[0], encoding='utf-8')
        return run

    def test_01_demo_verified_and_resume_does_not_recompute(self):
        before = copy.deepcopy(p.load_state(self.demo))
        attempts = sorted(x.name for x in (self.demo / 'attempts').iterdir())
        self.assertEqual(p.advance(self.demo), 0)
        after = p.load_state(self.demo)
        self.assertEqual(before['stages'], after['stages'])
        self.assertEqual(attempts, sorted(x.name for x in (self.demo / 'attempts').iterdir()))
        self.assertEqual(p.verify(self.demo), 0)
        self.assertEqual([s['mode'] for s in after['stages'][:3]], ['reused'] * 3)
        self.assertIn('template_generated', after['stages'][-1]['mode'])
        self.assertEqual(p.read(self.demo / 'evidence.json')['other_candidates'],
                         p.read(p.WINE / 'sources.json')['other_candidates'])

    def test_02_custom_waits_and_then_accepts_real_handoffs(self):
        run = self.custom('custom-paused')
        self.assertEqual(p.advance(run), 2)
        self.assertEqual(p.load_state(run)['status'], 'blocked')
        self.assertTrue((run / 'NEXT.md').is_file())
        next_text = (run / 'NEXT.md').read_text(encoding='utf-8')
        self.assertIn('真实已有材料', next_text)
        self.assertIn('模块索引', next_text)
        self.assertIn('主入口', next_text)
        full = self.prepared('custom-complete', run=run)
        self.assertEqual(p.advance(full), 0)
        self.assertEqual(p.verify(full), 0)
        self.assertTrue(all(s['validation_scope'] == 'structure_and_reference_integrity' for s in p.load_state(full)['stages']))

    def test_03_missing_evidence_does_not_run_experiment(self):
        run = self.custom('custom-missing')
        p.write(run / 'question.json', {'question': 'Q', 'scope': 'S', 'resources': 'R', 'stopping_condition': 'C'})
        self.assertEqual(p.advance(run), 2)
        state = p.load_state(run)
        self.assertEqual(state['stages'][0]['status'], 'accepted')
        self.assertEqual(state['stages'][1]['status'], 'blocked')
        self.assertFalse((run / 'attempts').exists())

    def test_04_modified_accepted_evidence_rejected(self):
        run = self.prepared('custom-source-change')
        self.assertEqual(p.advance(run), 0)
        obj = p.read(run / 'evidence.json'); obj['sources'][0]['supports'] = 'changed'
        p.write(run / 'evidence.json', obj)
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed'):
            p.advance(run)

    def test_05_modified_accepted_result_rejected(self):
        run = self.prepared('custom-result-change')
        self.assertEqual(p.advance(run), 0)
        (run / 'result.txt').write_text('wrong', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed'):
            p.verify(run)

    def test_06_missing_artifact_never_completes(self):
        run = self.prepared('custom-missing-artifact')
        (run / 'result.txt').unlink()
        self.assertEqual(p.advance(run), 2)
        self.assertEqual(p.load_state(run)['stages'][3]['status'], 'blocked')

    def test_07_unknown_and_unread_claim_sources_rejected(self):
        run = self.prepared('custom-unknown-source')
        obj = p.read(run / 'analysis.json'); obj['claims'][0]['source_ids'] = ['S404']
        p.write(run / 'analysis.json', obj)
        self.assertEqual(p.advance(run), 1)
        run = self.prepared('custom-unread-source')
        obj = p.read(run / 'evidence.json'); extra = dict(obj['sources'][0], id='S2', status='unavailable')
        obj['sources'].append(extra); p.write(run / 'evidence.json', obj)
        obj = p.read(run / 'analysis.json'); obj['claims'][0]['source_ids'] = ['S2']; p.write(run / 'analysis.json', obj)
        self.assertEqual(p.advance(run), 1)

    def test_08_path_escape_and_wrong_digest_rejected(self):
        run = self.prepared('custom-path-escape')
        obj = p.read(run / 'protocol.json'); obj['data'][0]['path'] = '../result.txt'; p.write(run / 'protocol.json', obj)
        self.assertEqual(p.advance(run), 1)
        run = self.prepared('custom-wrong-digest')
        obj = p.read(run / 'protocol.json'); obj['data'][0]['sha256'] = '0' * 64; p.write(run / 'protocol.json', obj)
        self.assertEqual(p.advance(run), 1)

    def test_09_failed_child_and_retry_preserve_logs(self):
        run = p.initialize(self.base / 'failed-child', 'wine')
        failed = subprocess.CompletedProcess([], 7, 'partial output', 'fixture failure')
        with patch.object(p.subprocess, 'run', return_value=failed):
            self.assertEqual(p.advance(run), 1)
        first = run / 'attempts/experiment-001/command.json'; old = first.read_bytes()
        self.assertEqual(p.load_state(run)['status'], 'failed')
        self.assertEqual(p.advance(run), 0)
        self.assertEqual(old, first.read_bytes())
        self.assertTrue((run / 'attempts/experiment-002/command.json').is_file())

    def test_10_timeout_is_failed_and_preserves_record(self):
        run = p.initialize(self.base / 'timed-out', 'wine')
        with patch.object(p.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['fixture'], 120, b'partial', b'timeout')):
            self.assertEqual(p.advance(run), 1)
        result = p.read(run / 'attempts/experiment-001/command.json')
        self.assertTrue(result['timed_out'])
        self.assertIsNone(result['exit_code'])
        self.assertEqual(p.load_state(run)['stages'][3]['status'], 'failed')

    def test_11_zero_exit_without_artifacts_is_failed(self):
        run = p.initialize(self.base / 'empty-success', 'wine')
        with patch.object(p.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'fake PASS', '')):
            self.assertEqual(p.advance(run), 1)
        self.assertEqual(p.load_state(run)['status'], 'failed')

    def test_12_optimized_python_rejected(self):
        env = dict(os.environ); env.pop('PYTHONOPTIMIZE', None)
        result = subprocess.run([sys.executable, '-O', '-B', str(HERE / 'research_pipeline.py'), 'doctor'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('disables', result.stderr)

    def test_13_existing_output_and_lock_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Output exists'):
            p.initialize(self.demo, 'wine')
        run = self.custom('locked')
        (run / '.pipeline.lock').write_text('fixture', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Run locked'):
            p.advance(run)

    def test_14_report_missing_limitations_rejected(self):
        run = self.prepared('custom-report-gap')
        (run / 'REPORT.md').write_text('The fixture records the value 3.', encoding='utf-8')
        self.assertEqual(p.advance(run), 1)
        self.assertEqual(p.load_state(run)['stages'][5]['status'], 'failed')

    def test_15_repository_fingerprint_change_rejected(self):
        run = self.prepared('custom-code-change')
        state = p.load_state(run); state['repository_inputs']['scripts/research_pipeline.py'] = '0' * 64
        p.save_state(run, state)
        with self.assertRaisesRegex(ValueError, 'Repository inputs or runner changed'):
            p.advance(run)

    def test_16_configurable_budgets_and_immutable_configuration(self):
        run = p.initialize(self.base / 'custom-budget', 'custom', 'Fixture question', max_searches=6, max_sources=10)
        self.prepared('unused', run=run)
        obj = p.read(run / 'evidence.json')
        obj['search_log'] = [{'query': 'fixture query ' + str(i), 'status': 'fixture only'} for i in range(5)]
        obj['sources'] += [dict(obj['sources'][0], id='S' + str(i)) for i in range(2, 10)]
        p.write(run / 'evidence.json', obj)
        self.assertEqual(p.advance(run), 0)
        state = p.load_state(run); state['limits']['host_max_searches'] = 100
        p.save_state(run, state)
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            p.verify(run)

    def test_17_attempt_budget_stops_after_three_failures(self):
        run = p.initialize(self.base / 'attempt-budget', 'wine')
        failed = subprocess.CompletedProcess([], 8, '', 'fixture failure')
        with patch.object(p.subprocess, 'run', return_value=failed) as mocked:
            for _ in range(4):
                self.assertEqual(p.advance(run), 1)
            self.assertEqual(mocked.call_count, 3)
        self.assertEqual(len(list((run / 'attempts').glob('experiment-*'))), 3)
        self.assertIn('budget exhausted', p.load_state(run)['stages'][3]['problem'])

    def test_18_malformed_contract_is_readable_failure(self):
        run = self.custom('malformed-contract')
        p.write(run / 'question.json', [])
        self.assertEqual(p.advance(run), 1)
        self.assertIn('JSON object', p.load_state(run)['stages'][0]['problem'])
        run = self.prepared('malformed-source')
        obj = p.read(run / 'evidence.json'); obj['sources'] = [[]]; p.write(run / 'evidence.json', obj)
        self.assertEqual(p.advance(run), 1)

    def test_19_doctor_requires_routing(self):
        real_safe = p.safe
        def missing_routing(base, name, exists=True):
            if name == 'workflows/automated-research/skill-routing.json':
                raise p.Blocked('Missing routing fixture')
            return real_safe(base, name, exists)
        with patch.object(p, 'safe', side_effect=missing_routing):
            with self.assertRaisesRegex(p.Blocked, 'Missing routing'):
                p.doctor()

    def test_20_positive_budget_required_and_cli_option_recorded(self):
        with self.assertRaisesRegex(ValueError, 'positive integers'):
            p.initialize(self.base / 'invalid-budget', 'custom', 'Q', max_searches=0)
        run = self.base / 'cli-budget'
        self.assertEqual(p.main(['init', '--topic', 'Q', '--output', str(run), '--max-searches', '7', '--max-sources', '12']), 2)
        state = p.load_state(run)
        self.assertEqual(state['limits']['host_max_searches'], 7)
        self.assertEqual(state['limits']['host_max_sources'], 12)

    def test_21_recorded_budget_excess_is_not_accepted(self):
        run = self.prepared('default-budget-excess')
        obj = p.read(run / 'evidence.json')
        obj['search_log'] = [{'query': 'fixture query', 'status': 'fixture only'} for _ in range(5)]
        p.write(run / 'evidence.json', obj)
        self.assertEqual(p.advance(run), 1)
        self.assertEqual(p.load_state(run)['stages'][1]['status'], 'failed')

    def test_22_prior_experiment_failure_and_partial_output_are_protected(self):
        run = p.initialize(self.base / 'failure-history-protected', 'wine')
        def fail_with_partial(argv, **kwargs):
            output = Path(argv[-1]); output.mkdir()
            (output / 'partial.txt').write_text('incomplete fixture output', encoding='utf-8')
            return subprocess.CompletedProcess(argv, 7, 'fixture stdout', 'fixture stderr')
        with patch.object(p.subprocess, 'run', side_effect=fail_with_partial):
            self.assertEqual(p.advance(run), 1)
        self.assertEqual(p.advance(run), 0)
        state = p.load_state(run)
        old = run / 'attempts/experiment-001/command.json'
        partial = run / 'attempts/experiment-001/output/partial.txt'
        self.assertIn(partial.relative_to(run).as_posix(), state['stages'][3]['outputs'])
        original = old.read_bytes(); old.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing file'):
            p.verify(run)
        old.write_bytes(original)
        partial.write_text('modified old partial result', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed'):
            p.verify(run)

    def test_23_prior_analysis_failure_logs_are_protected(self):
        run = p.initialize(self.base / 'analysis-failure-protected', 'wine')
        actual_run = p.subprocess.run
        def fail_analysis(argv, **kwargs):
            if any(str(x).endswith('verify_case.py') for x in argv):
                (run / 'attempts/analysis-001/partial.txt').write_text('partial audit fixture', encoding='utf-8')
                return subprocess.CompletedProcess(argv, 9, 'audit fixture stdout', 'audit fixture stderr')
            return actual_run(argv, **kwargs)
        with patch.object(p.subprocess, 'run', side_effect=fail_analysis):
            self.assertEqual(p.advance(run), 1)
        self.assertEqual(p.advance(run), 0)
        state = p.load_state(run)
        self.assertIn('attempts/analysis-001/partial.txt', state['stages'][4]['outputs'])
        old_stdout = run / 'attempts/analysis-001/stdout.txt'
        old_stdout.write_text('modified old failure log', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed'):
            p.verify(run)

    def test_24_custom_failure_paths_are_checked_and_frozen(self):
        run = self.prepared('custom-invalid-failure')
        obj = p.read(run / 'experiment.json'); obj['failures'] = ['../outside.log']; p.write(run / 'experiment.json', obj)
        self.assertEqual(p.advance(run), 1)
        run = self.prepared('custom-missing-failure')
        obj = p.read(run / 'experiment.json'); obj['failures'] = ['missing.log']; p.write(run / 'experiment.json', obj)
        self.assertEqual(p.advance(run), 2)
        run = self.prepared('custom-failure-protected')
        log = run / 'failure.log'; log.write_text('fixture failed attempt', encoding='utf-8')
        obj = p.read(run / 'experiment.json'); obj['failures'] = ['failure.log']; p.write(run / 'experiment.json', obj)
        self.assertEqual(p.advance(run), 0)
        log.write_text('modified custom failure', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed'):
            p.verify(run)

    def bind_code(self, run):
        code = run / 'research.py'
        code.write_text('print(1 + 2)\n', encoding='utf-8')
        config = run / 'model.json'
        p.write(config, {'fixture_condition': 'sum'})
        obj = p.read(run / 'protocol.json')
        obj['code'] = [{'path': path.name, 'sha256': p.digest(path)} for path in (code, config)]
        p.write(run / 'protocol.json', obj)
        experiment = p.read(run / 'experiment.json')
        experiment['protocol_sha256'] = p.digest(run / 'protocol.json')
        p.write(run / 'experiment.json', experiment)
        return code, config

    def test_25_custom_code_is_frozen_before_experiment_and_checked_on_resume(self):
        run = self.prepared('custom-code-before-experiment')
        code, config = self.bind_code(run)
        experiment = (run / 'experiment.json').read_bytes()
        (run / 'experiment.json').unlink()
        self.assertEqual(p.advance(run), 2)
        protocol = p.load_state(run)['stages'][2]
        self.assertEqual(protocol['implementation_binding'], 'declared_code_hashes')
        self.assertEqual(protocol['outputs'][code.name], p.digest(code))
        self.assertEqual(protocol['outputs'][config.name], p.digest(config))
        self.assertIn('已固定 protocol.code', (run / 'NEXT.md').read_text(encoding='utf-8'))
        (run / 'experiment.json').write_bytes(experiment)
        code.write_text('print(99)\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed: research.py'):
            p.advance(run)

    def test_26_custom_config_mutation_invalidates_completed_run(self):
        run = self.prepared('custom-config-protected')
        _, config = self.bind_code(run)
        self.assertEqual(p.advance(run), 0)
        self.assertEqual(p.verify(run), 0)
        p.write(config, {'fixture_condition': 'changed'})
        with self.assertRaisesRegex(ValueError, 'Accepted input/output changed: model.json'):
            p.verify(run)

    def test_27_custom_without_code_stays_compatible_and_explicitly_unbound(self):
        for empty in (False, True):
            with self.subTest(empty_code=empty):
                run = self.prepared('custom-unbound-' + str(empty))
                if empty:
                    obj = p.read(run / 'protocol.json'); obj['code'] = []; p.write(run / 'protocol.json', obj)
                    experiment = p.read(run / 'experiment.json')
                    experiment['protocol_sha256'] = p.digest(run / 'protocol.json')
                    p.write(run / 'experiment.json', experiment)
                self.assertEqual(p.advance(run), 0)
                self.assertEqual(p.verify(run), 0)
                self.assertEqual(p.load_state(run)['stages'][2]['implementation_binding'], 'not_bound')
                self.assertIn('未绑定实现（not_bound）', (run / 'NEXT.md').read_text(encoding='utf-8'))

    def test_28_custom_code_rejects_missing_wrong_digest_and_unsafe_path(self):
        variants = [('missing', 'missing.py', '0' * 64, 2),
                    ('wrong-digest', 'research.py', '0' * 64, 1),
                    ('unsafe', '../outside.py', '0' * 64, 1)]
        for suffix, path, expected, exit_code in variants:
            with self.subTest(variant=suffix):
                run = self.prepared('custom-code-' + suffix)
                self.bind_code(run)
                obj = p.read(run / 'protocol.json'); obj['code'] = [{'path': path, 'sha256': expected}]
                p.write(run / 'protocol.json', obj)
                self.assertEqual(p.advance(run), exit_code)
                self.assertNotEqual(p.load_state(run)['stages'][2]['status'], 'accepted')

    def test_29_changed_validated_bytes_are_not_accepted(self):
        actual_validate = p.validate_stage
        for target_stage in ('analysis', 'protocol'):
            with self.subTest(stage=target_stage):
                run = self.prepared('custom-validation-race-' + target_stage)
                code, _ = self.bind_code(run)
                def mutate_after_validation(run, stage, mode, limits=None):
                    validated = actual_validate(run, stage, mode, limits)
                    if stage == target_stage:
                        if stage == 'analysis':
                            obj = p.read(run / 'analysis.json'); obj['unit'] = ''
                            p.write(run / 'analysis.json', obj)
                        else:
                            code.write_text('print(99)\n', encoding='utf-8')
                    return validated
                with patch.object(p, 'validate_stage', side_effect=mutate_after_validation):
                    self.assertEqual(p.advance(run), 1)
                state = p.load_state(run)
                rejected = next(s for s in state['stages'] if s['id'] == target_stage)
                self.assertEqual(state['status'], 'failed')
                self.assertEqual(rejected['status'], 'failed')
                self.assertEqual(rejected['outputs'], {})
                self.assertIn('File changed during stage validation', rejected['problem'])

    def test_30_verify_rejects_change_after_validating_a_stage(self):
        run = self.prepared('custom-verify-race')
        self.assertEqual(p.advance(run), 0)
        actual_validate = p.validate_stage
        def mutate_after_validation(run, stage, mode, limits=None):
            validated = actual_validate(run, stage, mode, limits)
            if stage == 'analysis':
                obj = p.read(run / 'analysis.json'); obj['unit'] = ''
                p.write(run / 'analysis.json', obj)
            return validated
        with patch.object(p, 'validate_stage', side_effect=mutate_after_validation):
            with self.assertRaisesRegex(ValueError, 'File changed during stage validation: analysis.json'):
                p.verify(run)


if __name__ == '__main__':
    unittest.main(verbosity=2)
