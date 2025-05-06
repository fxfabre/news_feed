# To setup

Launch n8n service :
- docker compose up -d

Create gmail connection :
- Create a GCP project if needed
- API & Services -> enable gmail API
- API & Services -> Fill Oauth consent screen

## Template projects used
To use a template
- go the the url, select "use for free" and copy workflow to json and save it in a file.
- Then create a new workflow, top right > import from file
Template url :
- https://n8n.io/workflows/2433-daily-podcast-summary/
- https://n8n.io/workflows/2219-transforming-emails-into-podcasts/

## n8n notes
- The "simplify" option in a task does not simplify the UI and display only simple options.
  It filters the output from the node, returning fewer data
