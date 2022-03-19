# Using these tools to make an index to the IMC Shared Documents

## Phase 1: install and configure rclone

 1. Install [rclone](https://rclone.org/) if you don't have it.<br>
(if you're on Ubuntu or similar, use: **sudo apt install rclone** )

 1. Configure a "Google Application Client Id" <br>
See [https://rclone.org/drive/#making-your-own-client-id] <br>
This will give you "Client ID" and "Client Secret" magic strings which you'll use next.
**Note** these will only work from the same Google/Google-Suite account that you used to create the Client ID.

 1. Create an rclone "remote" drive name -- essentially a named pointer to the IMC's Google drive (or whatever set of files you'd like to scan).   This tells rclone how to find the top-level Google folder, and whose authentication to use when scanning it.

From the command line, run

    **rclone config**

and follow the prompts:
|Prompt             | Enter |
|:------------------|:------|
|  e/n/d/r/c/s/q> | **n**   (new remote drive) <br>
|  name>          | **imcdrive** <br>
|  Storage>       | **drive**   (this means "Google Drive") <br>
|  client_id>     | *enter the Client ID from above*<br>
|  client_secret> | *enter the Client Secret from above* <br>
|  scope>         | **drive.readonly**  (or, for this purpose, **drive.metadata.readonly** should work too and be more restrictive) <br>
|  <br>root_folder_id>| **0B-sQPHKpBoDOQ20xT2JOUXpfQmM**     (from the [IMC Shared Documents URL](https://drive.google.com/drive/u/0/folders/0B-sQPHKpBoDOQ20xT2JOUXpfQmM) after last "/") <br>
|  <br>service_account_file> | *leave this blank*<br>
|  <br>Edit advanced config? y/n>| **n**<br>
|  <br>Use auto config?<br> * Say Y if not sure<br> * Say N if ... remote or headless ...|*probably* **y** *(pops up a web browser which lets you log in)*<br>*or,* **n** *(prints a URL which you paste into your own browser, log in, get magic code, paste back into rclone)*

**When you authenticate, it will warn that you're authorizing an unapproved app to access files.**
It's OK.   Click to say that you accept the risk.

## Phase 2: Scan IMC files and prepare report

Run:

    python3  lsf2html.py  -doit

This will run rclone to scan the filesystem, and then reprocess its output.

You may get a web-browser prompt to refresh rclone's authentication.   You'll need to log in with the same Google account that you used to create the "Client ID" etc. above -- since that was created without going through the formal publication/approval process, it's a private Client ID.   Google Drive won't let anyone else authenticate to it.

lsf2html will write output to **imcindex**.*YYYY-MM-DD*.csv and .html

(You could instead run, say, **python3 lsf2html.py -o currentimc**
to get non-date-stamped files named **currentimc.csv** and **currentimc.html**.)

For other options and advice, run with -h:

    python3  lsf2html.py -h
