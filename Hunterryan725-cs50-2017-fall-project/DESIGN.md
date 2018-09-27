A "design document" for your project in the form of a file called DESIGN.md that discusses, technically, how you implemented your project
and why you made the design decisions you did. Your design document should be at least several paragraphs in length.
Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a
technical tour of your project underneath its hood.

The technical aspects of my project begin first with the user registration process which is meant to authenticate the user is an individual with
an active yale email address. Upon filling out the requisite boxed under registration and clicking submit, a validate form function is run over the email
to ensure that it contains the string "@yale.edu". The password is additionally hashed, all of the information is stored in the database, and the user is
redirected to the login page. Upon successful registration, the user will receive a confirmation email stating the user has officially registered and
an access key through the email that is 5 randomly generated numbers, which are stored in the database. This access key is then to be used in order
for the user to login and be directed to the home page.

To begin with the homepage, there are manyy different design concepts incorporated. The nav-bar is fixed so that as the user scrolls up and down the nav bar
follows. Additionally the background is an image from the internet that was incorporated and set so the image does not repeat and also remains fixed as the user
scrolls the page. The table bodies contain alternating colors using nth-child even and odd to alternate between grey and white and the header of the table contains
Yale blue similar to the nav bar. Inside each of the table body rows there are different forums, each of which contains a link to a different forum.

Upon clicking on a forum the user is directed to a dynamically generated url structured as /forums/<value> where <value> is the thread. On this page,
the tables again alternate color using nth-child. On the top there is a button Post. This will redirect the user to a page with the structure /post/<value>
where value again represents the forum in which the user is posting under. Upon filling out the information to post the description and title fields are stored in
the database and the <value> in the url is used to store the forum for that thread in the database. The content inside the table is returned using Jinja and
iterating through. Because the information needed for the table was found between two different tables in the database, an INNER JOIN needed to be used
to connect the tables With the information returned into the rows links were also embedded in the information. For the titles that link to the thread comment
area, Jinja was used to return part of the link. Similarly, the names connecting to those users profile were constructed using jinja to return part of the link
so it varies based on the user what the link is. Upon redirected to each of these pages again dynamic urls are used so that templates do not have to be made for everything

Upon clicking on the thread the initial post in addition to a list of comment(s) will be displayed. A link is embedded again using jinja to return part of the link
inside the users who posted and below there is the option to comment through filling out the box. Upon clicking post the box returns POST to the page storing the
comment in the database under the threads table along with a thread id so that all comments can be returned through a thread id. This thread id links to the
forums table in the database so that the initial post and all comments can be returned through thread id which is part of the dynamic url.

Upon clicking on another users profile a profile picture is returned if the user has uploaded one, otherwise a defult profile picture is show. Various information
is displayed, returned through jinja. At the bottom of the page is a link that redirects the user to a page that displays all of the threads started by the
individual whose page the user was on. These threads each contain links directing to those threads.

Upon clicking on post the user is directed to a page that has information to be filled out. The forum and category are contained in drop down boxes making sure the
user inputs valid values that can be returned on the pages. On clicking post the thread is submitted.

Upon clicking on profile the user is directed to their personal profile. This page contains the individuals personal information and allows the individual to
upload an image using os.path to store the image in the IDE and store the name of the file in the database. This name is then returned via Jinja to display that profile
picture for all to see.

Upon clicking on my posts, a list of posts by the user is returned through the database.

Lastly, upon clicking on the login button, the user is signed out.