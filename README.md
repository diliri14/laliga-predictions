# APP ACCESS: https://diliri.pythonanywhere.com/


## My Product

To achieve my final product, I will work on the design and development of a data analysis application, which will function to determine the probability of victory, draw, or defeat in each match between teams in any football game in the Spanish league. Users will be able to interact with the application developed in my project through a webpage and visualize the results produced by the predictive tool that uses the program. My idea is to show, for each game, an interface similar to this:

![image](https://github.com/user-attachments/assets/b41c97ee-4940-4dce-b3da-7a052ddd0a7c)

## Learning Objective

Numbers are a part of my life. Since I can remember, and according to my parents, I have done things that were advanced for my age. I learned to count and perform arithmetic operations before entering preschool. I really enjoy solving problems that involve mathematical analysis and logic, so my life has been tied to numbers and will continue to be. For this reason, I have known for several years that my future profession should be related to this area. On the other hand, I have practiced various sports throughout my life; football, in particular, has captured my attention. Although I recognize my limitations in playing it, I am currently a huge fan of this discipline, specifically of FC Barcelona, a team in the Spanish Primera División.

So, how can I combine both passions? This is where Data Science comes in, an area of knowledge that involves understanding the meaning of historical information to foresee and even predict future behaviors and outcomes. During the quarantine, I had the opportunity to learn basic notions of the Python programming language with my mom; and it turns out that programming is one of the foundations for being a data scientist. I am currently passionate about this area of knowledge, along with the development of algorithms and tools to analyze information accurately.

For the reasons already presented, my learning objective is to take the first steps in my training as a data scientist and connect my passions and skills (mentioned above) with my development and professional future (in this case, through the example of predicting match results involving FC Barcelona in the Spanish league and the possibility of becoming champions this season 2022-2023).


## Research

After conducting research and taking a course (Algorithms & Programming) at Universidad Metropolitana, I was able to better understand the world of data science, as well as the ideal programming language to carry out a project in this area—Python. I used its internal libraries such as Pandas, Numpy, and Scipy.

I identified that, to calculate the probability of victory, draw, and defeat of a team in a football match, three main parameters are used:

  - The offensive and defensive strength of the home and away teams (average goals scored and conceded at home/away, multiplied by the total goals scored). The method used for this calculation is known as the Poisson Distribution.
  - The recent form of both teams (number of wins, draws, and losses in their last 15 matches).
  - Head-to-head results (number of wins, draws, and losses for each team in previous matches they faced each other).

The three methods are explained in more detail in the contextual information. The databases I used to extract the information are found on Wikipedia. From there, I gathered all the results from all matches over the last six seasons (2017/18 to 2022/23, which is currently ongoing).

To develop the webpage, I chose HTML, a language that allows us to structure a webpage on the internet. CSS is an “extension” of HTML that enables us to manage the design and appearance of the page. To transfer the analysis tool to the web, I used Flask, a micro web framework that allows for the integration of webpage files and the functions of the program I developed.

## Context information

### Poisson distribution

The Poisson distribution is a mathematical tool that allows for the analysis of possible future outcomes based solely on the historical data of each team. In other words, it is a discrete probability distribution in which it is only necessary to know the events and their average frequency of occurrence to determine the probability of them happening. This analysis strategy focuses on performance statistics shown by a team to determine their future scores or performances; however, to obtain the most probable results, time must be spent researching all competing teams, reviewing many of their previous matches.

To predict a match, for example, in La Liga, we need to calculate the attacking power (PA) and defensive power (PD) of the two teams studied, under a defined condition (home or away).

The attacking power (PA) is the average goals scored by a team in a home/away condition, divided by the average goals of the competition (GT) in the same condition.
The defensive power (PD) is the average goals conceded by a team in a home/away condition, divided by the average goals of the competition (GT) in the same condition.
After calculating the attacking and defensive power of both teams, we must determine the expected goals of the teams depending on their condition.

To get the expected goals for the home team: PA (home) x PD (away) x GT (home)
To get the expected goals for the away team: PA (away) x PD (home) x GT (away)
Once we have the expected goals, we apply the Poisson formula to those expected goals; this calculation will determine the probability of a team scoring 0 goals, 1 goal, 2 goals, and so on. We can then tabulate values for each possible score by simply multiplying the probabilities of each team scoring a certain number of goals. For instance, for a result of 2-1, you multiply the percentage probability of the home team scoring 2 goals by the away team scoring 1 goal. For the total probabilities, we sum all combinations in which the home team wins, all in which there is a draw, and all in which there is a loss (Pinnacle, 2017).

### Head-to-Head Results

This method allows for predicting the outcome based on the encounters between both teams, considering the last 5 seasons. It counts the wins, draws, and losses of each team. The results of previous encounters in the condition we want to predict (home or away) carry more weight in the calculation. The inclusion of this method is justified as certain patterns have been found in teams that have been unable to defeat others despite being historically superior or having better results against the rest of the teams in the league.

### Recent Form of the Teams

This method uses the outcome probabilities of a match based on the last 15 games of each team in La Liga. It counts the wins, draws, and losses of the clubs with a weighted average (the more recent the match, the greater its relevance); and like the previous model, matches in the condition being played (home or away) carry more weight in the calculation. This condition is also fundamental, as some teams are better than others. However, if a "superior" club is on a losing streak, their chances of victory diminish, just as the chances increase for an inferior team that is in good recent form.
