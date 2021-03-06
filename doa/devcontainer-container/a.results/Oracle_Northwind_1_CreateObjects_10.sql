CREATE TABLE CUSTOMERCUSTOMERDEMO 
( 
  CUSTOMERID  CHAR(5) NOT NULL, 
  CUSTOMERTYPEID  CHAR(10) NOT NULL, 
CONSTRAINT PK_CUSTOMERDEMO 
  PRIMARY KEY (CUSTOMERID, CUSTOMERTYPEID), 
CONSTRAINT FK_CUSTOMERDEMO FOREIGN KEY (CUSTOMERTYPEID) REFERENCES CUSTOMERDEMOGRAPHICS(CUSTOMERTYPEID), 
CONSTRAINT FK_CUSTOMERDEMO_CUSTOMERS FOREIGN KEY (CUSTOMERID) REFERENCES CUSTOMERS(CUSTOMERID)
) 
;