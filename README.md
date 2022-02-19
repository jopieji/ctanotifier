# CTA Train Tracker with Notifications
### Jake Opie

---

### Overview
This project is going to be a web app that tracks a user's selected CTA trains and buses, and provides browser notifications to let the
user know when their train or bus is coming. This app will hopefully be useful to someone, as I am not sure there is a browser-based CTA
tracker out right now. The browser notifications will be perfect for students, who so often have many many tabs open and might forget to
keep an eye on when their bus/train might show up!

Right now, I am experiementing with creating a sort of intermediary API that will take requests from my Javascript, insert the API key and make a call to 
the remote CTA Train Tracker API. I want to take this approach to get some experience developing APIs in Java, as using a framework like Express with Node or
React would be much easier in this context. I might shift this choice later on, but we will see.

Spring Boot might not be the right choice either because it usually interfaces with a database, which as of right now, I don't plan on using. I could store each user's stops in a NOSQL database, but I don't need much functionality of my API; it is solely to add the API key to the URL. This also might change, but for now I am content with my initial idea. 

2/18/2022 Update
I'm having issues with Java dependencies, Maven, and other configuration stuff, so I might try and implement this using Django. This is something I've been looking into for over a year, but have yet to work with Django on a project.

I've fully pivoted to using Django.

### Technology
The technologies I plan on using are Javascript, Java, Spring Boot, and the CTA Train Tracker API.

I might add the CTA Bus Tracker API once I get an MVP up and running.

---
### Future Plans
As I mentioned above, I am going to add bus tracking and notifications as soon as possible. Also, I can experiment with email notifications
once the project has a real user base. Tackling custom emails (with ads, or custom messages) might be a fun experiment for me to try.

---

Feel free to reach out to me with any questions.
