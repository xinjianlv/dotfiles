# coding: utf-8
#
# Copyright (C) 2013  Google Inc.
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # noqa

import contextlib
from nose.tools import eq_, ok_
from mock import patch

from ycm.test_utils import MockVimModule
vim_mock = MockVimModule()
from ycm import base


@contextlib.contextmanager
def MockCurrentFiletypes( filetypes = [''] ):
  with patch( 'ycm.vimsupport.CurrentFiletypes', return_value = filetypes ):
    yield


@contextlib.contextmanager
def MockCurrentColumnAndLineContents( column, line_contents ):
  with patch( 'ycm.vimsupport.CurrentColumn', return_value = column ):
    with patch( 'ycm.vimsupport.CurrentLineContents',
                return_value = line_contents ):
      yield


@contextlib.contextmanager
def MockTextAfterCursor( text ):
  with patch( 'ycm.vimsupport.TextAfterCursor', return_value = text ):
    yield


def AdjustCandidateInsertionText_Basic_test():
  with MockTextAfterCursor( 'bar' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar' ] ) )


def AdjustCandidateInsertionText_ParenInTextAfterCursor_test():
  with MockTextAfterCursor( 'bar(zoo' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar' ] ) )


def AdjustCandidateInsertionText_PlusInTextAfterCursor_test():
  with MockTextAfterCursor( 'bar+zoo' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar' ] ) )


def AdjustCandidateInsertionText_WhitespaceInTextAfterCursor_test():
  with MockTextAfterCursor( 'bar zoo' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar' ] ) )


def AdjustCandidateInsertionText_MoreThanWordMatchingAfterCursor_test():
  with MockTextAfterCursor( 'bar.h' ):
    eq_( [ { 'abbr': 'foobar.h', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar.h' ] ) )

  with MockTextAfterCursor( 'bar(zoo' ):
    eq_( [ { 'abbr': 'foobar(zoo', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText( [ 'foobar(zoo' ] ) )


def AdjustCandidateInsertionText_NotSuffix_test():
  with MockTextAfterCursor( 'bar' ):
    eq_( [ { 'abbr': 'foofoo', 'word': 'foofoo' } ],
         base.AdjustCandidateInsertionText( [ 'foofoo' ] ) )


def AdjustCandidateInsertionText_NothingAfterCursor_test():
  with MockTextAfterCursor( '' ):
    eq_( [ 'foofoo',
           'zobar' ],
         base.AdjustCandidateInsertionText( [ 'foofoo',
                                              'zobar' ] ) )


def AdjustCandidateInsertionText_MultipleStrings_test():
  with MockTextAfterCursor( 'bar' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' },
           { 'abbr': 'zobar', 'word': 'zo' },
           { 'abbr': 'qbar', 'word': 'q' },
           { 'abbr': 'bar', 'word': '' }, ],
         base.AdjustCandidateInsertionText( [ 'foobar',
                                              'zobar',
                                              'qbar',
                                              'bar' ] ) )


def AdjustCandidateInsertionText_DictInput_test():
  with MockTextAfterCursor( 'bar' ):
    eq_( [ { 'abbr': 'foobar', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText(
           [ { 'word': 'foobar' } ] ) )


def AdjustCandidateInsertionText_DontTouchAbbr_test():
  with MockTextAfterCursor( 'bar' ):
    eq_( [ { 'abbr': '1234', 'word': 'foo' } ],
         base.AdjustCandidateInsertionText(
           [ { 'abbr': '1234', 'word': 'foobar' } ] ) )


def OverlapLength_Basic_test():
  eq_( 3, base.OverlapLength( 'foo bar', 'bar zoo' ) )
  eq_( 3, base.OverlapLength( 'foobar', 'barzoo' ) )


def OverlapLength_BasicWithUnicode_test():
  eq_( 3, base.OverlapLength( u'bar fäö', u'fäö bar' ) )
  eq_( 3, base.OverlapLength( u'zoofäö', u'fäözoo' ) )


def OverlapLength_OneCharOverlap_test():
  eq_( 1, base.OverlapLength( 'foo b', 'b zoo' ) )


def OverlapLength_SameStrings_test():
  eq_( 6, base.OverlapLength( 'foobar', 'foobar' ) )


def OverlapLength_Substring_test():
  eq_( 6, base.OverlapLength( 'foobar', 'foobarzoo' ) )
  eq_( 6, base.OverlapLength( 'zoofoobar', 'foobar' ) )


def OverlapLength_LongestOverlap_test():
  eq_( 7, base.OverlapLength( 'bar foo foo', 'foo foo bar' ) )


def OverlapLength_EmptyInput_test():
  eq_( 0, base.OverlapLength( '', 'goobar' ) )
  eq_( 0, base.OverlapLength( 'foobar', '' ) )
  eq_( 0, base.OverlapLength( '', '' ) )


def OverlapLength_NoOverlap_test():
  eq_( 0, base.OverlapLength( 'foobar', 'goobar' ) )
  eq_( 0, base.OverlapLength( 'foobar', '(^($@#$#@' ) )
  eq_( 0, base.OverlapLength( 'foo bar zoo', 'foo zoo bar' ) )


def LastEnteredCharIsIdentifierChar_Basic_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 3, 'abc' ):
      ok_( base.LastEnteredCharIsIdentifierChar() )

    with MockCurrentColumnAndLineContents( 2, 'abc' ):
      ok_( base.LastEnteredCharIsIdentifierChar() )

    with MockCurrentColumnAndLineContents( 1, 'abc' ):
      ok_( base.LastEnteredCharIsIdentifierChar() )


def LastEnteredCharIsIdentifierChar_FiletypeHtml_test():
  with MockCurrentFiletypes( ['html'] ):
    with MockCurrentColumnAndLineContents( 3, 'ab-' ):
      ok_( base.LastEnteredCharIsIdentifierChar() )


def LastEnteredCharIsIdentifierChar_ColumnIsZero_test():
  with MockCurrentColumnAndLineContents( 0, 'abc' ):
    ok_( not base.LastEnteredCharIsIdentifierChar() )


def LastEnteredCharIsIdentifierChar_LineEmpty_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 3, '' ):
      ok_( not base.LastEnteredCharIsIdentifierChar() )

    with MockCurrentColumnAndLineContents( 0, '' ):
      ok_( not base.LastEnteredCharIsIdentifierChar() )


def LastEnteredCharIsIdentifierChar_NotIdentChar_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 3, 'ab;' ):
      ok_( not base.LastEnteredCharIsIdentifierChar() )

    with MockCurrentColumnAndLineContents( 1, ';' ):
      ok_( not base.LastEnteredCharIsIdentifierChar() )

    with MockCurrentColumnAndLineContents( 3, 'ab-' ):
      ok_( not base.LastEnteredCharIsIdentifierChar() )


def CurrentIdentifierFinished_Basic_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 3, 'ab;' ):
      ok_( base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 2, 'ab;' ):
      ok_( not base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 1, 'ab;' ):
      ok_( not base.CurrentIdentifierFinished() )


def CurrentIdentifierFinished_NothingBeforeColumn_test():
  with MockCurrentColumnAndLineContents( 0, 'ab;' ):
    ok_( base.CurrentIdentifierFinished() )

  with MockCurrentColumnAndLineContents( 0, '' ):
    ok_( base.CurrentIdentifierFinished() )


def CurrentIdentifierFinished_InvalidColumn_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 5, '' ):
      ok_( not base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 5, 'abc' ):
      ok_( not base.CurrentIdentifierFinished() )


def CurrentIdentifierFinished_InMiddleOfLine_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 4, 'bar.zoo' ):
      ok_( base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 4, 'bar(zoo' ):
      ok_( base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 4, 'bar-zoo' ):
      ok_( base.CurrentIdentifierFinished() )


def CurrentIdentifierFinished_Html_test():
  with MockCurrentFiletypes( ['html'] ):
    with MockCurrentColumnAndLineContents( 4, 'bar-zoo' ):
      ok_( not base.CurrentIdentifierFinished() )


def CurrentIdentifierFinished_WhitespaceOnly_test():
  with MockCurrentFiletypes():
    with MockCurrentColumnAndLineContents( 1, '\n' ):
      ok_( base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 3, '\n    ' ):
      ok_( base.CurrentIdentifierFinished() )

    with MockCurrentColumnAndLineContents( 3, '\t\t\t\t' ):
      ok_( base.CurrentIdentifierFinished() )
