This is a personal boilerplate for Django 4.2 projects hosted on Platform.sh with celery queues and workers, basic smtp, Segment for analytics, CI using Github actions (linting and unit tests), a custom Django User model.


## Set up and run App Instance
Clone repo. Run the following commands to configure the project:
```
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

## SEGMENT_WRITE_KEY
This environment variable will likely need to be set. Use the same key that's in
staging.

## Leverage Services:
Platform.sh lets us provision and tunnel to a clone of a full environment
for use during development. Mostly for queues at this point.

They are awkward to operate. Here's how to set up the tunnel and pull in
environment variables from Platform.sh. These may need to be more securely stored.

1. [Create a tethered connection](https://docs.platform.sh/development/local/tethered.html#create-the-tethered-connection) to platformsh
2. Run this in the console and re-launch the mindshare server:

    $ platform tunnel:open
    $ export PLATFORM_RELATIONSHIPS="$(platform tunnel:info --encode)"
    $ python manage.py runserver

## [View RabbitMQ Web UI (while tethered)](https://docs.platform.sh/add-services/rabbitmq.html#access-the-management-ui)
1. After opening the platformsh tunnel, tunnel to the queue directly with:
    $ ssh $(platform ssh --pipe) -L 15672:queue_sms.internal:15672
2. [View UI in browser](http://localhost:15672)

## Workflow (once project set up):
[Install and authenticate with the Platform CLI](https://docs.platform.sh/administration/cli.html)
1. Create a branch (e.g. `feature/my-new-thing`) from the head of the `production` branch
2. When ready to test deployment, activate a new Platform environment with `platform environment:activate feature/my-new-thing`
3. Push your branch with its changes, if you haven't, with `git push` (or `git push -u origin feature/my-new-thing` on the first push)
4. Set relevant environment variables: https://docs.platform.sh/development/variables/set-variables.html
5. When ready to merge work intro production, create PR in github
6. Merge work in github (once tests pass)


### NOTE:
Because we have a single "app" from Google's perspective, you may need to [revoke access](https://myaccount.google.com/connections) in order to re-authenticate (or switch between environments).

## Expose Server to internet for testing with remote services
```
ngrok http 8000
```

## Useful Platform commands:

Check application logs:
`platform log -e <ENVIRONMENT_NAME> app`

In-process deploy log (e.g. after `git push`):
`platform activity:log --type environment.push -e <ENVIRONMENT_NAME>`

SSH directly to an environment:
`platform ssh --project 5nveo3uyaysfa --environment <ENVIRONMEND_NAME> --app <MY_APP_NAME>`

Getting a new environment deploying:
```
git checkout -b my-new-branch
git push -u origin my-new-branch
platform environment:activate
```

## Unit Test Notes:
* Add fake values for any django.conf.settings settings (e.g. those from config.settings) that must be set for unit tests to succeed in `conftest.py`


## Tech Debt:
Local environment a bit much to wrangle with various services