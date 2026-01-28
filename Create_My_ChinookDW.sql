-------- DESIGN OF THE CHINOOK WAREHOUSE DATABASE --------

USE master
GO
IF exists (SELECT * FROM sysdatabases WHERE name='My_ChinookDW')
		BEGIN
	ALTER DATABASE My_ChinookDW 
	SET SINGLE_USER 
	WITH ROLLBACK IMMEDIATE;
		DROP DATABASE My_ChinookDW

END
GO


CREATE DATABASE My_ChinookDW;
USE My_ChinookDW;


-- Create DimCustomer Table
CREATE TABLE DimCustomer (
	CustomerKey INT IDENTITY(1,1) NOT NULL,
	CustomerId INT NOT NULL,
	CustomerName VARCHAR(100) NOT NULL, -- concatenate CustFirstName + CustLastName
	Company VARCHAR(100),
	CustomerCity VARCHAR(100) NOT NULL,
	CustomerState VARCHAR(100),
	CustomerCountry VARCHAR(100) NOT NULL,
	CustomerEmail VARCHAR(100) NOT NULL,
	SupportRepFullName VARCHAR(100) NOT NULL, -- concatenate EmpFirstName + EmpLastName
	RowIsCurrent INT NOT NULL DEFAULT 1,
	RowStartDate DATE NOT NULL DEFAULT  '1899-12-31',
	RowEndDate DATE NOT NULL DEFAULT  '9999-12-31',
	RowChangeReason VARCHAR(100) NULL,

	CONSTRAINT PK_DimCustomer PRIMARY KEY CLUSTERED (CustomerKey)
);


-- Create DimTrack Table
CREATE TABLE DimTrack (
	TrackKey INT IDENTITY(1,1) NOT NULL,
	TrackId INT NOT NULL,
	TrackName VARCHAR(MAX) NOT NULL,
	Artist VARCHAR(100) NOT NULL,
	AlbumTitle VARCHAR(100) NOT NULL,
	Genre VARCHAR(100) NOT NULL,
	PlaylistCount INT NOT NULL,
	PlaylistNameList VARCHAR(200) NOT NULL,
	RowIsCurrent INT NOT NULL DEFAULT 1,
	RowStartDate DATE NOT NULL DEFAULT  '1899-12-31',
	RowEndDate DATE NOT NULL DEFAULT  '9999-12-31',
	RowChangeReason VARCHAR(100) NULL,

	CONSTRAINT PK_DimTrack PRIMARY KEY CLUSTERED (TrackKey)
);


-- Create DimDate Table
CREATE TABLE DimDate (
	DateKey INT PRIMARY KEY,  -- of the form 'YYYYMMDD'
	FullDate DATE NOT NULL,
	Day INT NOT NULL,
	Month INT NOT NULL,
	MonthName VARCHAR(100) NOT NULL,
	Quarter INT NOT NULL,
	Year INT NOT NULL
);


-- Create DimLocation Table
CREATE TABLE DimLocation (
	LocationKey INT IDENTITY(1,1),
	InvoiceId INT NOT NULL,
	BillingCity VARCHAR(100) NOT NULL,
	BillingState VARCHAR(100),
	BillingCountry VARCHAR(100) NOT NULL,

	CONSTRAINT PK_DimLocation PRIMARY KEY CLUSTERED (LocationKey)
);


-- Create FactSales Table
CREATE TABLE FactSales (
	TrackKey INT NOT NULL,
	CustomerKey INT NOT NULL,
	SaleDate INT NOT NULL,
	LocationKey INT NOT NULL,
	InvoiceId INT NOT NULL,
	UnitPrice NUMERIC(10,2) NOT NULL,
	Quantity INT NOT NULL,
	Total NUMERIC(10,2) NOT NULL -- UnitPrice * Quantity
);


-------------- Creation of Foreign Keys ------------------

-- FactSales / DimTrack 
ALTER TABLE FactSales
ADD CONSTRAINT FK_FactSales_DimTrack
FOREIGN KEY (TrackKey)
REFERENCES DimTrack(TrackKey);

-- FactSales / DimCustomer 
ALTER TABLE FactSales
ADD CONSTRAINT FK_FactSales_DimCustomer
FOREIGN KEY (CustomerKey)
REFERENCES DimCustomer(CustomerKey);

-- FactSales / DimDate 
ALTER TABLE FactSales
ADD CONSTRAINT FK_FactSales_DimDate
FOREIGN KEY (SaleDate)
REFERENCES DimDate(DateKey);

-- FactSales / DimLocation
ALTER TABLE FactSales
ADD CONSTRAINT FK_FactSales_DimLocation
FOREIGN KEY (LocationKey)
REFERENCES DimLocation(LocationKey);