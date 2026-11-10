module.exports = grammar({
  name: 'filter',

  extras: $ => [/\s/],

  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,
      $.in_expression,
      $.and_expression,
      $.or_expression,
      $.not_expression,
      $.parenthesized,
    ),

    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value),
    ),

    in_expression: $ => seq(
      field('field', $.identifier),
      'in',
      field('values', $.value_list),
    ),

    value_list: $ => seq(
      '(',
      $._value,
      repeat(seq(',', $._value)),
      ')',
    ),

    or_expression: $ => prec.left(1, seq(
      field('left', $._expr),
      'or',
      field('right', $._expr),
    )),
    and_expression: $ => prec.left(2, seq(
      field('left', $._expr),
      'and',
      field('right', $._expr),
    )),
    not_expression: $ => prec(3, seq(
      'not',
      field('operand', $._expr),
    )),

    parenthesized: $ => seq('(', $._expr, ')'),

    _value: $ => choice($.string, $.number, $.boolean),

    string: $ => /"[^"]*"/,
    boolean: $ => choice('true', 'false'),
    number: $ => /\d+(\.\d+)?/,
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});
