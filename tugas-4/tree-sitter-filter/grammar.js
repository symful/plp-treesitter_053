module.exports = grammar({
  name: 'filter',

  extras: $ => [/\s/],

  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,
      $.and_expression,
    ),

    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='),
      $._value,
    ),

    and_expression: $ => seq($._expr, 'and', $._expr),

    _value: $ => choice($.string, $.number),

    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});
