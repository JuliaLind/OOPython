#!/usr/bin/env python3
"""
Flask app for the yahtzee game
"""

import traceback
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session # type: ignore

from src.flashmessage import Flashmessage
from src.errors import SearchMiss
from src.trie import Trie

app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

def recreateTrie():
    trie = Trie.create_from_file(session.get("filename"))
    for word in session["removed_words"]:
        trie.remove(word)
    return trie

@app.route("/", methods=["GET"])
def main():
    """
    Main route
    """

    if not session.get("filename"):
        session["filename"] = "frequency.txt"
    if not session.get("removed_words"):
        session["removed_words"] = []
    session["flashmessage"] = ("", "")
    session["word"] = ""


    return render_template("index.html")


@app.route("/check_word", methods=["GET"])
def check_word():
    """
    Route for checking if word is in trie
    """
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")

    return render_template("check_word.html", flashmessage = message)


@app.route("/check_word", methods=["POST"])
def check_word_():
    """
    Route for checking if word is in trie
    """
    the_word = request.form.get("word")

    trie = recreateTrie()

    msg_type = "danger"
    neg = "not "

    if the_word in trie:
        msg_type = "success"
        neg = ""

    session["flashmessage"] = (f"alert alert-{msg_type}",
        f"The word '{the_word}' is {neg}spelled correctly.")

    # if the_word in trie:
    #     session["flashmessage"] = ("alert alert-success",
    #     f"The word '{the_word}' is spelled correctly.")
    # else:
    #     session["flashmessage"] = ("alert alert-danger",
    #     f"The word '{the_word}' is not spelled correctly.")

    return redirect(url_for('check_word'))


@app.route("/list_words", methods=["GET"])
def list_words():
    """
    Lists all words
    """

    trie = recreateTrie()

    return render_template("list_words.html", trie=trie)


@app.route("/remove_word", methods=["GET"])
def remove_word():
    """
    Rote for removing a word
    """
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")
    return render_template("remove_word.html", flashmessage = message)

@app.route("/remove_word", methods=["POST"])
def remove_word_():
    """
    Rote for removing a word
    """
    the_word = request.form.get("word")

    trie = recreateTrie()

    try:
        trie.remove(the_word)
        session["removed_words"].append(the_word)
        session["flashmessage"] = ("alert alert-success",
        f"The word '{the_word}' has been removed from the Dictionary.")
    except SearchMiss:
        session["flashmessage"] = ("alert alert-danger",
        f"The word '{the_word}' is not in the Dictionary.")

    return redirect(url_for('remove_word'))

@app.route("/prefix_search", methods=["GET"])
def prefix_search():
    """
    Route for finding all words that start with a prefix
    """

    trie = recreateTrie()

    prefix = session["word"]
    session["word"] = ""
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")

    return render_template("prefix_search.html", trie=trie, flashmessage=message, prefix=prefix)


@app.route("/prefix_search", methods=["POST"])
def prefix_search_():
    """
    Route for finding all words that start with a prefix
    """
    session["word"]  = request.form.get("word")

    trie = recreateTrie()

    msg_type = ""
    msg = ""

    if not session["word"] or not trie.prefix_search(session["word"]):
        msg_type = "alert alert-warning"
        msg = f"No words were found with prefix '{session['word']}'." 

    session["flashmessage"] = (msg_type, msg)

    return redirect(url_for('prefix_search'))


@app.route("/suffix_search", methods=["GET"])
def suffix_search():
    """
    Route with the form for finding words that end with suffix
    """
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")
    suffix = session["word"]
    session["word"] = ""

    trie = recreateTrie()

    return render_template("suffix_search.html", flashmessage=message, suffix=suffix, trie=trie)


@app.route("/suffix_search", methods=["POST"])
def suffix_search_():
    """
    Route for finding words that end with suffix
    """
    session["word"] = request.form.get("word")

    trie = recreateTrie()

    if not session["word"] or not trie.suffix_search(session["word"]):
        session["flashmessage"] = ("alert alert-warning",
        f"No words were found with suffix '{session['word']}'.")

    return redirect(url_for('suffix_search'))


@app.route("/correct_spelling", methods=["GET"])
def correct_spelling():
    """
    Route for checking if a word is spelled correctly
    """

    trie = recreateTrie()

    word = session.get("word")
    session["word"] = ""
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")

    return render_template("correct_spelling.html", trie=trie, flashmessage=message, the_word=word)


@app.route("/correct_spelling", methods=["POST"])
def correct_spelling_():
    """
    Route for checking if a word is spelled correctly
    """

    trie = recreateTrie()

    session["word"] = request.form.get("word")

    if not trie.correct_spelling(session["word"]):
        session["flashmessage"] = ("alert alert-warning",
        f"The word '{session['word']}' is not spelled correctly and no similar words were found.")
    elif session["word"] in trie:
        session["flashmessage"] = ("alert alert-success",
        f"The word '{session['word']}'is spelled correctly.")

    return redirect(url_for('correct_spelling'))

@app.route("/change_dictionary", methods=["GET"])
def change_dictionary():
    """
    Route for changing filename for the dictionary
    """
    message = Flashmessage(*session.get("flashmessage"))
    session["flashmessage"] = ("", "")
    return render_template("change_dict.html",flashmessage=message)

@app.route("/change_dictionary", methods=["POST"])
def change_dictionary_():
    """
    Route for changing filename for the dictionary
    """
    session["filename"] = request.form.get("filename")
    session["flashmessage"] = ("alert alert-success",
    f"The dictionary has been changed to '{session['filename']}'")
    session["removed_words"] = []
    return redirect(url_for('change_dictionary'))


@app.route("/reset")
def reset():
    """ Route for reset session """
    _ = [session.pop(key) for key in list(session.keys())]

    return redirect(url_for('main'))




@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."

@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()

# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(debug=True)
