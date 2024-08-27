CREATE TABLE Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    company TEXT NOT NULL,
    industry TEXT NOT NULL,
    position TEXT NOT NULL,
    profileUrl TEXT NOT NULL,
    UNIQUE(firstName, lastName, profileUrl) --ensures unique users without having to check in upload
);

CREATE TABLE Posts (
    postID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    content TEXT,
    contentFormat TEXT,
    postUrl TEXT NOT NULL,
    imgUrl TEXT,
    likeCount INTEGER NOT NULL,
    commentCount INTEGER NOT NULL,
    repostCount INTEGER NOT NULL,
    sharedPostUrl TEXT,
    isRepost BOOLEAN DEFAULT 0,
    videoUrl TEXT,
    sharedJobUrl TEXT,
    articleTitle TEXT,
    articleSubtitle TEXT,
    articleReadingDuration INTEGER,
    articleCoverUrl TEXT,
    eventUrl TEXT,
    eventTitle TEXT,
    yearOfPost INTEGER NOT NULL,
    monthOfPost VARCHAR(10) NOT NULL,
    dayOfPost INTEGER NOT NULL,
    dayOfWeek VARCHAR(10) NOT NULL,
    militaryHour VARCHAR(10) NOT NULL,
    documentTitle TEXT,
    documentPageCount INTEGER,
    thoughtLeadership BOOLEAN DEFAULT 0,
    totalEngagement INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Engagements (
    reactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    postID INTEGER,
    postContent TEXT,
    contentFormat TEXT,
    postUrl TEXT NOT NULL,
    imgUrl TEXT,
    likeCount INTEGER NOT NULL,
    commentCount INTEGER NOT NULL,
    repostCount INTEGER NOT NULL,
    commentContent TEXT,
    commentUrl TEXT,
    sharedPostUrl TEXT,
    isComment BOOLEAN DEFAULT 0,
    reactionType TEXT NOT NULL,
    videoUrl TEXT,
    sharedJobUrl TEXT,
    articleTitle TEXT,
    articleSubtitle TEXT,
    articleReadingDuration INTEGER,
    articleCoverUrl TEXT,
    eventUrl TEXT,
    eventTitle TEXT,
    yearOfPost INTEGER NOT NULL,
    monthOfPost VARCHAR(10) NOT NULL,
    dayOfPost INTEGER NOT NULL,
    dayOfWeek VARCHAR(10) NOT NULL,
    militaryHour VARCHAR(10) NOT NULL,
    documentTitle TEXT,
    documentPageCount INTEGER,
    thoughtLeadership BOOLEAN DEFAULT 0,
    totalEngagement INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Themes (
    themeID INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT UNIQUE NOT NULL
);

CREATE TABLE PostThemes (
    postID INTEGER NOT NULL,
    themeID INTEGER NOT NULL,
    FOREIGN KEY (postID) REFERENCES Posts(postID) ON DELETE CASCADE,
    FOREIGN KEY (themeID) REFERENCES Themes(themeID) ON DELETE CASCADE,
    PRIMARY KEY (postID, themeID)
);

CREATE TABLE EngagementThemes (
    engagementID INTEGER NOT NULL,
    themeID INTEGER NOT NULL,
    FOREIGN KEY (engagementID) REFERENCES Engagements(reactionID) ON DELETE CASCADE,
    FOREIGN KEY (themeID) REFERENCES Themes(themeID) ON DELETE CASCADE,
    PRIMARY KEY (engagementID, themeID)
);

CREATE TABLE Insights (
    insightID INTEGER PRIMARY KEY AUTOINCREMENT, 
    insightName TEXT NOT NULL,
    insightDetails TEXT NOT NULL,
    monthYear TEXT NOT NULL
);
