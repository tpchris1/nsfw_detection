#!/bin/bash

dockerComposeCreate(){
    echo "Creating docker-compose.yml..."

    touch docker-compose.yml
    
    echo "version: \"3.7\"" > docker-compose.yml
    echo "services:" >> docker-compose.yml
    echo "" >> docker-compose.yml

    index=1
    while [ "$index" -le "$1" ]
    do
        echo "  api"$index":" >> docker-compose.yml
        echo "    container_name: api"$index"_container" >> docker-compose.yml
        echo "    restart: always" >> docker-compose.yml
        echo "    build:" >> docker-compose.yml
        echo "      context: ./api" >> docker-compose.yml
        echo "      args:" >> docker-compose.yml
        echo "        CONTAINER_INDEX: "$index >> docker-compose.yml
        echo "        CONTAINER_WORKDIR: \"docker_nsfw"$index"/\" " >> docker-compose.yml
        echo "    volumes:" >> docker-compose.yml
        echo "      - api"$index"-volume:/docker_nsfw"$index >> docker-compose.yml
        echo "      - ./api"$index"_container:/docker_nsfw"$index"/media/" >> docker-compose.yml
        echo "" >> docker-compose.yml
        index=`expr $index + 1`
    done

    echo "  nginx:" >> docker-compose.yml
    echo "    container_name: nginx-container" >> docker-compose.yml
    echo "    restart: always" >> docker-compose.yml
    echo "    build: ./nginx" >> docker-compose.yml
    echo "    ports:" >> docker-compose.yml
    echo "      - \"80:80\"" >> docker-compose.yml
    echo "    volumes:" >> docker-compose.yml
    
    index=1
    while [ "$index" -le "$1" ]
    do
        echo "      - api"$index"-volume:/etc/nginx/api"$index"_volume/" >> docker-compose.yml
        echo "      - ./api"$index"_container:/etc/nginx/api"$index"_volume/media/" >> docker-compose.yml
        index=`expr $index + 1`
    done
    
    echo "" >> docker-compose.yml

    echo "volumes:" >> docker-compose.yml
    index=1
    while [ "$index" -le "$1" ]
    do
        echo "  api"$index"-volume:" >> docker-compose.yml
        index=`expr $index + 1`
    done
    
}

nginxConfCreate(){
    echo "Creating nginx/nsfw_detection.conf..."

    touch nginx/nsfw_detection.conf

    echo "# nsfw_detection.conf" > nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    echo "upstream django {" >> nginx/nsfw_detection.conf

    index=1
    while [ "$index" -le "$1" ]
    do
        echo "    server unix:/etc/nginx/api"$index"_volume/nsfw_detection.sock; # for a file socket (better version)" >> nginx/nsfw_detection.conf
        index=`expr $index + 1`
    done
    echo "" >> nginx/nsfw_detection.conf


    echo "}" >> nginx/nsfw_detection.conf
    echo "server {" >> nginx/nsfw_detection.conf
    echo "    listen      80; # the port your site will be served on" >> nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    echo "    server_name 127.0.0.1; # substitute your machine's IP address or FQDN" >> nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    echo "    charset     utf-8;" >> nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    echo "    client_max_body_size 75M; # max upload size" >> nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    echo "    location /static {" >> nginx/nsfw_detection.conf
    echo "        alias /etc/nginx/api1_volume/static; # Django project's static files" >> nginx/nsfw_detection.conf
    echo "    }" >> nginx/nsfw_detection.conf
    echo "" >> nginx/nsfw_detection.conf
    
    index=1
    while [ "$index" -le "$1" ]
    do
        echo "    location /container/"$index"/media  {" >> nginx/nsfw_detection.conf
        echo "        alias /etc/nginx/api"$index"_volume/media;  # Django project's media files" >> nginx/nsfw_detection.conf
        echo "    }" >> nginx/nsfw_detection.conf
        index=`expr $index + 1`
    done    
    echo "" >> nginx/nsfw_detection.conf

    index=1
    while [ "$index" -le "$1" ]
    do
        echo "    location /container/"$index"/admin {" >> nginx/nsfw_detection.conf
        echo "        uwsgi_pass  unix:/etc/nginx/api"$index"_volume/nsfw_detection.sock;" >> nginx/nsfw_detection.conf
        echo "        include     /etc/nginx/api1_volume/uwsgi_params; # the uwsgi_params file you installed" >> nginx/nsfw_detection.conf
        echo "    }" >> nginx/nsfw_detection.conf
        index=`expr $index + 1`
    done    

    echo "" >> nginx/nsfw_detection.conf
    echo "    location / {" >> nginx/nsfw_detection.conf
    echo "        uwsgi_pass  django;" >> nginx/nsfw_detection.conf
    echo "        include     /etc/nginx/api1_volume/uwsgi_params; # the uwsgi_params file you installed" >> nginx/nsfw_detection.conf
    echo "    }" >> nginx/nsfw_detection.conf
    echo "}" >> nginx/nsfw_detection.conf


}


echo "Starting nsfw_run..."
if [ "$1" = "clear" ]; then
    echo "Clearing..."
    if [ "$2" = "-i" -a "$3" -gt 0 ]; then
        index_clear=1
        while [ "$index_clear" -le "$3" ]
        do
            folder_name="api"${index_clear}"_container"
            echo "Deleting... "$folder_name
            index_clear=`expr $index_clear + 1`
            sudo rm -rf $folder_name  
        done
    else
        echo "Clear grammar not right. Type 'help' for more guide."
    fi
elif [ "$1" = "run" ]; then
    echo "Running..."
    if [ "$2" = "-i" -a "$3" -gt 0 ]; then
        dockerComposeCreate $3
        nginxConfCreate $3
        docker-compose down -v
        docker-compose build -q
        docker-compose up -d --remove-orphans
    else
        echo "'run' grammar not right. Type 'help' for more guide."
    fi
elif [ "$1" = "stop" ]; then
    echo "Stopping..."
    docker-compose down -v
    # if [ "$2" = "-i" -a "$3" -gt 0 ]; then
        # dockerComposeCreate $3
        # nginxConfCreate $3
        # docker-compose build -q
        # docker-compose up -d --remove-orphans
    # else
        # echo "'stop' grammar not right. Type 'help' for more guide."
    # fi
elif [ "$1" = "debug" ]; then
    echo "Debugging..."
    if [ "$2" = "-i" -a "$3" -gt 0 ]; then
        dockerComposeCreate $3
        nginxConfCreate $3
        docker-compose down -v
        docker-compose build
        docker-compose up --remove-orphans
    else
        echo "'debug' grammar not right. Type 'help' for more guide."
    fi
elif [ "$1" = "help" ]; then
    echo "Info: 'run -i 8' to run 8 containers in background, e.g.('api1_container','api2_container', ...)." 
    echo "Info: 'debug -i 8' to run 8 containers in foreground to check logs, e.g.('api1_container','api2_container', ...)." 
    echo "Info: 'clear -i 8' to clear 8 media folders of relative containers, e.g.('api1_container','api2_container', ...)." 
    echo "Info: 'help' to get more info about how to use the shell file."
else
    echo "No Such Command!"
    echo "Type 'help' for more."
fi