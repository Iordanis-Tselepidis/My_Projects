------ CREATION OF STAGING AREA -------

USE master
GO
IF EXISTS (SELECT * FROM sysdatabases WHERE NAME = 'My_ChinookStaging')
BEGIN
	ALTER DATABASE My_ChinookStaging 
	SET SINGLE_USER 
	WITH ROLLBACK IMMEDIATE;
		DROP DATABASE My_ChinookStaging
END
GO


CREATE DATABASE My_ChinookStaging
USE My_ChinookStaging;
GO


-- Creatte and populate Customer Table in Staging
SELECT c.CustomerId, c.FirstName AS CustFirstName, c.LastName AS CustLastName,
	c.Company, c.City AS CustCity, c.State AS CustState, c.Country AS CustCountry, c.Email AS CustEmail,
	CONCAT(e.FirstName, ' ', e.LastName) AS SuppRepFullName
INTO Customer
FROM My_Chinook.dbo.Customer AS c
JOIN My_Chinook.dbo.Employee AS e ON e.EmployeeId = c.SupportRepId;
GO

-- Create and pupolate Invoice Table in Staging 
SELECT i.InvoiceId, i.CustomerId, i.InvoiceDate, il.TrackId, il.UnitPrice, il.Quantity
INTO Invoice
FROM My_Chinook.dbo.Invoice AS i 
JOIN My_Chinook.dbo.InvoiceLine AS il ON i.InvoiceId = il.InvoiceId;
GO

-- Create PlaylistCount View (to use it in the Track Table later)
CREATE VIEW PlaylistCount 
AS
SELECT t.TrackId, COUNT(pt.PlaylistId) AS PlaylistCount, STRING_AGG(p.Name, ', ') AS PlaylistNames
FROM My_Chinook.dbo.Track t
JOIN My_Chinook.dbo.PlaylistTrack AS pt ON pt.TrackId = t.TrackId
JOIN My_Chinook.dbo.Playlist AS p ON p.PlaylistId = pt.PlaylistId
GROUP BY t.TrackId;
GO

-- Create and populate Track Table in Staging
SELECT t.TrackId, t.Name AS TrackName, ar.Name AS ArtistName, 
	al.Title AS AlbumTitle, g.name AS GenreName,
	plc.PlaylistCount, plc.PlaylistNames
INTO Track
FROM My_Chinook.dbo.Track AS t 
JOIN My_Chinook.dbo.Album AS al ON al.AlbumId = t.AlbumId
JOIN My_Chinook.dbo.Artist AS ar ON ar.ArtistId	= al.ArtistId
JOIN My_Chinook.dbo.Genre AS g ON g.GenreId = t.GenreId
JOIN PlaylistCount AS plc ON plc.TrackId = t.TrackId;
GO

-- Create and populate BillingLocation Table in Staging
SELECT InvoiceId, BillingCity, BillingState, BillingCountry
INTO InvoiceLocation
FROM My_Chinook.dbo.Invoice;
GO
