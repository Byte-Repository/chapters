Project Overview
The E-Learning Platform is a web application where students can enroll in courses, access course materials, and upload portfolio work as a part of their learning experience. The platform has been modified and extended based on specific project requirements, including Docker deployment for production readiness.

Features Implemented
Core Features (Chapters 12-17)
Student Enrollment and Course Content

Students can enroll in available courses.
Enrolled students can view course contents, organized and paginated for ease of navigation.
Portfolio Uploads

Students can upload representative work (e.g., text, PDFs, PNGs, and MP4s) for each course they’re enrolled in.
This functionality includes a form where students can upload files, which are then associated with the respective enrolled course.
Portfolio Content Types

Text: Students can enter text directly or upload text files.
Image: Supports PNG format uploads for images.
Video: Supports MP4 format for video content.
PDF: Students can upload PDFs as part of their portfolio submissions.
Role-Based Content Viewing

Students can view only their own portfolio items associated with each course.
Instructors/Administrators can view all portfolio items uploaded by all students in a course, allowing them to manage and review student submissions easily.
Deployment Preparation

Following Chapter 17, the project has been set up with "Going Live" steps to ensure production readiness.
Docker integration packages the project into a container for straightforward deployment.
Usage
User Roles

Students can enroll in courses, view course content, and upload work as part of their portfolio.
Instructors/Administrators have management access to view all students’ uploaded work for each course.
Portfolio Submission

Each portfolio item includes a title, date, and a link to view the content in detail.
Uploads are limited to PDF, PNG, MP4, and text formats to maintain consistent portfolio content types.
Deployment

Production setup is handled through Docker, making the project containerized and prepared for live hosting.
