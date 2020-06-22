# Final Proposal: Worship Setlist Generator

### Main Goal

For my capstone, I will be creating a worship setlist generator for use in churches. The main goal is to take inputs such as sermon topics and Bible verses and output a setlist of specified length (e.g. "4 songs") that closely maps on to these topics/Bible verses and helps churches coordinate services and weekly messages. Songs will be chosen based on lyrical content/themes, and setlists will be structured by to fit typical service flow (high tempo songs in the beginning, slower songs at the end). I am expecting inputs to come primarily in two forms: general themes and specific Bible verses.

### Methods & Models

To obtain the data I need, I am using praisecharts.com as a reference. PraiseCharts is a paid service used by many churches to get accurate chord charts for their worship team members. The site also features annual blogs cataloguing the 40 most popular songs for each year, dating back to 2004 and including a Top 40 "so far" list for 2020. Each song on these top 40 lists links to the song's info page, where purchase options are listed and, more importantly, metadata is publicly shared. This metadata includes song authorship, tempo category, and lyrics. Songs are already tagged with multiple themes derived from the lyrics (e.g. "unity," "joy," "healing"), but I am not sure if I will use their themes or construct my own; regardless, specific biblical references are not provided, and I will find a way to generate them. **I have already collected this data.** 

Other data I need is the the Bible text itself. Collecting this data should be fairly straightforward, either through scraping a Bible reference site (the Bible is a public domain text and, as you can imagine, is published widely online) or through an existing Python library (e.g. "python-scriptures"). I am still determining how to best order this data in terms of columns/rows, and I am unsure if I will use the entire Bible or just the parts most likely to inspire lyrics. I am also unsure how many translations of the Bible I want to use, since slight variations of verses can change key words that would impact whether a song is detected as invoking that particular passage. I am waiting to make these decisions before I pull any data so that my extraction is as efficient as possible.

For modeling, I will likely use spaCy to identify themes in the songs' lyrics and either use these themes to pick out Bible verses or find some method for identifying allusions to Bible verses within the songs, since many songs are written with lyrics directly quoting or explicitly paraphrasing passages of the Bible. This part I am still working out. 

Many songs are on top 40 lists for multiple years. I want to be able to weight more popular songs more than songs that were only popular for one year, and I also want to weight newer songs more than older songs (though brand new songs should not be weighted in proportion, I would say the sweet spot is a song that's 1-2 years old). Setlists should be balanced, as brand new songs are hard to sing corporately, since many won't be familiar with all of them, and old songs get REALLY old when you're singing them on a semi-weekly basis for, in some cases, a decade.

### Risks/Assumptions

My biggest risk is assuming that it is possible to use NLP to compare a list of lyrics to the entire text of the Bible and accurately produce verses that the song is likely referring to (or directly quoting). The mechanics of how this will work are unclear to me, but I have no doubt that this is possible. Another concern is how precise this will be, given the overlap between various Bible verses and various song lyrics.

I am a little concerned with how I will measure success. Given my direct experience with this subject, I think I have sufficient domain knowledge, nay, domain expertise to tell whether my recommendation system works well. However, if will be hard to demonstrate this success to others in any objective way.

### Stretch Goals

I would like to 