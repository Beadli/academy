---
title: "6.9 Open the database your Git server is running on"
sidebar_position: 9
---

# 6.9 Open the database your Git server is running on

You've been running a database since lesson 6.6 and nobody mentioned it.

Every application you will ever operate keeps its state somewhere, and
that somewhere is almost always a database. Your Git server knows who you
are, which repositories exist, and who is allowed into them, and it does
not keep that in a text file. Today you open it and ask it questions.

The reason this belongs in an infrastructure course, rather than a
developer one, is that "look in the database" is an operational move. Why
does this user still show as active after I deleted them? Which accounts
have admin? How many repositories are actually in use? Support articles
answer those questions with screenshots of a web interface that changes
every release. The database answers them directly and doesn't change.

You do not need to become a database administrator. You need to be able to
open one, find your way around, and get an answer out.

## Two kinds of database, in one paragraph each

**Relational** databases store data in tables: rows and columns, with a
strict shape agreed in advance. A `user` table has a column for the name,
one for whether they're an admin, and every row has exactly those columns.
Relationships between tables are the point, hence the name: a repository
row doesn't repeat its owner's name, it stores the owner's `id` and you
join the two together when you need both. You talk to them in **SQL**
(Structured Query Language). PostgreSQL, MySQL, SQL Server, and SQLite are
all this kind, and they are the overwhelming majority of what you'll meet.

**Non-relational**, often called **NoSQL**, relaxes that. Documents can
have different fields from each other, and there's no schema agreed in
advance. That flexibility suits data whose shape you don't know yet, which
is why the search and logging tools in Module 12 use one. The trade is
that the database can no longer enforce consistency for you, so the
application has to.

Gitea uses SQLite, which is relational and unusual in one respect: there's
no server process at all. The entire database is a single file on disk.
That makes it a good first one to open, and it's the same SQL you'd type
against a Postgres cluster with a thousand connections.

## Find the file

In lesson 6.6 you mapped `./data` into the container. Everything Gitea
owns lives there, including its database:

```bash
cd ~/gitea
ls -lh data/gitea/gitea.db
```

Expect a single file, a few megabytes at most.

That is worth pausing on. Your entire Git server, every repository's
metadata, every account, is that one file plus the repositories beside it.
It's also the clearest possible illustration of why lesson 6.6 told you
that backing up `./data` gets you everything.

Install the command-line client:

```bash
sudo apt install sqlite3
```

## Open it without breaking it

**Open it read-only.** The application is running right now and expects to
be the only thing writing to this file:

```bash
sqlite3 "file:data/gitea/gitea.db?mode=ro" -header -column
```

The `?mode=ro` is not decoration. A stray `UPDATE` or `DELETE` against a
live application's database is one of the classic ways to ruin an
afternoon, and unlike a bad config change there is no reload that undoes
it. Read-only makes the mistake impossible rather than unlikely.

You'll get a `sqlite>` prompt. Two things before anything else: `.tables`
lists what exists, and `.quit` gets you out. If you ever find yourself
stuck at a `...>` prompt, you forgot the semicolon that ends a statement.

:::tip[Least privilege]
Opening read-only is the principle from lesson 5.6 applied to data. You
need to *read* this database, so take exactly that and nothing more.

In production the same idea is a separate database account with `SELECT`
permission and no write permission, handed to reporting tools and
analysts. Same instinct as `sudo`, as `PermitRootLogin no` in lesson 6.3,
and as the offline root you'll build in Module 7: hold the smallest
capability that does the job.
:::

## Ask it questions

```sql
.tables
```

A long list. Gitea has dozens of tables and you only care about two today:
`user` and `repository`.

`.schema` shows how a table is built, which is how you find out what
columns exist without guessing:

```sql
.schema user
```

Now the query that everything else is a variation on. **SELECT** picks
columns, **FROM** picks the table:

```sql
SELECT name, is_admin FROM user;
```

```text
name      is_admin
--------  --------
sokoth    1
testuser  0
```

Your own account, and whether it holds admin. That `1` and `0` are how
SQLite stores true and false.

**WHERE** filters rows:

```sql
SELECT name FROM user WHERE is_admin = 1;
```

That is the "who has admin on this system" question from lesson 5.6,
asked of a different system. It's the same question every audit asks, and
you can now answer it for anything that stores its users in a database.

**COUNT** answers "how many" without printing everything:

```sql
SELECT COUNT(*) FROM repository;
```

```text
3
```

**ORDER BY** sorts, and **LIMIT** cuts the list short. Together they
answer most "top N" questions you'll ever be asked:

```sql
SELECT name, num_stars FROM repository ORDER BY num_stars DESC LIMIT 5;
```

## The join, which is the whole point of relational

The `repository` table stores an `owner_id`, not an owner's name. Ask for
repositories on their own and you get a number you can't read:

```sql
SELECT name, owner_id FROM repository;
```

**JOIN** stitches the two tables together on the value they share:

```sql
SELECT r.name AS repo, u.name AS owner
FROM repository r
JOIN user u ON r.owner_id = u.id
ORDER BY r.name;
```

```text
repo       owner
---------  --------
lab-vault  sokoth
sandbox    testuser
scripts    sokoth
```

Read the query aloud and it says what it does: take repositories, attach
the user whose `id` matches the repository's `owner_id`, show me the two
names. The `r` and `u` are just short nicknames so the rest is readable.

This is why the owner's name is stored once, in one place. Rename that
user and every repository reports the new name immediately, because
nothing copied it. Store the name in both tables and you have two
versions of the truth and no way to know which is current. That single
idea is what "relational" is really about, and it's most of database
design.

## What carries forward

The SQL you just used is not SQLite-specific. `SELECT`, `WHERE`, `COUNT`,
`ORDER BY`, and `JOIN` work essentially unchanged against PostgreSQL,
MySQL, and SQL Server. What changes is how you connect and who manages the
server, not how you ask.

You'll use this again in Module 13, where a vulnerability scanner hands
you thousands of findings across dozens of hosts. "Which of my machines
has a finding that CISA lists as actively exploited" is a join between two
tables, and it's a far better tool than scrolling a report.

## Make it yours

1. Find out when your account was created. The column is `created_unix`
   and it holds a Unix timestamp, which is seconds since 1970. SQLite can
   translate it: `SELECT name, datetime(created_unix, 'unixepoch') FROM
   user;`
2. Count how many repositories are private versus public, in one query.
   You'll want `COUNT(*)`, and `GROUP BY is_private` to split the count
   into groups rather than totalling everything.
3. Harder, and genuinely useful: list every user who owns no repositories
   at all. There are a few ways; a `LEFT JOIN` where the repository side
   comes back empty is the classic one. If it fights you, this is a good
   thing to take to Claude using lesson 1.6's rule: ask it to explain the
   difference between `JOIN` and `LEFT JOIN`, then write the query
   yourself.
