# Worship Setlist Generator

### Problem Statement
<a href="https://en.wikipedia.org/wiki/Evangelicalism#:~:text=Evangelicalism%20(%2F%CB%8Ci%CB%90v%C3%A6,alone%2C%20solely%20through%20faith%20in" target="_blank">Evangelical Christianity</a> constitutes a quarter of the Christian church worldwide and is the dominant religion in the U.S. One important feature of Evangelicalism is worship music (the music sung corporately during church services), and there is a growing number of Christian hit-makers constantly churning out new songs sung by churches around the world. Due to the nature of the music and the context in which the music is performed, it is often very important that a band's setlist for a given service be tailored to that service's message. Curating appropriately themed songs is often up to the pastor and worship leader, and the list of songs to choose from is innumerable and grows every year. The Evangelical Church needs a way to take this burden off its church leaders and maximize its ability to bring together songs that enhance and support the message of each service. My worship setlist generator does just that, by taking in a handful of user inputs and producing a worship setlist tailor-made for your pastor's sermon and ready to bless both your congregation and church leadership.

### Executive Summary

For this project I first gathered data, using BeautifulSoup4 and Requests to build webscrapers that retrived song info, lyrics, and biblical texts from PraiseCharts.com and BibleStudyTools.com. After cleaning the data, I used the Natural Language Processing library <a href="https://spacy.io/" target="_blank">spaCy</a> to process the song lyrics and biblical texts, which included tokenization, lemmatization, and vectorization. Finally, I wrote a function that takes in user input (i.e. Bible verse addresses and sermon keywords, number of songs to be played, and ratio of upbeat/slower songs), pulls the relevant Bible verse text, and compares the verse text and keywords to each song's lyrics to find songs that most closely align with the user's needs. Additionally, I used VaderSentiment to perform sentiment analysis on and explore my data. 


### Data Collection

For this project, I needed three types of data: song metadata (such as artist, tempo, etc.), song lyrics, and the Bible. I got this data from two sources:

-<a href="https://www.praisecharts.com/" target="_blank">PraiseCharts.com</a> <br>
-<a href="https://www.biblestudytools.com/" target="_blank">BibleStudyTools.com</a> 

Praisecharts is a subscription service providng worship sheet music, chord charts, and backing tracks to church musicians. Additionally, PraiseCharts releases an annual "Top 40 Songs of..." list for each year going back to 2004, and I decided these would be great collections from which to pull song lists for this project's first iteration, as it would help guarantee that I was generating setlists of songs that churches are familiar with. Though PraiseCharts is a paid service for most of its content, these "Top 40" blogs are freely accessed, and each song listed in the blogs is linked to its info page (also freely accessed), where price options, metadata, and lyrics are posted. Using BeautifulSoup4, I scraped each song's link from each of these "Top 40" blogs and used those links to gather all the song data that was public. I also ensured that I tagged each song with which year it was featured in a "Top 40" blog for later use. 

BibleStudyTools is a website that, among other things, posts the entire text of the Bible in numerous translations. Because many worship songs explicitly allude to various passages of the Bible (often quoting verses directly), and because wording changes across translations, I decided to pull many versions of the Bible to ensure these lyric references were not lost. Using a list of the "best selling Bible translations" from a <a href="https://www.christianitytoday.com/edstetzer/2011/february/best-selling-bible-translations.html" target="_blank">Christianity Today article</a>, I pulled the text from the 5 most popular translations, as well as one paraphrase version of the Bible (a version that is more concerned with readability to the layman than accuracy/fidelity). These top 5 versions are the New International Version, King James Version, New King James Version, New Living Translation, and English Standard Version, and the paraphrase is The Message. BibleStudyTools uses a uniform structure on its site for each version of the Bible, with Bible books linking to chapters that link to each chapter's verses. I used nested for loops to map onto this structure and pull all the biblical data in an automated, organized fashion.

### Data Cleaning

For my song data, I immediately dropped metadata that I knew weren't going to be important for this inaugural version of my setlist generator, such as album, year published, style, time signature, etc. I retained the names of each song, the artist who popularized that version, the tempo (categorized by PraiseCharts as "Slow," "Med Slow," "Med Fast," and "Fast), and the year(s) the song was popular (i.e. which annual blog(s) it appeared on). I then dropped Christmas songs, as they were numerous and not fit for this version of the project, and flagged tempo as a binary value (lumping "Med Fast" and "Fast" together as 1 and the others as 0), as these two general categories are more useful in ordering a setlist than more particular subdivisions of tempo (though I plan to utilize the even more precise BPMs for each song in later, more sophisticated versions). I then dropped any song that didn't have lyrics and removed "(Live)" tags from songs' titles so that live versions and studio versions would not be counted separately. I attached the number of times a song appeared in the "Top 40" blogs to each song as a new column and dropped all duplicates. In doing this, I kept track of how popular a song was over the last 16 years while ensuring that each song was listed only once. 

*(NOTE: In running certain "test" Bible verses that I knew would probably predict for certain songs that overtly referenced those verses, a process that I outline below, I noticed that one song never showed up. Given my familiarity with both the verse and the song, I found this to be very odd, so I looked at the song's lyrics and noticed one of the keywords shared by the verse and the song was misspelled. Knowing what I was about to do wasn't a scalable methodology--but being unable to unsee what I had seen--I decided to manually change the spelling of this one word. I did not perform a spellcheck in any systematic way on my data, though this one experience ensures that such a process will be integral to future versions of this project. Similarly, I manually tagged a song with a missing tempo with what I felt would be appropriate after listening to the song. This kind of discrepancy can be accounted for in later versions when I use BPM instead of PraiseCharts' tempo categories.)*

For my Bible data, I deemed cleaning to be unnecessary, as I was pulling commonly used and revered public domain texts. However, I did decide to concatenate all of the versions' texts into one somewhat repititious text. Much of this repetition is expunged from my dataset in NLP, and combining the texts in this way ensures that verse-song pairs have a good chance at being predicted despite possible differences in keywords used between Bible translations. I compared use of this six-in-one corpus to that of the NIV, which is the most popular translation in Evangelicalism, and I was more satisfied with the results of the six-in-one Bible text during preliminary setlist generation, so that's what I used in this iteration's final product.

### Data Processing (NLP)

![](/assets/spacy.png)

To process this text data, I used spaCy's robust NLP package that allows for many kinds of data transformations and tagging.

When converting each document into a spaCy object, spaCy tokenizes and vectorizes each word and allows you to manipuate the data in a variety of ways. Such manipulations include the removal of stopwords or non-alphabetic characters, filtering out certain parts of speech (e.g. conjunction words like "and," "or", etc.), lemmatization, employing entity recognition (i.e. differentiating apple the fruit and Apple the company), and much more. For my text, I took advantage of the following:

- Tokenization: breaks a string of words down to its constituent parts
- Vectorization: assigns a unique set of numbers to each token to represent that token
- Lemmatization: reduces tokens to their root dictionary word (e.g. "ran" and "running" become "run")
- Stopwords: removes commonly used words that don't provide much meaning (e.g. "is," "the," etc.)
- I also filtered out all non-alphabetic tokens (i.e. numbers, special characters, punctuation) in this process.

Though the code for the NLP part of this project is very short (thanks mostly to spaCy's robust package that does works much of its magic under the hood), determining to what extent I should process the data took a lot of time. The main challenge was in determining how much of the Biblical and lyric text to prune (i.e. lemmatize and remove), given that in this context the biblical text is viewed as sacred and, as such, songs inspired by the texts often quote passages directly. Removing commonly used words and reducing the remaining words to their root (stopwords and lemmatization, respectively) might dilute any matching verse and lyric texts to the point where exact quotation is no longer recognizable; in other words, a Bible text that might stand out as being word-for-word source material for a given song might now be one of many verses that such a song's processed lyrics text matches. For example, if a given verse and set of lyrics are reduced to words like "praise," "God," and "love" while all connecting words that demonstrate more specificity are removed, this could be any number of verses (especially in the book of Psalms) and song lyrics!

To find out how big of an issue this was, I ran multiple tests on differently processed Bible/song text using specific verses I knew should match up with certain songs (again, this process is outlined below). I tried many styles of processing, some very light (lemmatization) and some more heavy duty (lemmatization, removing stopwords, removing pronouns, etc.) and some in between (removing certain parts of speech rather than all stopwords, leaving in pronouns, and not lemmatizing). No two methods produced the same results, but it was clear that for the most part, the more heavily processed the verse and lyric texts were, the better job my generator did at predicting the songs I was looking for. Thus, I decided to process the data more heavily, which involved removing stopwords, non-alphabetic characters, and lemmatizing each token. 

### The "Model" (i.e. Worship Setlist Generator)

Perhaps the most important tool for my project in spaCy's toolkit is its `.similarity()` method. This method allows you to compare the vectors of two documents, outputting a similarity score on a scale of 0-1 (1 being an identical match). Such a vector comparison is done by taking the average of each word's vector in one document and comparing it with the average of each word's vector in another document. (More technically, this process uses the <a href="https://www.christianitytoday.com/edstetzer/2011/february/best-selling-bible-translations.html" target="_blank">cosine similarity</a> of the vectors, or how similar the vectors' orientation are when graphed in dimensions that are hard to conceptualize as a human.) This spaCy method is at the heart of my setlist generator.

Here is a workflow diagram of my model, follwed by an explanation of how it works:

![](/assets/workflow.png)

To create my setlist generator, I defined a function that takes in four arguments:

1. List of Bible verse addresses (e.g. `[Genesis 1:1, John 3:16]`)
2. List of keywords
3. Number of songs to be returned
4. Ratio of praise/worship songs to return

First, it uses the Bible verse addresses and grabs the processed text of each verse. Next, it puts each verse text in a list, along with each keyword and a concatenated string of all verses and key words in one. (I initially only used the concatenated string, treating all of the text inputs as one text, but the results were abysmal, as you might expect. Too much noise was added in the process and the setlists generated contained songs that measured high in cosine similiarity with the concatenated text vectors but didn't correspond to any one verse or theme in a noticeable way. Still, I included it in addition to each individual verse/theme in case no one input had a high match with any one song). Each object in the new text list is then converted to a spaCy object so that spaCy's `.similarity()` function can be used on it.

Next, each input (i.e. verse, theme, and concatenated string of all verses/themes) is compared to every song in my corpus, and the *n*-number of songs with the highest cosine similarity for each input is saved as a new dataframe. Here, *n* is defined by the set length input, and this process is done for both tempo categories. These dataframes, each containing songs with the *n*-highest cosine similarity ratings for each input and for each tempo, are then put together. If a song came up on the list for multiple inputs, it is counted and tagged with the number of times it appears in the dataframe, and duplicates are then dropped.

Next, songs are sorted again, this time by number of times a song appeared in the list for each input (since a song that is relevant to more than one input text should be considered more important than songs relevant to only one input), then sorted by the year that song was first popular according to the "Top 40" blogs (favoring newer songs), then by how many years it was listed in those blogs (favoring more popular songs), and finally sorted again by similarity rating. 

Finally, a setlist is generated, taking the highest *n*-number of upbeat songs and slower songs as specified by the user (here *n* refers to the ratio argument). The nomenclature common in churches to refer to these different kinds of songs is "praise" for upbeat songs and "worship" for slower songs. I adopt that verbage here. 

Here is a screenshot of my locally hosted Flask application home page, with the input fields described above:

![](/assets/wsg1.png)

Here is what the application looks like with the fields populated:

![](/assets/wsg2.png)

And here is the return page, with a setlist curated to the specified inputs:

![](/assets/wsg3.png)


### Model "Testing"

Data science is a field marked chiefly by its ability to model data and test the validity of those models. However, NLP is a subset of data science that doesn't always mix neatly with this methodology, and this is especially true for recommendation systems like my worship setlist generator. But this doesn't mean that I don't have a "model" or that I can't "test." Using my domain expertise, I came up with a list of songs in my corpus that refer to known bible verses or themes, and I used those verses and themes to see if my generator could predict those songs. Here are the verses I used (in NIV for simplicity), along with the song and lyric that I think best match them:

**Genesis 50:20**: "You intended to harm me, but God intended it for good to accomplish what is now being done, the saving of many lives."<br>
**See A Victory**: (bridge) "You took what the enemy meant for evil and you turned it for good"

**Luke 15:4**: “Suppose one of you has a hundred sheep and loses one of them. Doesn’t he leave the ninety-nine in the open country and go after the lost sheep until he finds it?"<br>
**Reckless Love**: (chorus, referring to God's love) "...oh, it chases me down, fights 'til I'm found, leaves the ninety-nine"

**1 John 4:4**: "You, dear children, are from God and have overcome them, because the one who is in you is greater than the one who is in the world."<br>
**Greater**: (chorus) "And greater is the One living inside of me than he who is living in the world"


In addition, I used key terms that might be used in a message that invokes these verses: 

- **love**
- **battle**
- **power**

Here is the setlist returned, if the number of songs wanted is 5 and the praise:worship ratio is .6:

1. Greater (MercyMe)
2. God Is Able (Hillsong Worship)
3. There's Nothing That Our God Can't Do (Passion, Kristian Stanfill)
4. See A Victory (Elevation Worship)
5. Even If (MercyMe)

Reckless Love is not listed (though I know from experimenting that it is in the top 8 worship songs with these parameters), but my setlist generator picked out the other two test songs! I did this for myriad other verses to similarly satisfactory results. 

### Conclusions and Recommendations

My worship setlist generator returns a setlist to a user's specifications, and after intial, albeit manual, testing, it seems to do a pretty good job recommending appropriate songs. However, much needs to be done for this setlist generator to meet its full potential. Next steps are listed below:

1. More songs! 250 of the most popular songs on PraiseCharts is not a bad start, but there are thousands of songs sung by churches that should be accounted for.
2. Along with #1, churches may know a diverse range of songs, but no church knows all songs. Fulfilling #1 and then integrating this generator into an app like FourScore or a site like PraiseCharts that documents what songs a church has chord charts for would be perfect for generating only songs that your church knows.
3. Along with #2, knowing which keys your band does which songs in. Again, integrating into FourScore would be great for this to ensure the setlist flows even better. 
4. More diverse input. Right now you can only put in up to three verses. I envision being able to upload a sermon outline and have my generator parse verse addresses, verse text, and sermon text and extract out verses/keywords on its own. At the very least, being able to accept a range of verses (e.g. Luke 15:4-7) would be an easy addition that would greatly expand the usefulness of this generator.
5. Use tempo categories other than those of PraiseCharts. PraiseCharts doesn't seem accurate ("See A Victory" isn't a Med Slow song, especially if songs like "Run To The Father" are tagged as Med Fast). It also doesn't seem to take into account time signatures (BPMs feel different depending on 4/4 or 6/8). BPMs and time-signatures can be scraped from DJ websites.
6. Adjusting for seasons. As holidays like Easter, Christmas, and (in the U.S.) 4th of July approach, setlists tend to reflect that. Factoring that into the code so that more and more holiday-specific songs are suggested as the holidays approach would be great.
7. Denominations tend to play different songs depending on style and theology. This is also true for denominations by area (e.g. southern U.S. vs. western U.S. Baptist churches). Accounting for this would be difficult. 
8. Another angle in #7 would be to track recommendations and allow users to rate them so that the generator learns trends in churches, locations, etc.
9. Rate each song with how "biblical" it is (i.e. how many verses it achieves a high cosine similarity with independently as well as in relation to all other songs). 
10. Treat each translation independently in measuring cosine similarity. Also, use more than six translations.
11. Incorporate sentiment analysis into generator
12. Look into pairwise distancing measurements and how those results differ from cosine similarity results
13. Being able to set whether you want to be introduced to new songs or not (see #2)



This worship setlist generator, though it is only a "rough draft" version, works surprisingly well, and the church that employs me is already using it to supplement the choosing of songs for our services' setlists!