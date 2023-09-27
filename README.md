# gpeg
Search with Parsing Expressions: global/parsing expressions/print

A utility for searching streams using [pe](https://github.com/goodmami/pe/tree/main)
style Parsing Expression Grammars (PEGs).

# Examples
```
$ cat digits.tsv
123
abc
456
$ gpeg '[0-9]+' <digits.tsv # find lines containing only digits
123
456
$ cat trees.tsv
()
(()
(())
(()())
$ gpeg 'top <- '(' top* ')'' <trees.txt # verify parentheses
()
(())
(()())
$ cat mydata.jsonl
# Comments aren't spec
['hello world']
- Neither is this
$ gpeg json.grm <mydata.jsonl # use more complicated grammars
['hello world']
```