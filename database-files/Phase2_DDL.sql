-- All subsequent DB commands will be executed in the context of
-- course_companion

CREATE DATABASE IF NOT EXISTS course_companion;
USE course_companion;


-- Table for post tags (hash-tags) that can be applied to posts
CREATE TABLE IF NOT EXISTS tags
(
    `tagId`   INTEGER AUTO_INCREMENT PRIMARY KEY,
    `tagName` VARCHAR(200) NOT NULL UNIQUE
);

-- Table for departments that classes reside in
CREATE TABLE IF NOT EXISTS `department`
(
    `departmentId`   INT AUTO_INCREMENT PRIMARY KEY,
    `description`    TEXT,
    `departmentName` VARCHAR(100) NOT NULL UNIQUE
);

-- Table for courses. Each course is uniquely identified by its course Id and
-- section Id . For example CS32000 (Prof Fontenot section) is a different
-- course from CS3200 (Prof Lebron section)
CREATE TABLE IF NOT EXISTS `courses`
(
    `sectionId`         INT          NOT NULL,
    `courseId`          INT          NOT NULL,
    `courseDescription` TEXT,
    `courseName`        VARCHAR(100) NOT NULL,
    `departmentId`      INT          NOT NULL,
    PRIMARY KEY (`courseId`, `sectionId`),
    -- Create an index on course name so that we can look up courses by specific
    -- course names are faster
    INDEX courseName_Idx (courseName),
    CONSTRAINT fk_course_department FOREIGN KEY (departmentId) REFERENCES department (departmentId)
);

-- Table for our users of our app
CREATE TABLE IF NOT EXISTS `users`
(
    `userId`          INT AUTO_INCREMENT PRIMARY KEY,
    `firstName`       VARCHAR(100)       NOT NULL,
    `lastName`        VARCHAR(100),
    `bio`             TEXT,
    -- All users must have a bday, but it may not be known. For the
    -- cases where it is unknown, we will use null :)
    `birthdate`       DATE,
    `universityEmail` VARCHAR(75) UNIQUE NOT NULL,
    INDEX email_idx (universityEmail)
);

-- Table for posts that users can create. Includes both announcements
-- and regular posts
CREATE TABLE IF NOT EXISTS `posts`
(
    `postId`         INTEGER AUTO_INCREMENT PRIMARY KEY,
    `title`          VARCHAR(75) NOT NULL,
    `content`        TEXT        NOT NULL,
    `createdAt`      DATETIME    NOT NULL,
    `updatedAt`      DATETIME,
    `isAnnouncement` BOOLEAN     NOT NULL,
    `authorId`       INT         NOT NULL,
    `courseId`       INT         NOT NULL,
    `sectionId`      INT         NOT NULL,
    -- Create an index on author Id so that we can look up posts by specific
    -- authors faster
    INDEX authorId_idx (authorId),
    -- Create an index on content so that we can look up posts by specific
    -- content are faster. Index only the first 255 chars of content to improve performance
    INDEX content_Idx (content(255)),
    CONSTRAINT fk_posts_course FOREIGN KEY (courseId, sectionId) REFERENCES courses (courseId, sectionId),
    CONSTRAINT fk_posts_author FOREIGN KEY (authorId) REFERENCES users (userId)
);


-- Table for messages between users (handles both direct and group messages via
-- the user_messages linkage table)
CREATE TABLE IF NOT EXISTS `messages`
(
    `messageId` INT AUTO_INCREMENT PRIMARY KEY,
    `createdAt` DATETIME NOT NULL,
    `updatedAt` DATETIME,
    `content`   TEXT     NOT NULL,
    `authorId`  INT      NOT NULL,
    -- Create an index on content so that we can look up messages by specific
    -- content are faster. Index only the first 255 chars of content to improve performance
    INDEX content_Idx (content(255)),
    CONSTRAINT fk_messages_author FOREIGN KEY (authorId) REFERENCES users (userId)
);


-- Table for the comments applied to posts on our app
CREATE TABLE IF NOT EXISTS `comments`
(
    `commentId`       INT AUTO_INCREMENT PRIMARY KEY,
    `content`         TEXT     NOT NULL,
    `createdAt`       DATETIME NOT NULL,
    `updatedAt`       DATETIME,
    `authorId`        INT      NOT NULL,
    `parentCommentId` INT,
    `postId`          INT      NOT NULL,
    -- Create an index on content so that we can look up comments by specific
    -- content are faster. Index only the first 255 chars of content to improve performance
    INDEX content_Idx (content(255)),
    CONSTRAINT fk_comments_author FOREIGN KEY (authorId) REFERENCES users (userId),
    CONSTRAINT fk_comments_post FOREIGN KEY (postId) REFERENCES posts (postId),
    -- Recusrive relationship - any comment that is a reply stores a pointer to the
    -- parent comment that it is a reply off of
    CONSTRAINT fk_parentCommentId FOREIGN KEY (parentCommentId) REFERENCES comments (commentId)
);


-- Table for linking users and messages. Support both direct messages (one recipient)
-- and group messages (multiple recipients)
CREATE TABLE IF NOT EXISTS `user_messages`
(
    messageId   INT NOT NULL,
    recipientId INT NOT NULL,
    PRIMARY KEY (messageId, recipientId),
    CONSTRAINT fk_userMsg_message FOREIGN KEY (messageId) REFERENCES messages (messageId),
    CONSTRAINT fk_userMsgRecipient_message FOREIGN KEY (recipientId) REFERENCES users (userId)
);

-- Linkage table connecting posts and tagss
CREATE TABLE IF NOT EXISTS `post_tags`
(
    `postId` INT NOT NULL,
    `tagId`  INT NOT NULL,
    PRIMARY KEY (`postId`, `tagId`),
    CONSTRAINT fk_postTags_tag FOREIGN KEY (tagId) REFERENCES tags (tagId),
    CONSTRAINT fk_postTags_post FOREIGN KEY (postId) REFERENCES posts (postId)
);

-- Linkage table connecting users and courses
CREATE TABLE IF NOT EXISTS `user_course`
(
    `userId`    INT                                        NOT NULL,
    `role`      ENUM ('Student', 'Admin', 'Teacher', 'TA') NOT NULL,
    `isActive`  BOOLEAN                                    NOT NULL,
    `courseId`  INT                                        NOT NULL,
    `sectionId` INT                                        NOT NULL,
    -- Each user will have a unique role in each course-section they are a member of
    PRIMARY KEY (`userId`, `courseId`, sectionId),
    CONSTRAINT fk_userCourse_user FOREIGN KEY (userId) REFERENCES users (userId),
    CONSTRAINT fk_userCourse_course FOREIGN KEY (`courseId`, `sectionId`) REFERENCES courses (`courseId`, `sectionId`)
);

-- Linkage table for posts and their viewing groups (a multi-valued attribute)
CREATE TABLE IF NOT EXISTS `posts_viewingGroup`
(
    `postId`       INT                                        NOT NULL,
    `viewingGroup` ENUM ('Student', 'Admin', 'Teacher', 'TA') NOT NULL,
    PRIMARY KEY (postId, `viewingGroup`),
    CONSTRAINT fk_postsViewingGroup_posts FOREIGN KEY (postId) REFERENCES posts (postId)
);

-- Insert sample tags into our DB
INSERT INTO tags (tagName)
VALUES ('homework'),
       ('exam'),
       ('project'),
       ('announcement'),
       ('question'),
       ('discussion'),
       ('resource'),
       ('syllabus');
-- Insert sample departments into our DB: Math, CS, Spanish, Sports
INSERT INTO department (departmentName, description)
VALUES ('Mathematics', 'Department focused on mathematical theory and applications'),
       ('Computer Science', 'Department focused on computation, programming, and algorithmic thinking'),
       ('Spanish', 'Department focused on Spanish language and culture'),
       ('Sports', 'Department focused on physical education and sports');
/**
 Insert sample courses into our DB:
 - Intro to Spanish, Section 01
 - Intro to Spanish, Section 02
 - Fundies of CS 1
 - AP Basketball
 - Linear Algebra
 */
INSERT INTO courses (sectionId, courseId, courseName, courseDescription, departmentId)
VALUES (1, 1001, 'Intro to Spanish', 'Introduction to Spanish language for beginners', 3),
       (2, 1001, 'Intro to Spanish', 'Introduction to Spanish language for beginners', 3),
       (1, 2001, 'Fundies of CS 1', 'Fundamentals of Computer Science 1 - Introduction to programming concepts', 2),
       (1, 4001, 'AP Basketball', 'How to dunk like LeGoat and splash 3 pointers like Steph', 4),
       (1, 3001, 'Linear Algebra', 'Study of linear equations, matrices, vector spaces, and linear transformations', 1);

/**
 Insert sample users into our db: Bob, Alice, Lebron:
 */
INSERT INTO users (firstName, lastName, bio, birthdate, universityEmail)
VALUES ('Bob', 'Smith', 'Computer Science major with a passion for AI and machine learning.', '2000-05-15',
        'bsmith@university.edu'),
       ('Alice', 'Johnson', 'Mathematics major interested in cryptography and number theory.', '1999-10-22',
        'ajohnson@university.edu'),
       ('Lebron', 'James', 'Physical Education professor specializing in basketball techniques and team strategy.',
        '1984-12-30', 'ljames@university.edu');

-- Add our users into the course - Bob as a student, Lebron as a teacher, Alice as a TA
INSERT INTO user_course (userId, role, isActive, courseId, sectionId)
VALUES
-- Bob as a student in Spanish Section 01
(1, 'Student', TRUE, 1001, 1),
-- Bob as a student in Fundies of CS 1
(1, 'Student', TRUE, 2001, 1),
-- Bob as a student in AP Basketball
(1, 'Student', TRUE, 3001, 1),
-- Alice as a TA in Fundies of CS 1
(2, 'TA', TRUE, 2001, 1),
-- Alice as a student in Linear Algebra
(2, 'Student', TRUE, 4001, 1),
-- Alice as a student in Intro to Spanish Section 02
(2, 'Student', TRUE, 1001, 2),
-- Lebron as a teacher in AP Basketball
(3, 'Teacher', TRUE, 3001, 1);

/**
  Insert sample posts into our AP basketball course by Lebron
 */
INSERT INTO posts (title, content, createdAt, updatedAt, isAnnouncement, authorId, courseId, sectionId)
VALUES ('Welcome to AP Basketball',
        'Welcome to the class! In this course, we will be focusing on advanced basketball techniques and strategies. Looking forward to a great semester!',
        '2025-01-15 09:00:00', NULL, TRUE, 3, 3001, 1),
       ('Practice Schedule',
        'Practice sessions will be held on Mondays and Wednesdays from 3 PM to 5 PM. Please bring appropriate gear.',
        '2025-01-16 14:30:00', NULL, TRUE, 3, 3001, 1),
       ('Ball Handling Drills',
        'Today we learned some basic ball handling drills.',
        '2025-01-20 16:45:00', NULL, FALSE, 3, 3001, 1);

-- Make our sample posts viewable to all groups
INSERT INTO posts_viewingGroup (postId, viewingGroup)
VALUES (1, 'Student'),
       (1, 'Admin'),
       (1, 'Teacher'),
       (1, 'TA'),
       (2, 'Student'),
       (2, 'Admin'),
       (2, 'Teacher'),
       (2, 'TA'),
       (3, 'Student'),
       (3, 'Admin'),
       (3, 'Teacher'),
       (3, 'TA');

-- Insert sample tags onto our posts
INSERT INTO post_tags (postId, tagId)
VALUES (1, 4), -- Welcome post tagged as 'announcement'
       (2, 4), -- Practice schedule tagged as 'announcement'
       (2, 7), -- Practice schedule tagged as 'resource'
       (3, 7);
-- Ball handling drills tagged as 'resource'

-- Insert sample comments from Bob and Alice on Lebron's post
INSERT INTO comments (content, createdAt, updatedAt, authorId, parentCommentId, postId)
VALUES ('Thanks for the welcome! I\'m excited to learn more advanced techniques.', '2025-01-15 10:15:00', NULL, 1, NULL,
        1),
       ('The drills we practiced today were challenging but helpful. Could you recommend any additional exercises to improve ball handling?',
        '2025-01-20 18:30:00', NULL, 1, NULL, 3),
       ('I found these drills quite effective when I was playing in college. Looking forward to seeing your progress in class!',
        '2025-01-20 19:45:00', NULL, 2, 2, 3);


-- Insert messages: a DM between Alice and Bob
INSERT INTO messages (createdAt, updatedAt, content, authorId)
VALUES ('2025-01-17 11:20:00', NULL, 'Hey Bob, how are you finding the CS class so far?', 2),
       ('2025-01-17 11:25:00', NULL,
        'It\'s challenging but interesting! I\'m struggling a bit with the latest assignment though.', 1),
       ('2025-01-17 11:30:00', NULL, 'I\'m holding office hours tomorrow from 2-4 PM if you want to stop by for help.',
        2);

-- Link the DM messages to the appropriate recipients
INSERT INTO user_messages (messageId, recipientId)
VALUES (1, 1), -- Alice's message to Bob
       (2, 2), -- Bob's message to Alice
       (3, 1);
-- Alice's message to Bob

-- Insert group chat messages with Bob, Lebron, Alice
INSERT INTO messages (createdAt, updatedAt, content, authorId)
VALUES ('2025-01-18 15:00:00', NULL, 'I\'ve created this group chat for our basketball project team.', 3),
       ('2025-01-18 15:05:00', NULL, 'Great idea! When should we meet to discuss our approach?', 2),
       ('2025-01-18 15:10:00', NULL, 'How about Monday after practice?', 1);

-- Link the group chat messages to all recipients
INSERT INTO user_messages (messageId, recipientId)
VALUES (4, 1), -- Lebron's message to Bob
       (4, 2), -- Lebron's message to Alice
       (5, 1), -- Alice's message to Bob
       (5, 3), -- Alice's message to Lebron
       (6, 2), -- Bob's message to Alice
       (6, 3); -- Bob's message to Lebron