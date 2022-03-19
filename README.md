# Using these tools to make an index to the IMC Shared Documents

## Phase 1: install and configure rclone

 1. Install rclone if you don't have it (sudo apt install rclone)

 1. Configure a "Google Application Client Id" <br>
See [https://rclone.org/drive/#making-your-own-client-id] <br>
This will give you "Client ID" and "Client Secret" magic strings which you'll use next.

 1. From the command line, run

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


## Phase 2: Scan IMC files and prepare report

Run:

    python3  lsf2html.py  -doit

By default, it will run rclone (you might get a prompt to refresh rclone's authentication),
and then write output to **imcindex**.*YYYY-MM-DD*.csv and .html

For other options and advice, run with -h:

    python3  lsf2html.py -h
