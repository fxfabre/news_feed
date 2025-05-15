# news_feed
Read some news feed (email, ...) and generate a daily synthesis - or feed Notebook LM ?

## To setup n8n
Launch n8n service :
- docker compose up -d

Create gmail connection :
- Create a GCP project if needed
- API & Services -> enable gmail API
- API & Services -> Fill Oauth consent screen

Sample .env file (replace values with a $):
```env
# n8n service
DB_TYPE=postgresdb

DB_POSTGRESDB_HOST=$host_name
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=$database_name
DB_POSTGRESDB_USER=$pg_user
DB_POSTGRESDB_PASSWORD=$pg_password

# Database
POSTGRES_USER=$pg_user
POSTGRES_PASSWORD=$pg_password
POSTGRES_DB=$database_name
```

## Template projects used
To use a template
- go to the url, select "use for free" and copy workflow to json and save it in a file.
- Then create a new workflow, top right > import from file
Template url :
- https://n8n.io/workflows/2433-daily-podcast-summary/
- https://n8n.io/workflows/2219-transforming-emails-into-podcasts/

## n8n notes
- The "simplify" option in a task does not simplify the UI and display only simple options.
  It filters the output from the node, returning fewer data

