// Define a grammar called Hello
grammar Hello;
r  : 'hello' ID          // match keyword hello followed by an identifier
   | expr ;

expr : expr '*' expr
     | expr '+' expr
     | INT ;

ID : [a-z]+ ;             // match lower-case identifiers
INT: [1-9][0-9]* ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
