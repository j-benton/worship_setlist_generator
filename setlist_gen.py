

import numpy as np
import pandas as pd
import spacy
import en_core_web_lg
nlp = spacy.load('en_core_web_lg')

songs = pd.read_csv('./data/clean_songs.csv', index_col='Unnamed: 0')
bible = pd.read_csv('./data/clean_six_bible.csv', index_col='Unnamed: 0')

def process_themes(text):

    # Converts text into spacy object
    text = nlp(text)

    # Returns alphabetic tokens w/o stopwords
    return [token.lemma_.lower() \
                     for token in text \
                     if token.is_alpha \
                     if not token.is_stop]

def setlist_generator(verses, themes, set_length, pw_ratio):

    # Removes empty strings
    verses = [verse for verse in verses if verse != '']
    #themes = [theme for theme in themes if theme != '']

    # References verse list to extract biblical text
    verse_text = [bible.loc[verse]['verse'] for verse in verses]

    # Converts themes to list of individual words w/o punctuation, stopwords, etc.
    themes = process_themes(themes)

    # Concatenates verse text and theme words
    concat_text = [''.join([bible.loc[verse]['verse'] + ' ' for verse in verses]) + ' '.join(themes)]

    # Puts all input text into one list to convert to spaCy object
    all_text = verse_text + themes + concat_text

    # Converts input text to spaCy object
    processed_text = [nlp(text) for text in all_text]

    # Creates empty list to store top scoring songs
    df_list = []

    # Iterates through processed input text to find most similar songs
    for text in processed_text:

        # Saves 'songs' df to new variable to keep df fresh for each iteration
        df = songs

        # Creates new column containing similarity score for each song/input text
        df['score'] = [text.similarity(nlp(lyrics)) for lyrics in df['lyrics']]

        # Sorts scores in descending order
        df.sort_values(by='score', ascending=False, inplace=True)

        # Puts top praise songs into empty list above
        df_list.append(df[df['tempo'] == 1].head(set_length))

        # Puts top worship songs into empty list above
        df_list.append(df[df['tempo'] == 0].head(set_length))

    # Combines all top praise/worship songs for each input text
    master_df = pd.concat([df for df in df_list], axis=0)

    # Creates column with number of times each song appears in df
    master_df['song_count'] = master_df['song'].apply(lambda x: master_df.song.value_counts()[x])

    # Sorts master_df by scores and drops duplicates, keeping highest score for each song
    master_df = master_df.sort_values(by='score', ascending=False)\
                         .drop_duplicates(subset='song', keep='first')\
                         .reset_index(drop=True)

    # Creates list of variables to sort by (in order)
    sort_list = ['song_count', 'year', 'years_pop', 'score']

    # Separates praise/worship songs after sorting by list above
    praise = master_df[master_df['tempo'] == 1].sort_values(by=sort_list, ascending=False)
    worship = master_df[master_df['tempo'] == 0].sort_values(by=sort_list, ascending=False)

    # Selects number of praise/worship songs based on user input
    pw_ratio = pw_ratio/100
    praise_set = round(set_length * pw_ratio)
    worship_set = set_length - praise_set

    # Uses praise/worship ratio to select top songs from each list and create ordered setlist
    setlist = pd.concat([praise.head(praise_set),\
                        worship.head(worship_set)],\
                        axis=0, ).reset_index(drop=True)

    # Returns setlist
    return {f'{i+1}'+'.': f'{setlist.song[i]} ({setlist.artist[i]})' for i in range(len(setlist.index))}
