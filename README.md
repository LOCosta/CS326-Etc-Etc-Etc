# CS326-Etc-Etc-Etc
CS 326 Group Project

## Folder Structure
* The 'project1' folder is for the first project assignment.
* The 'Etc\_Etc\_Etc' folder is for the second project assignment.
  * Within that folder, our webapp is contained within the 'rendezvous' folder.

## Site URL Mapping
* `*/rendezvous/` leads to the index page, which is the main menu page for the site.
* `*/rendezvous/create-project/` leads to the project creation page.
* `*/rendezvous/project/` leads to the generic list view that shows a list of all projects, that page is mostly intended for debug purposes and to make things easier for graders.
* `*/rendezvous/project/[\d\w]+` leads to the specific project based on the given id, which is captured by the regex `[\d\w]+`.
* `*/rendezvous/user/` leads to the generic list view that shows a list of all users, that page is mostly intended for debug and grading purposes as well.
* `*/rendezvous/user/[\d\w]+` leads to the specific user based on the given id, which is captured by the regex `[\d\w]+`.
* `*/rendezvous/advanced-search` leads to the advanced search page, which, while currently nonfunctional, will be able to search for projects on the finished site.