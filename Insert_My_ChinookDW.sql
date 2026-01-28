--------- LOAD DATA IN THE WAREHOUSE ---------

USE My_ChinookDW;
GO

-- Load DimCustomer 
INSERT INTO DimCustomer (CustomerId, CustomerName, Company, CustomerCity, CustomerState,
	CustomerCountry, CustomerEmail, SupportRepFullName)
	(SELECT CustomerId,
		CONCAT(CustFirstName, ' ', CustLastName),
		Company,
		CustCity,
		CustState,
		CustCountry,
		CustEmail,
		SuppRepFullName
	FROM My_ChinookStaging.dbo.Customer);


-- Load DimTrack
INSERT INTO DimTrack (TrackId, TrackName, Artist, AlbumTitle, Genre, PlaylistCount, PlaylistNameList)
	(SELECT TrackId,
		TrackName,
		ArtistName,
		AlbumTitle,
		GenreName,
		PlaylistCount,
		PlaylistNames
	FROM My_ChinookStaging.dbo.Track);


-- Load DimLocation 
INSERT INTO DimLocation (InvoiceId, BillingCity, BillingState, BillingCountry)
	(SELECT InvoiceId,
		BillingCity,
		BillingState,
		BillingCountry
	FROM My_ChinookStaging.dbo.InvoiceLocation);


-- Load DimDate
INSERT INTO DimDate (DateKey, FullDate, Day, Month, MonthName, Quarter, Year)
SELECT DISTINCT
    CAST(FORMAT(InvoiceDate,'yyyyMMdd') AS INT) AS DateKey,
    CAST(InvoiceDate AS DATE) AS FullDate,
    DATEPART(DAY, InvoiceDate) AS Day,
    DATEPART(MONTH, InvoiceDate) AS Month,
    DATENAME(MONTH, InvoiceDate) AS MonthName,
    DATEPART(QUARTER, InvoiceDate) AS Quarter,
    DATEPART(YEAR, InvoiceDate) AS Year
FROM My_ChinookStaging.dbo.Invoice;


-- Load FactSales
INSERT INTO FactSales (TrackKey, CustomerKey, SaleDate, LocationKey, InvoiceId, UnitPrice, Quantity, Total)
	(SELECT dt.TrackKey,
		dc.CustomerKey,
		dd.DateKey,
		dl.LocationKey,
		i.InvoiceId,
		i.UnitPrice,
		i.Quantity,
		i.UnitPrice * i.Quantity
	FROM My_ChinookStaging.dbo.Invoice AS i 
	JOIN DimTrack AS dt ON dt.TrackId = i.TrackId
	JOIN DimCustomer AS dc ON dc.CustomerId = i.CustomerId
	JOIN DimLocation AS dl ON dl.InvoiceId = i.InvoiceId
	JOIN DimDate AS dd ON CAST(FORMAT(i.InvoiceDate,'yyyyMMdd') AS INT) = dd.DateKey);
	

