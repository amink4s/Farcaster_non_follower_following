# Farcaster Follow Graph Analysis

Pulls a Farcaster account's follower and following lists from the Neynar API, saves each to CSV, then joins them in DuckDB to find accounts that don't follow back.

## What it does

- followers.py paginates the Neynar followers endpoint and writes followers.csv (fid, username, display_name)
- following.py does the same against the following endpoint and writes following.csv
- compare.py joins the two files in DuckDB and writes out.csv

Both pulls use cursor pagination: each response carries a next object holding a cursor, which is passed back as a request parameter until no cursor is returned.

## The query

sql
SELECT fi.username, fi.display_name
FROM read_csv('following.csv') AS fi
LEFT JOIN read_csv('followers.csv') AS fr
    ON fi.fid = fr.fid
WHERE fr.fid IS NULL


A LEFT JOIN keeps every row from following.csv. Where the followers side has no match, fr.fid is NULL, which means the account being followed never followed back.

## Results

On FID 477126 (10,704 followers, 1,678 following), the query returned 637 accounts followed that don't follow back.

## Setup


pip install requests python-dotenv duckdb


Create a .env file in the folder with:


NEYNAR_API=your_key_here


Get a key from the Neynar developer dashboard. .env is gitignored and should never be committed.

## Run


python followers.py
python following.py
python compare.py


## Stack

Python, requests, DuckDB, Neynar API.
