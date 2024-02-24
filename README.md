# FOOROOM

![Project-image]()

Fooroom is a forum site that aims to strike a happy middle ground between the modern format of Reddit and the sleek form and functionality of traditional bulletin board sites from decades past. Ease of use and no distractions make the foundation of this app's design philosophy.

Users can post, discuss, and interact without any unnecessary distractions.

[View the website here](https://fooroom-9cc630806337.herokuapp.com/)

## Contents

* [Features](#Features)
  * [Existing Features](#existing-features)
    * [Home page](#home-page)
    * [Post page](#post-page)
    * [Profile page](#profile-page)
    * [Register/Login page](#registerlogin-page)
  * [Future Implementations](#future-implementations)
  * [Defensive Design Feaures](#defensive-design-features)

* [User Experience](#User-Experience)
  * [User Stories](#User-Stories)

* [Deployment](#Deployment)
* [Heroku](#heroku)
* [GitHub](#github)

* [Design](#Design)
  * [Color Scheme](#Color-Scheme)
  * [Typography](#Typography)
  * [Images](#Images)
  * [Wireframe](#wireframe)
  * [Accessibility](#Accessibility)
  * [Agile Methodology](#agile-methodology)
  * [Data Model](#data-model)

* [Technologies Used](#Technologies-Used)
  * [Languages Used](#Languages-Used)
  * [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)
  * [Other Technologies Used](#other-technologies-used)

* [Testing](#Testing)
  * [Solved Bugs](#solved-bugs)
  * [Known Bugs](#unfixed-bugs)
  
* [Credits](#Credits)
  * [Content](#Content)
  * [Media](#Media)
  * [Tutorials & Code Used](#tutorials--code-used)

## Features

The site has two pages, one for the main menu and one for the game itself.

### Existing Features

#### Home Page:
![Home page](#)

The home page displays a list of posts sorted by recent activity. Each post shows the avatar of the original poster along with information about when the post was posted, how many likes and comments it has, and when it got its latest comment. Clicking any of the posts opens the corresponding post as a new page. Posts designated as "sticky" are always displayed at the top of the list with a light border and an asterisk before the title.

The search bar lets users filter posts to easily find what they're looking for.

#### Post Page:
![Post page](#)

Here, users can see the full contents of a chosen post along with any comments it has. Comments are sorted from oldest to newest in descending order. Under the main content of each post, there's a like button with its associated counter. To the right of it, there are buttons for editing and deleting the post. Given an authenticated user, the buttons appear to give the user full CRUD capabilities. Any user assigned as staff or administrator also gets these controls for all posts and not just their own.

#### Profile Page:
![Profile page](#)

On the profile page, an authenticated user can write a presentation and upload a profile picture. There's also a button for deleting the account. Users can also see a list of posts and comments made by the associated user, each one linking to its origin.

#### Register/Login Page:
![Login page](#)

The pages for account registration and user authentication are kept simple and clean. New users can sign up using a username, with email registration kept optional for a better user experience.

### Future Implementations:

The main thing I'd change in the future is the setup for image hosting and external resources. With the current setup, I can't access and change certain factors that are detrimental to page loading and general performace. Cloudinary is slow, Summernote's internal structure doesn't fully comply with current best practices, and the bootstrap imports redundant data. In the scope of a bigger project, I'd have dealt with this, but it wasn't a feasible investment of time for this study project.

In a potential future iteration, I'd also like to add private messaging and a friend system. The list view and post detail view should also enable sorting choices.

### Defensive Design Features

These are the features I have implemented for defensive design.

* Authentication checks
  * With the @login_required decorator on certain views, I restrict access for unauthenticated users.
  * Using Django's UserPassesTestMixin, I ensure that users can not edit other user's posts (unless they have administrator access)
  * Admin features are only accessible if signed in as a superuser
  * I refrained from using the @csrf_exempt decorator for ajax calls to avoid potential cross-site exploits
  * Manually inputting URLs to sensitive endpoints such as account deletion does not grant access

* Form validation
  * If a form contains any invalid data on submission, it will refuse to submit and instead warn the user
  * Image file size is restricted using a custom validator
  * Model fields that can be manipulated have default values and restrictions such as maximum character count
  * CSRF token checks ensure that forms can only be submitted by users on the site
  * No base forms that could enable code injection

* Backup and default values
  * Image fields have a placeholder to prevent broken links
  * Profiles, images, and more have a creation routine that automatically adds them to prevent null references
  * Template tags check for placeholders and nonexistent values before rendering anything to the page

* Error pages
  * A custom 404 page appears if users try to visit a non-existent page. The page features a button for returning to the home page.
  * A custom 500 page appears if the site encounters a server error trying to load content. The same "return to home" button is found here too.

## User Experience

### User stories

__Site owner / Administrator goals__

EPIC - Site Administration

* As a site admin, I can manage, edit, and delete content on the site

* As a site admin, I can delete user accounts from the site

__User goals__

EPIC - Site navigation

* As a site user, I can have a clear idea of the site as soon as I open it so that I can know whether I should stay there.

* As a site user, I can see how to navigate the site intuitively so that I can find what I want and find the around the site

* As a site user, I can see a segmented list of posts so that I can select what to read

* As a site user, I can click on a chosen post to see the whole post and its thread of comments on its own page

EPIC - User posting

* As a site user, I can submit a new post to the forum so that people can read my post

* As a site user, I can post replies to other people's posts and replies so that we can discuss the content of the post

* As a site user, I can edit or delete my posts so that I can correct mistakes

* As a site user, I can like posts and see how many likes a post has

EPIC - User profile

* As a site user, I can upload a profile picture

* As a site user, I can view the profile page for my account and others

* As a site user, I can see my posts and profile picture on my profile page

## Design

### Color palette

![Color Palette](documentation/color-palette.png)

I decided from the start that I wanted a "night mode" design for this site, but not just grayscale. I went with muted purple tones. This palette is consistently applied across the whole site, including widgets. Certain important buttons are kept red to highlight their nature, but everything else adheres to the color theme.

### Typography

For this site, I kept it simple with a clean sans-serif font across the whole site. Roboto is the name of the font, which I imported from Google Fonts.

### Images

The site uses no imagery of its own and instead leaves the whole image space for users' profile pictures.

### Wireframes

Before

<details>
![Wireframe](documentation/post-list.png)
</details>

<details>
![Wireframe](documentation/thread-view.png)
</details>

<details>
![Wireframe](documentation/profile-page.png)
</details>

### Accessibility

I ensure high accessibility by using high contrast design across the entire site. I have also used ARIA features such as the aria-label and aria-hidden HTML tags to help screen readers perform well. I verified the accessibility with Lighthouse, WAVE, and Internet Disability Simulator. 

### Agile Methodology

I used GitHub projects to manage this project's development stages using Agile methodology. You can see my [iterations](https://github.com/EmilionR/django-pp4/milestones) and [project board](https://github.com/users/EmilionR/projects/4/views/1) to learn more.

After breaking up the epics into user stories, I added all the user stories to the Issues page and connected them to the project board. I then set up milestones for each iteration and sorted relevant user stories into the corresponding iteration milestone based on urgency and importance. I kept iterations short and somewhat flexible.
Each user story has a list of acceptance criteria and associated tasks, each one with a checkbox for easy tracking of progress.


### Data Model

![Data model](documentation/forum-erd2.png)

I used a PostgreSQL relational database for this project. The entity relationship diagram (ERD) above represents the database of the project. The one below represents the original idea I envisioned before building the program.
I had to make some alterations to harmonize better with Django's modular design and safety features.

I use a highly object-oriented design for the project, using abstraction and mixins where applicable to reduce repetitions and redundancy. For example, I have an abstract model laying the foundation for posts and comments. I had to break away from this abstraction a few times due to the way django handles certain relations.

The models for posts and comments are there to let users create content. Each time a user submits a post or comment, a new object based its model is created. Similarly, a profile object is assigned to each new user created. And each time a user likes a post or a comment, this creates a new like object pairing the user and the entry so that users can only like any given entry once.

<details>
![Old data model](documentation/forum-erd.png)
</details>

## Technologies Used

### Languages Used

Python, HTML, CSS, and JavaScript.

### Frameworks & Libraries Used

Django - The main framework, used for database handling and templates

Bootstrap - Used for more efficient styling and scripting

Summernote - Posting forms

FontAwesome - Supplies the icons used across the site

Google Fonts - Supplies the webfont used

### Other Technologies Used

VSCode - Used for all the coding.

Git - For version control.

GitHub - For project management and storage

Heroku - For live site deployment

AWS - Hosting the database

Cloudinary - Hosting the profile images

Google & Mozilla Developer Tools - For debugging and trying out design improvements on the fly.

GNU Image Manipulation Program - Cropping and scaling images for faster load times.

Figma - Wireframing

Lucidchart - ERD design

Am I Responsive - For testing how the site looks on different devices.

WAVE Evaluation Tool - To check accessibility.

Web Disability Simulator - To check accessibility.

realfavicongenerator.net/ - For the Favicon

## Deployment

### Heroku

To deploy the project to Heroku, I took the following steps.

__Requirements and Procfile__

In order to deploy the project, Heroku needs information about the technologies used. Before deployment, I create a Procfile and a list of requirements. In some cases, you may also need a runtime.txt file specifying the version of Python to use.

* Create a plain file called Procfile without any file suffix, at the root level of the project.
* Type ```web: gunicorn fooroom.wsgi:application``` into the Procfile and save.
* In your IDE terminal, type ```pip3 freeze local > requirements.txt``` to create the requirements.
* (Optional) Create a runtime.txt and type ```python-3.12.1``` (or whichever version you use)
* Commit and push these files to the project repository.

__Create the Heroku app:__

* Sign in or sign up to [Heroku](https://heroku.com/).
* Click the button that says "Create new app."
* Enter a unique app name.
* Choose your region from the dropdown menu.
* Click the "Create app" button.

__Heroku Settings:__

For Heroku to be able to process and render the project, you must define some environment variables.
Deploying the project without these is like trying to start a car without the key.

* Go to the settings page of your new app
* Scroll down and open the Config Vars
* Add a DATABASE_URL variable and assign it a link to your database
* Add a SECRET_KEY variable and assign it a secret key of your choice
* Add a CLOUDINARY_URL variable and assign it a link to your Cloudinary

__Project Settings:__

It's important that the environment variables and settings in the django project are compatible with the settings on heroku. These are the steps to ensure a proper setup.

* Include ```https://<your_app_name>.herokuapp.com``` in the ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS lists inside the settings.py file.
* Make sure that the environment variables (DATABASE_URL, SECRET_KEY, and CLOUDINARY_URL) are correctly set ```to os.environ.get("<variable_name>")```
* If making changes to static files or apps, make sure to run collectstatic or migrate as needed.
* Commit and push to the repository.

__Connect the repository__

Once your Heroku settings and GitHub repository are up to date, it's time to connect the two.

* Go to the Deploy tab of your heroku app.
* Find the "Deployment method" section and click GitHub.
* Type in the name of your repository to search for it
* Click 'Connect' to connect the repository
* (Optional) Enable automatic deployment to automatically update the Heroku app whenever you push to GitHub

__Deploy the project to Heroku__

Now, all that's left to do is to deploy and open the app.

* Click "Deploy branch"
* Wait for Heroku to finish building the app.
* Upon successful deployment, click the "View" button to open the app.

### GitHub

__How to Fork the Repository__

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [EmilionR/django-pp4](https://github.com/EmilionR/django-pp4)
3. Click the Fork button in the top right corner.

__How to Clone the Repository__

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [EmilionR/django-pp4](https://github.com/EmilionR/django-pp4)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

## Testing

Please refer to [TESTING.md](TESTING.md) for full testing documentation.

### Solved Bugs

### Unfixed Bugs

## Credits

### Media

**Images used**

Grandmaster - [Generated with Night Cafe](https://creator.nightcafe.studio/)

Cat - [Photo by Raoul Droog](https://unsplash.com/photos/russian-blue-cat-wearing-yellow-sunglasses-yMSecCHsIBc?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
  
Mouse - [Photo by Joshua J. Cottenhttps](https://unsplash.com/photos/a-rat-sitting-on-a-piece-of-wood-QxW15BmJxOQ?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)

### Tutorials & Code Used

Unique together, abstract classes, and more
https://docs.djangoproject.com/en/5.0/ref/models/options/

Signals used for automatically creating a profile when a new user is created and updating post activity when new comments are posted
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/

Phind for help with the post form and edit model

For cloudinary and profile image form
https://cloudinary.com/blog/managing-media-files-in-django
https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/enctype

Shortening the datetime format
https://docs.python.org/3/library/datetime.html

CSRF without forms for the 'like' button AJAX code
https://stackoverflow.com/questions/7827079/django-csrf-token-without-forms

Queryset manipulation with Django Q model
https://docs.djangoproject.com/en/5.0/topics/db/queries/#complex-lookups-with-q-objects

Scrollbar styling
https://www.w3schools.com/howto/howto_css_custom_scrollbar.asp

Summernote form integration
https://github.com/summernote/django-summernote?tab=readme-ov-file#form