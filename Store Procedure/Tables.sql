-- USER_DETAILS TABLE --

CREATE TABLE USER_DETAILS (USER_ID INT PRIMARY KEY,USER_NAME VARCHAR(20) NOT NULL,
EMAIL VARCHAR(MAX),PASSWORD VARCHAR(20) NOT NULL,CREATED_DATE DATETIME,MODIFIED_DATE DATETIME)


INSERT INTO USER_DETAILS (USER_ID,USER_NAME,EMAIL,PASSWORD,CREATED_DATE,MODIFIED_DATE)
VALUES('111','KOKILA','KOK@GMAIL.COM','ADFST123',GETDATE(),GETDATE());
INSERT INTO USER_DETAILS (USER_ID,USER_NAME,EMAIL,PASSWORD,CREATED_DATE,MODIFIED_DATE)
VALUES('112','PRIYA','PRI@GMAIL.COM','HDWYYG567',GETDATE(),GETDATE());

SELECT * FROM USER_DETAILS



---------------------------------------BANKACCOUNT TABLE----------------------------------

CREATE TABLE BANK_ACCOUNT(USER_ID INT,
                      BNKACT_ID INT NOT NULL,
                      ACCOUNT_NUMBER INT NOT NULL, 
                      NAME VARCHAR(50) NOT NULL, 
                      BANK VARCHAR(50) NOT NULL,
                      IFSC_CODE VARCHAR(10) NOT NULL,
                      BALANCE INT NOT NULL,
                      CREATED_DATE DATETIME,
                      MODIFIED_DATE DATETIME,
                      FOREIGN KEY(USER_ID) REFERENCES USER_DETAILS(USER_ID))
SELECT * FROM BANK_ACCOUNT

---------------------------WALLET TABLE------------------------------------------------------

CREATE TABLE WALLET_ACCOUNT(USER_ID INT,
					  NAME VARCHAR(30) NOT NULL,
                      AMOUNT INT NOT NULL,
                      CREATED_DATE DATETIME,
                      MODIFIED_DATE DATETIME,
                      FOREIGN KEY(USER_ID) REFERENCES USER_DETAILS(USER_ID))
SELECT * FROM WALLET_ACCOUNT
