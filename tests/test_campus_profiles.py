"""Compile small documents to check campus layouts and physical page counting.

Run with: python3 -m unittest discover -s tests -v
Requires pdflatex; compilation products are written to temporary directories.
"""
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('pdflatex'), 'pdflatex is required')
class CampusProfilesTest(unittest.TestCase):
    def compile_document(self, campus, body, setup='', finish=True, success=True):
        source = r'''
\documentclass[11pt,a4paper]{report}
\usepackage[left=35mm,right=25mm,top=35mm,bottom=35mm]{geometry}
\title{An extended paper}
\usepackage{fiiw-campus}
\usepackage{hyperref}
\makeatletter
\def\@campus{CAMPUS}
\newcommand{\layoutcheck}[1]{%
  \typeout{LAYOUT #1: \if@twocolumn 2\else 1\fi}%
  \typeout{METRICS #1: \f@size,\the\textwidth,\the\columnsep,\the\baselineskip}%
  \typeout{HEADINGS #1: \ifx\chapter\originalchapter report\else paper\fi}}
\makeatother
SETUP
\begin{document}
\let\originalchapter\chapter
\pagenumbering{roman}
\layoutcheck{front}
Front matter excluded from the count.
\thesiscontent
\layoutcheck{content}
BODY
FINISH
\end{document}
'''
        for key, value in {
            'CAMPUS': campus,
            'SETUP': setup,
            'BODY': body,
            'FINISH': (r'\finishthesiscontent\layoutcheck{back}'
                       r'\appendix\chapter{Appendix}Excluded appendix.'
                       if finish else ''),
        }.items():
            source = source.replace(key, value)
        with tempfile.TemporaryDirectory(prefix='fiiw-campus-') as directory:
            path = Path(directory)
            (path / 'test.tex').write_text(source)
            env = dict(os.environ, TEXINPUTS=str(ROOT) + os.pathsep
                       + os.environ.get('TEXINPUTS', ''))
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'test.tex'],
                cwd=path, env=env, capture_output=True, text=True, timeout=30)
            log = (path / 'test.log').read_text()
        if success:
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn('LAYOUT front: 1', log)
            if finish:
                self.assertIn('LAYOUT back: 1', log)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return log

    def assert_count(self, log, pages, limit, exceeded=False):
        self.assertIn(f'FIIW content pages: {pages}; limit: {limit}', log)
        self.assertEqual('Content page limit exceeded' in log, exceeded)
        self.assertEqual(log.count('FIIW content pages:'), 1)

    def test_all_campus_language_variants(self):
        for campus in ('gent', 'ghenteng', 'denayer', 'denayereng', 'geel',
                       'geeleng', 'groept', 'groupteng', 'brugge', 'brugeseng'):
            with self.subTest(campus=campus):
                ghent = campus in ('gent', 'ghenteng')
                log = self.compile_document(campus, r'Content.\clearpage More content.')
                self.assertIn(f'LAYOUT content: {2 if ghent else 1}', log)
                self.assert_count(log, 2, 20 if ghent else 0)

    def test_ghent_limit_boundary_both_languages(self):
        for campus in ('gent', 'ghenteng'):
            for pages in (20, 21):
                with self.subTest(campus=campus, pages=pages):
                    log = self.compile_document(campus, r'Content.\clearpage ' * pages)
                    self.assert_count(log, pages, 20, exceeded=pages > 20)

    def test_two_columns_count_as_one_page(self):
        log = self.compile_document('gent', r'Left column.\newpage Right column.')
        self.assert_count(log, 1, 20)

    def test_float_only_page_is_counted(self):
        log = self.compile_document('gent', r'''
Content.
\begin{figure*}[p]\centering\rule{10cm}{5cm}\caption{Pending float}\end{figure*}
''')
        self.assert_count(log, 2, 20)

    def test_numbering_reset_does_not_reset_count(self):
        log = self.compile_document('ghenteng',
                                    r'One.\clearpage\setcounter{page}{1}Two.')
        self.assert_count(log, 2, 20)

    def test_override_and_disabled_limit(self):
        for limit in (1, 0):
            with self.subTest(limit=limit):
                log = self.compile_document(
                    'gent', r'One.\clearpage Two.',
                    setup=r'\campussetup{columns=1,max-content-pages=' + str(limit) + '}')
                self.assertIn('LAYOUT content: 1', log)
                self.assert_count(log, 2, limit, exceeded=limit == 1)

    def test_end_document_fallback(self):
        log = self.compile_document('ghenteng', 'Final page.', finish=False)
        self.assert_count(log, 1, 20)

    def test_profile_can_be_reconfigured(self):
        log = self.compile_document(
            'geel', 'Content.',
            setup=r'\DeclareCampusProfile{geel,geeleng}{columns=2,max-content-pages=15}')
        self.assertIn('LAYOUT content: 2', log)
        self.assert_count(log, 1, 15)

    def test_paper_headings_flow_and_report_style_returns(self):
        for campus in ('gent', 'ghenteng', 'geeleng'):
            with self.subTest(campus=campus):
                log = self.compile_document(campus, r'''
\chapter[Short title]{Introduction}\label{intro}First paragraph.
\section{Approach}Some details.
\chapter{Results}\label{results}Second paragraph.
\chapter*{Discussion}An unnumbered heading.
See Sections~\ref{intro} and~\ref{results}.
''')
                paper = campus != 'geeleng'
                self.assert_count(log, 1 if paper else 3, 20 if paper else 0)
                self.assertIn('HEADINGS content: ' + ('paper' if paper else 'report'), log)
                self.assertIn('HEADINGS back: report', log)
                metrics = dict(re.findall(r'METRICS (\w+): ([^\n]+)', log))
                self.assertEqual(metrics['front'], metrics['back'])
                if paper:
                    self.assertTrue(metrics['content'].startswith('10,'))
                    self.assertTrue(metrics['content'].endswith(',12.0pt'))
                    self.assertNotEqual(metrics['front'], metrics['content'])
                else:
                    self.assertEqual(metrics['front'], metrics['content'])

    def test_paper_layout_can_be_disabled(self):
        log = self.compile_document('gent', r'\chapter{One}Text.\chapter{Two}Text.',
                                    setup=r'\campussetup{layout=report}')
        self.assert_count(log, 2, 20)
        self.assertIn('HEADINGS content: report', log)

    def test_invalid_configuration(self):
        for campus, setup, message in (
            ('unknown', '', 'Unknown campus'),
            ('gent', r'\campussetup{layout=unknown}', 'Layout must be paper or report'),
            ('gent', r'\campussetup{columns=3}', 'Columns must be 1 or 2'),
            ('gent', r'\campussetup{max-content-pages=-1}', 'must be nonnegative'),
        ):
            with self.subTest(campus=campus, setup=setup):
                log = self.compile_document(campus, 'Content.', setup=setup, success=False)
                self.assertIn(message, log)


if __name__ == '__main__':
    unittest.main()
