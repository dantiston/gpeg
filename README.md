# gpep
Search with Parsing Expressions: global/parsing expressions/print

A utility for searching streams using [pe](https://github.com/goodmami/pe/tree/main)-style
Parsing Expression Grammars (PEGs).

# Examples
```
$ cat digits.tsv
123
abc
456
$ gpep '[0-9]+' <digits.tsv # find lines containing only digits
123
456
$ cat trees.tsv
()
(()
(())
(()())
$ gpep "top <- '(' top* ')'" <trees.txt # verify parentheses
()
(())
(()())
$ cat mydata.jsonl
# Comments aren't spec
['hello world']
- Neither is this
$ gpep json.grm <mydata.jsonl # use more complicated grammars
['hello world']
$ cat home.html
<html>
    /* I don't care about comments */
    <span><a href="github.com">github</a></span>
</html>
$ gpep html_links.grm <home.html # extract links from HTML
github.com
```