-- constraint clause in create table.
-- Check if the constraint clause is parsed as a constraint, but the column definition.
-- "constraint" is keyword, so if we allow keywords as a column name,
-- out_of_line constraint rule conflicts with column_definition rule.
CREATE TABLE ORDERDETAILS (
    ORDERID DECIMAL NOT NULL,
    PRODUCTID DECIMAL NOT NULL,
    UNITPRICE DECIMAL NOT NULL,
    QUANTITY DECIMAL NOT NULL,
    DISCOUNT DECIMAL NOT NULL,
    CONSTRAINT FK_ORDERDETAILS_ORDERS FOREIGN KEY (ORDERID) REFERENCES ORDERS(ORDERID),
    CONSTRAINT FK_ORDERDETAILS_PRODUCTS FOREIGN KEY (PRODUCTID) REFERENCES PRODUCTS(PRODUCTID)
);