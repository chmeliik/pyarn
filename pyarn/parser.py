"""
Copyright (C) 2020  Red Hat, Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pyarn.lexer import tokens  # noqa: F401


def p_blocks_single(p):
    """blocks : block"""
    if isinstance(p[1], str):
        # comment
        p[0] = {'comments': [p[1]], 'data': {}}
    else:
        p[0] = {'comments': [], 'data': p[1]}


def p_blocks(p):
    """blocks : blocks block"""
    if isinstance(p[2], str):
        # comment
        p[1]['comments'].append(p[2])
    else:
        p[1]['data'].update(p[2])

    p[0] = p[1]


def p_block_title(p):
    """block : title members"""
    # TODO: do we want to separate titles like "foo, bar"?
    # have in mind they may also be like "foo || bar, biz"
    p[0] = {p[1]: p[2]}


def p_block_pair(p):
    """block : pair"""
    p[0] = p[1]


def p_block_comment(p):
    """block : comment"""
    p[0] = p[1]


def p_title(p):
    """title : STRING COLON NEWLINE INDENT
             | list COLON NEWLINE INDENT"""
    p[0] = p[1]


def p_list(p):
    """list : STRING COMMA STRING
            | list COMMA STRING"""
    p[0] = ', '.join([p[1], p[3]])


def p_members(p):
    """members : pair"""
    p[0] = p[1]


def p_members_multiple_pairs(p):
    """members : pair INDENT members"""
    p[0] = {**p[1], **p[3]}


def p_members_nested_title(p):
    """members : title members"""
    p[0] = {p[1]: p[2]}


def p_pair(p):
    """pair : STRING STRING NEWLINE"""
    p[0] = {p[1]: p[2]}


def p_pair_colon(p):
    """pair : STRING COLON STRING NEWLINE"""
    p[0] = {p[1]: p[3]}


# TODO: handle indented comments
# this generates a parser conflict if not properly handled inside a block
def p_comment(p):
    """comment : COMMENT NEWLINE"""
    p[0] = p[1]


def p_error(p):
    raise ValueError(f'error parsing {p}')
