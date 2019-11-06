## regex to nfa
### Thompsonʼs Construction
#### key idea
* Key idea
  * For each symbol & each operator, we have an NFA pattern
  * Join them with e moves in precedence order & adjust final states
* Precedence in REs:  ```*+?()|```
  1. Parentheses ()
  2. ```*+?```
  3. Concatenation  ab
  4. Alternation  a|b   

* ε-NFA
  * ε边存在的最大的理由：我们可以通过使用ε边来给出一个简洁的算法把一个正则表达式转换成ε-NFA  by vczh
