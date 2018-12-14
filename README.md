# bigPanda ops exercise

## Requirements
 * python3 
 * docker-ce 1.13.0+ or higher
 * docker-compose , latest
 * git 
 * user in docker group (linux), user capable of running docker - macOs
 
## Script Flow
1.  script validates that:
    1.  git, docker, docker-compose exist on host
    2. if there are images from previous run - deletes
    3. if there is code from previous run - deletes
    4. if no target dir for images - creates
2. downloads archive from web
3. extracts the archive
4. clones the repo to its running dir ( relative to bigPanda dir)
5. modifies npm app dockerfile - adding curl
6. creates .env file -> path to images is variable
7. add compose file to the cloned repo
8. build the containers with docker-compose
9. start compose

## How-to run
```$xslt
./appDeploy.py
```

 