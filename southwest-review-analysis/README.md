# Southwest Review Analyzer

The Southwest Review Analyzer is a web-based tool designed to process, display, and interpret customer reviews from Southwest Airlines. It applies sentiment analysis techniques to evaluate the tone of each review—positive, negative, or neutral—and organizes the results in an interactive, paginated interface as well as through five insightful visualizations. 

## Structure
- App includes everything related to the making of the web-based tool. The file app.py is where the tool can be launched. Simply following the link when it is successfully running will take you to the homepage.
- Data is where the reviews are processed after being scraped. This includes cleaning the data and then performing sentiment analysis for each review.
- Scraper is where the reviews are initially scraped from Southwest Airlines' profile on TrustPilot. The amount of reviews scraped depends on the user input while using the app.
