-- Categories Table
CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(255) NOT NULL
);

-- DataTypes Table
CREATE TABLE DataTypes (
    DataTypeID INT AUTO_INCREMENT PRIMARY KEY,
    TypeName VARCHAR(255) NOT NULL
);

-- Languages Table
CREATE TABLE Languages (
    LanguageID INT AUTO_INCREMENT PRIMARY KEY,
    LanguageName VARCHAR(255) NOT NULL
);

-- DataFormats Table
CREATE TABLE DataFormats (
    DataFormatID INT AUTO_INCREMENT PRIMARY KEY,
    FormatName VARCHAR(255) NOT NULL
);

-- Resources Table
CREATE TABLE Resources (
    ResourceID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    URL TEXT NOT NULL,
    UsabilityDescription TEXT NOT NULL
);

-- ResourceCategories Table (Many-to-Many Relationship)
CREATE TABLE ResourceCategories (
    ResourceID INT,
    CategoryID INT,
    PRIMARY KEY (ResourceID, CategoryID),
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- ResourceDataTypes Table (Many-to-Many Relationship)
CREATE TABLE ResourceDataTypes (
    ResourceID INT,
    DataTypeID INT,
    PRIMARY KEY (ResourceID, DataTypeID),
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (DataTypeID) REFERENCES DataTypes(DataTypeID)
);

-- ResourceLanguages Table (Many-to-Many Relationship)
CREATE TABLE ResourceLanguages (
    ResourceID INT,
    LanguageID INT,
    PRIMARY KEY (ResourceID, LanguageID),
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (LanguageID) REFERENCES Languages(LanguageID)
);

-- ResourceDataFormats Table (Many-to-Many Relationship)
CREATE TABLE ResourceDataFormats (
    ResourceID INT,
    DataFormatID INT,
    PRIMARY KEY (ResourceID, DataFormatID),
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (DataFormatID) REFERENCES DataFormats(DataFormatID)
);

-- Applications Table
CREATE TABLE Applications (
    ApplicationID INT AUTO_INCREMENT PRIMARY KEY,
    ApplicationName VARCHAR(255) NOT NULL,
    Description TEXT
);

-- ResourceApplications Table (Many-to-Many Relationship)
CREATE TABLE ResourceApplications (
    ResourceID INT,
    ApplicationID INT,
    PRIMARY KEY (ResourceID, ApplicationID),
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (ApplicationID) REFERENCES Applications(ApplicationID)
);