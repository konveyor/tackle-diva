CREATE TABLE PRODUCTS 
( 
  PRODUCTID  DECIMAL NOT NULL, 
  PRODUCTNAME  VARCHAR(40) NOT NULL, 
  SUPPLIERID  DECIMAL, 
  CATEGORYID  DECIMAL, 
  QUANTITYPERUNIT  VARCHAR(20), 
  UNITPRICE  DECIMAL, 
  UNITSINSTOCK  DECIMAL, 
  UNITSONORDER  DECIMAL, 
  REORDERLEVEL  DECIMAL, 
  DISCONTINUED  DECIMAL(1) NOT NULL, 
CONSTRAINT PK_PRODUCTS 
  PRIMARY KEY (PRODUCTID), 
CONSTRAINT CK_PRODUCTS_UNITPRICE   CHECK ((UNITPRICE >= 0)), 
CONSTRAINT CK_REORDERLEVEL   CHECK ((REORDERLEVEL >= 0)), 
CONSTRAINT CK_UNITSINSTOCK   CHECK ((UNITSINSTOCK >= 0)), 
CONSTRAINT CK_UNITSONORDER   CHECK ((UNITSONORDER >= 0)), 
CONSTRAINT FK_PRODUCTS_CATEGORIES FOREIGN KEY (CATEGORYID) REFERENCES CATEGORIES(CATEGORYID), 
CONSTRAINT FK_PRODUCTS_SUPPLIERS FOREIGN KEY (SUPPLIERID) REFERENCES SUPPLIERS(SUPPLIERID)
) 
;