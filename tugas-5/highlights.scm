; Keyword DSL filter
["and" "or" "not" "in" "contains"] @keyword

; Operator perbandingan
["=" "!=" ">" "<" ">=" "<="] @operator

; Nilai
(string) @string
(number) @number
(boolean) @constant.builtin

; Nama field di sebelah kiri perbandingan
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)

; Tanda kurung
["(" ")"] @punctuation.bracket
[","] @punctuation.delimiter
