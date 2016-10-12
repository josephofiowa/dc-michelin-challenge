<h1>DC Michelin Guide Challenge</h1>

Predict which Washington DC restaurants will receive stars (and how many) when the Michelin Guide comes out Oct. 13, 2016.

<h2>Getting Started</h2>

No coding was done. Web scraping was done on the <a href="https://www.washingtonian.com/food/restaurantreviews/" target="_blank">https://www.washingtonian.com/food/restaurantreviews/</a>
 database using <a href="https://www.parsehub.com/" target="_blank">https://www.parsehub.com/</a>. Analysis was done with Excel spreadsheets. 

<h2>Data Sources</h2>

The following websites provided data for the analysis:</br>

<strong>Washingtonian Restaurant Reviews</strong> <a href="https://www.washingtonian.com/food/restaurantreviews/" target="_blank">https://www.washingtonian.com/food/restaurantreviews/</a></br>

<strong>Andy Hayler's blog</strong> <a href="http://www.andyhayler.com/restaurant-guide?country=252&city=Washington" target="_blank">http://www.andyhayler.com/restaurant-guide?country=252&city=Washington</a> </br>


<strong>Steve Plotnicki's Opinionated About Dining blog</strong> 2016, 2015, and 2014 top 100 in the United States</br>
<li><a href="http://www.opinionatedaboutdining.com/2016/us.html" target="_blank">http://www.opinionatedaboutdining.com/2016/us.html</a></br>
<li><a href="http://www.opinionatedaboutdining.com/2015/us.html" target="_blank">http://www.opinionatedaboutdining.com/2015/us.html</a></br>
<li><a href="http://opinionatedaboutdining.com/2014/us_1-20.html" target="_blank">http://opinionatedaboutdining.com/2014/us_1-20.html</a>
</br>

<strong>Bon Appetit</strong> 10 Best New Restaurants in America and August 2016 article about DC restaurants
<li>2014 Ten Best <a href="http://www.eater.com/2014/8/19/6168941/bon-appetit-announces-ten-best-new-restaurants-2014" target="_blank">http://www.eater.com/2014/8/19/6168941/bon-appetit-announces-ten-best-new-restaurants-2014</a>
</br>
<li>2016 Ten Best <a href="http://www.bonappetit.com/best-new-restaurants" target="_blank">http://www.bonappetit.com/best-new-restaurants</a>
</br>
<li>August 2016 "Washington DC Is the Restaurant City of the Year" <a href="http://www.bonappetit.com/story/washington-dc-restaurant-city-of-the-year" target="_blank">http://www.bonappetit.com/story/washington-dc-restaurant-city-of-the-year</a>
</br>

<strong>Tom Sietsema Washington Post Top Ten</strong> 2014-2016 
<li>2016 Top 10 <a href="https://www.washingtonpost.com/people/tom-sietsema/" target="_blank">https://www.washingtonpost.com/people/tom-sietsema/</a> and <a href="https://www.washingtonpost.com/lifestyle/food/all-purpose-review-the-neighborhood-restaurant-of-your-dreams/2016/09/06/05c1f95a-5a48-11e6-831d-0324760ca856_story.html" target="_blank">https://www.washingtonpost.com/lifestyle/food/all-purpose-review-the-neighborhood-restaurant-of-your-dreams/2016/09/06/05c1f95a-5a48-11e6-831d-0324760ca856_story.html</a>
</br>
<li>2015 Top 10 <a href="https://www.washingtonpost.com/news/going-out-guide/wp/2015/10/07/how-tom-sietsema-chose-his-2015-top-10-restaurants-list/?0p19G=c" target="_blank">https://www.washingtonpost.com/news/going-out-guide/wp/2015/10/07/how-tom-sietsema-chose-his-2015-top-10-restaurants-list/?0p19G=c</a>
</br>
<li>2014 Top 10 <a href="http://www.washingtonpost.com/sf/guides/guide/2014-fall-dining-guide/" target="_blank">http://www.washingtonpost.com/sf/guides/guide/2014-fall-dining-guide/</a>
</br>

<strong>Michelin Washington DC Bib Gourmand press release</strong> <a href="http://www.prnewswire.com/news-releases/michelin-reveals-washington-dcs-bib-gourmand-selections-ahead-of-inaugural-michelin-guide-debut-next-week-300340721.html#continue-jump" target="_blank">http://www.prnewswire.com/news-releases/michelin-reveals-washington-dcs-bib-gourmand-selections-ahead-of-inaugural-michelin-guide-debut-next-week-300340721.html#continue-jump</a>
</br>


<h2>Setting Boundaries and Modes of Comparison</h2>

The Washingtonian reviews were filtered for DC restaurants with 3 or more stars. The Michelin Bib Gourmand list of 19 restaurants in Washington DC was used to remove any DC restaurants named Bib Gourmands, since they cannot receive a star as well. The current Michelin lists of starred restaurants in the United States (New York, Chicago, and San Francisco) were consulted to determine ratios of starred restaurants to Bib Gourmand restaurants and to compare (using Chicago) the ratio of 3-stars, 2-stars, and 1-star to the total number of starred restaurants.
</br>
<strong>Michelin Chicago:</strong> <a href="http://www.chicagotribune.com/dining/ct-michelin-stars-announced-for-chicago-restaurants-20151027-story.html" target="_blank">http://www.chicagotribune.com/dining/ct-michelin-stars-announced-for-chicago-restaurants-20151027-story.html</a></br>


<h2>Scoring Method</h2>

The Washingtonian restaurant review database gives a star-rating for restaurants. This rating is the foundation for the analysis (only restaurants that received 3 stars, 3.5 stars and 4 stars were used with 2 exceptions). </br>The price guidelines (1 to 4 dollar signs) were also scraped and placed in a column of the Excel spreadsheet. The price helped when evaluating the finalists, with the thought that a Michelin starred restaurant would most likely be at the high ($$$$) end.</br>


Scoring weights were added to or subtracted from the Washingtonian star-base. Each scoring weight is a column in the Excel spreadsheet:</br>
<strong>Bib Gourmand&nbsp;&nbsp;&nbsp;&nbsp; -20 </strong>[flag to remove those named in Michelin's October 6, 2016 Washington DC Bib Gourmand list of 19 restaurants]</br>
<strong>Andy Hayler&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +0.4 </strong></br>
<strong>Steve Plotnicki&nbsp;&nbsp;&nbsp; +0.4 </strong>(OpinionatedAboutDining.com Top 100 for 2014, 2015, or 2016)</br>
<strong>Bon Appetit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +0.2 </strong>(Top 10 or Top 50 for 2014, 2015, or 2016) </br>
<strong>Tom Sietsema&nbsp;&nbsp;&nbsp; +0.15 </strong>(Washington Post Top 10 for 2014, 2015, or 2016) </br>
<strong>Tom Sietsema&nbsp;&nbsp;&nbsp; +0.05</strong> (bump for #1 in WP Top 10)</br>
<strong>Newness penalty&nbsp;&nbsp;&nbsp; -0.5</strong> (if restaurant opened between October 2015 and now)</br>


The scoring weights are added to the Washingtonian star-base, then the StarSum column is sorted in descending order.The top 15 were selected but 6 were discarded, leaving 9 restaurants as "finalists."  Reasons for discards were personal judgments: restaurant too new; another restaurant in the set with same owner/chef; not enough blog "buzz" for the restaurant.</br>
 </br>

<h3>Example: Komi restaurant (blog up-score)</h3>
Komi restaurant was reviewed by Andy Hayler (AndyHayler.com) and Steve Plotnicki (OpinionatedAboutDining.com) as well as receiving a Tom Sietsema Top 10 rating.</br>

Komi Star-base from Washingtonian</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.5</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+0.4 Andy Hayler</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+0.4 OpinionatedAboutDining</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+0.15 Tom Sietsema Top 10</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -----</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4.45 Total Star Rank</br>
                                   
<h2>Assigning 1, 2, or 3 stars</h2>
The 2016 Chicago Michelin star distribution served as a model for how to allocate stars to the 9 Washington DC finalists. However, no Washington DC restaurant was given 3 stars. My reasoning is that DC is new to the Michelin guides and the conservative Michelin reviewers will wait at least a year before awarding 3 stars to a restaurant.</br>

<h3>Chicago 1-star ratio applied to DC</h3>
In 2016 Chicago had 17 restaurants that received 1 Michelin star out of 22 restaurants that received stars: 17/22 or 0.77</br>
9 DC * 0.77 = 6.93 (rounded to 7) restaurants receive 1 Micheliin star. </br>

<h3>Chicago 2-star ratio applied to DC</h3>
In 2016 Chicago had 3 restaurants that received 2 Michelin stars out of 22 restaurants that received stars: 3/22 or 0.14</br>
9 DC * 0.14 = 1.26 (rounded to 2) restaurants that receive 2 Micheliin stars.  </br>

<h3>Chicago 3-star ratio NOT applied to DC</h3>
In 2016 Chicago had 2 restaurants that received 3 Michelin stars out of 22 restaurants that received stars: 2/22 or 0.09</br>
9 DC * 0.09 = 0.81 (but for the reasons stated above I decided not to give 3 stars to any Washington DC restaurant).  </br>


<h2>Notes</h2>

The Excel worksheets (as pdfs) are at the links given below. 
FirstRound  <a href="https://drive.google.com/file/d/0B-I_uKYv_wJcNklWZmQxU2pMUlk/view?usp=sharing" target="_blank">https://drive.google.com/file/d/0B-I_uKYv_wJcNklWZmQxU2pMUlk/view?usp=sharing</a></br>
Finalists  <a href="https://drive.google.com/file/d/0B-I_uKYv_wJccVppcDY5RnNzZTA/view?usp=sharing" target="_blank">https://drive.google.com/file/d/0B-I_uKYv_wJccVppcDY5RnNzZTA/view?usp=sharing</a></br>
Predicted Winners  <a href="https://drive.google.com/file/d/0B-I_uKYv_wJcQjdUaHBhYkRUYkk/view?usp=sharing" target="_blank">https://drive.google.com/file/d/0B-I_uKYv_wJcQjdUaHBhYkRUYkk/view?usp=sharing</a>
</br>



<h2>Acknowledgments</h2>

Thanks to Joseph Nelson (@JosephofIowa) for presenting this as a learning exercise. 
</br>

<h2>Who Is LocalMicro?</h2>
LocalMicro is E.S. Dempsey (Sharon). Follow @LocalMicro on Twitter or send gm to LocalMicro@YouKnowtheRest
</br>

